"""Screen recording and screenshot analysis pipeline with OCR/transcription helpers."""

from __future__ import annotations

import dataclasses
import json
import shutil
import subprocess
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

try:  # pragma: no cover - optional dependency
    from PIL import Image  # type: ignore
except Exception:  # pragma: no cover - optional dependency
    Image = None  # type: ignore

try:  # pragma: no cover - optional dependency
    import pytesseract  # type: ignore
except Exception:  # pragma: no cover - optional dependency
    pytesseract = None  # type: ignore

try:  # pragma: no cover - optional dependency
    import cv2  # type: ignore
except Exception:  # pragma: no cover - optional dependency
    cv2 = None  # type: ignore

VIDEO_EXTENSIONS = {".mp4", ".mov", ".mkv", ".avi", ".webm"}
TEXT_EXTENSIONS = {".txt", ".md"}
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".bmp", ".tiff"}


@dataclass
class AnalysisOptions:
    """Configuration controlling how media analysis is performed."""

    enable_audio_transcription: bool = True
    enable_video_ocr: bool = True
    enable_screenshot_ocr: bool = True
    frame_interval_seconds: float = 10.0
    whisper_model: str = "base"
    max_frames: int = 8


@dataclass
class ScreenRecordingJob:
    """Describes a screen recording that should be analyzed."""

    source: Path
    label: Optional[str] = None
    transcript_path: Optional[Path] = None
    transcript_text: Optional[str] = None
    precomputed_frames: Dict[str, str] = field(default_factory=dict)


@dataclass
class ScreenshotJob:
    """Describes a screenshot to run OCR against."""

    source: Path
    label: Optional[str] = None
    ocr_path: Optional[Path] = None
    ocr_text: Optional[str] = None


@dataclass
class TranscriptResult:
    text: Optional[str]
    source: str
    success: bool
    error: Optional[str] = None


@dataclass
class OcrResult:
    text: Optional[str]
    source: str
    success: bool
    error: Optional[str] = None
    frame_id: Optional[str] = None
    image_path: Optional[str] = None


@dataclass
class ScreenRecordingResult:
    source: str
    label: str
    transcript: TranscriptResult
    ocr_frames: List[OcrResult]
    metadata: Dict[str, object]
    insights: Dict[str, object]
    notes: List[str] = field(default_factory=list)


@dataclass
class ScreenshotResult:
    source: str
    label: str
    ocr: OcrResult
    metadata: Dict[str, object]
    insights: Dict[str, object]
    notes: List[str] = field(default_factory=list)


@dataclass
class MediaAnalysisSummary:
    screen_recordings: List[ScreenRecordingResult]
    screenshots: List[ScreenshotResult]
    generated_at: str
    options: Dict[str, object]


def run_media_analysis(
    screen_recordings_dir: Optional[Path],
    screenshots_dir: Optional[Path],
    transcripts_dir: Optional[Path],
    output_dir: Path,
    options: Optional[AnalysisOptions] = None,
    force: bool = False,
) -> MediaAnalysisSummary:
    """Run analysis on the provided media directories and return a summary."""

    options = options or AnalysisOptions()
    output_dir = output_dir.resolve()
    screen_out_dir = output_dir / "screen_recordings"
    screenshot_out_dir = output_dir / "screenshots"

    if output_dir.exists() and force:
        shutil.rmtree(output_dir)
    screen_out_dir.mkdir(parents=True, exist_ok=True)
    screenshot_out_dir.mkdir(parents=True, exist_ok=True)

    screen_jobs = _discover_screen_jobs(screen_recordings_dir, transcripts_dir)
    screenshot_jobs = _discover_screenshot_jobs(screenshots_dir)

    screen_results: List[ScreenRecordingResult] = []
    for job in screen_jobs:
        job_out_dir = screen_out_dir / (job.label or job.source.stem)
        job_out_dir.mkdir(parents=True, exist_ok=True)
        result = _process_screen_job(job, options, job_out_dir)
        _write_screen_outputs(result, job_out_dir)
        screen_results.append(result)

    screenshot_results: List[ScreenshotResult] = []
    for job in screenshot_jobs:
        shot_out_dir = screenshot_out_dir / (job.label or job.source.stem)
        shot_out_dir.mkdir(parents=True, exist_ok=True)
        result = _process_screenshot_job(job, options)
        _write_screenshot_outputs(result, shot_out_dir)
        screenshot_results.append(result)

    summary = MediaAnalysisSummary(
        screen_recordings=screen_results,
        screenshots=screenshot_results,
        generated_at=datetime.utcnow().isoformat(timespec="seconds") + "Z",
        options=dataclasses.asdict(options),
    )
    _write_summary_files(summary, output_dir)
    return summary


def _discover_screen_jobs(
    screen_dir: Optional[Path], transcripts_dir: Optional[Path]
) -> List[ScreenRecordingJob]:
    jobs: List[ScreenRecordingJob] = []
    if not screen_dir or not screen_dir.exists():
        return jobs

    for video_path in sorted(_iter_media_files(screen_dir, VIDEO_EXTENSIONS)):
        transcript_path = _find_text_sidecar(
            video_path,
            [video_path.parent, transcripts_dir] if transcripts_dir else [video_path.parent],
            suffixes=TEXT_EXTENSIONS,
            tag_variants=("_transcript", "-transcript", " transcript"),
        )
        transcript_text = _read_text_file(transcript_path) if transcript_path else None

        precomputed_frames: Dict[str, str] = {}
        candidate_dirs: List[Path] = [video_path.parent]
        if transcripts_dir and transcripts_dir not in candidate_dirs:
            candidate_dirs.append(transcripts_dir)
        for stem in _generate_alt_stems(video_path.stem):
            prefix = f"{stem}_frame"
            for directory in candidate_dirs:
                if not directory.exists():
                    continue
                for frame_file in sorted(directory.glob(f"{prefix}*")):
                    if frame_file.suffix.lower() not in TEXT_EXTENSIONS:
                        continue
                    frame_id = frame_file.stem[len(prefix) :].lstrip("-_ ") or frame_file.stem
                    precomputed_frames[frame_id] = _read_text_file(frame_file)

        jobs.append(
            ScreenRecordingJob(
                source=video_path,
                transcript_path=transcript_path,
                transcript_text=transcript_text,
                precomputed_frames=precomputed_frames,
            )
        )
    return jobs


def _discover_screenshot_jobs(screenshot_dir: Optional[Path]) -> List[ScreenshotJob]:
    jobs: List[ScreenshotJob] = []
    if not screenshot_dir or not screenshot_dir.exists():
        return jobs

    for image_path in sorted(_iter_media_files(screenshot_dir, IMAGE_EXTENSIONS)):
        ocr_path = _find_text_sidecar(
            image_path,
            [image_path.parent],
            suffixes=TEXT_EXTENSIONS,
            tag_variants=("_ocr", "-ocr", "_text"),
        )
        ocr_text = _read_text_file(ocr_path) if ocr_path else None
        jobs.append(
            ScreenshotJob(
                source=image_path,
                ocr_path=ocr_path,
                ocr_text=ocr_text,
            )
        )
    return jobs


def _iter_media_files(directory: Path, extensions: Iterable[str]) -> Iterable[Path]:
    normalized = {ext.lower() for ext in extensions}
    for path in directory.iterdir():
        if path.is_file() and path.suffix.lower() in normalized:
            yield path


def _generate_alt_stems(stem: str) -> List[str]:
    variants = {
        stem,
        stem.lower(),
        stem.replace(" ", "_"),
        stem.replace(" ", "-"),
    }
    return sorted(variants)


def _find_text_sidecar(
    base_path: Path,
    directories: Sequence[Optional[Path]],
    suffixes: Iterable[str],
    tag_variants: Sequence[str],
) -> Optional[Path]:
    suffixes = tuple(suffixes)
    for directory in directories:
        if directory is None or not directory.exists():
            continue
        for stem in _generate_alt_stems(base_path.stem):
            for tag in ("", *tag_variants):
                for suffix in suffixes:
                    candidate = directory / f"{stem}{tag}{suffix}"
                    if candidate.exists():
                        return candidate
    return None


def _read_text_file(path: Optional[Path]) -> str:
    if not path:
        return ""
    return path.read_text(encoding="utf-8", errors="ignore").strip()


def _process_screen_job(
    job: ScreenRecordingJob, options: AnalysisOptions, job_out_dir: Path
) -> ScreenRecordingResult:
    transcript = _load_transcript(job, options, job_out_dir)
    metadata = _collect_video_metadata(job.source)
    ocr_frames = _collect_video_ocr(job, options, job_out_dir)
    combined_ocr_texts = [frame.text for frame in ocr_frames if frame.text]
    insights = _generate_insights(transcript.text, combined_ocr_texts)

    notes: List[str] = []
    if not transcript.success and transcript.error:
        notes.append(f"Transcript unavailable: {transcript.error}")
    if not combined_ocr_texts and ocr_frames:
        # There were OCR attempts but all failed.
        failures = [frame.error for frame in ocr_frames if frame.error]
        if failures:
            notes.append("; ".join(sorted(set(failures))))
    if not ocr_frames:
        notes.append("No OCR frames captured")

    return ScreenRecordingResult(
        source=str(job.source),
        label=job.label or job.source.stem,
        transcript=transcript,
        ocr_frames=ocr_frames,
        metadata=metadata,
        insights=insights,
        notes=notes,
    )


def _process_screenshot_job(job: ScreenshotJob, options: AnalysisOptions) -> ScreenshotResult:
    ocr_result = _load_or_perform_ocr(job, options)
    metadata = _collect_image_metadata(job.source)
    insights = _generate_insights(ocr_result.text, [])
    notes: List[str] = []
    if not ocr_result.success and ocr_result.error:
        notes.append(f"OCR unavailable: {ocr_result.error}")
    return ScreenshotResult(
        source=str(job.source),
        label=job.label or job.source.stem,
        ocr=ocr_result,
        metadata=metadata,
        insights=insights,
        notes=notes,
    )


def _load_transcript(
    job: ScreenRecordingJob, options: AnalysisOptions, job_out_dir: Path
) -> TranscriptResult:
    if job.transcript_text:
        return TranscriptResult(
            text=job.transcript_text,
            source=str(job.transcript_path or "provided"),
            success=True,
        )
    if job.transcript_path and job.transcript_path.exists():
        return TranscriptResult(
            text=_read_text_file(job.transcript_path),
            source=str(job.transcript_path),
            success=True,
        )
    if not options.enable_audio_transcription:
        return TranscriptResult(
            text=None,
            source="audio-transcription",
            success=False,
            error="Audio transcription disabled by configuration",
        )

    audio_path, error = _extract_audio(job.source, job_out_dir)
    if error:
        return TranscriptResult(
            text=None,
            source="audio-extraction",
            success=False,
            error=error,
        )

    text, engine, success, transcription_error = _transcribe_audio(audio_path, options.whisper_model)
    if not success or text is None:
        return TranscriptResult(
            text=None,
            source=engine,
            success=False,
            error=transcription_error,
        )
    return TranscriptResult(text=text, source=engine, success=True)


def _load_or_perform_ocr(job: ScreenshotJob, options: AnalysisOptions) -> OcrResult:
    if job.ocr_text:
        return OcrResult(
            text=job.ocr_text,
            source=str(job.ocr_path or "provided"),
            success=True,
        )
    if job.ocr_path and job.ocr_path.exists():
        return OcrResult(
            text=_read_text_file(job.ocr_path),
            source=str(job.ocr_path),
            success=True,
        )

    text, engine, success, error = _perform_image_ocr(job.source, options.enable_screenshot_ocr)
    return OcrResult(text=text, source=engine, success=success, error=error)


def _collect_video_metadata(video_path: Path) -> Dict[str, object]:
    metadata: Dict[str, object] = {
        "size_bytes": video_path.stat().st_size if video_path.exists() else 0,
        "exists": video_path.exists(),
    }
    if not video_path.exists() or cv2 is None:
        if cv2 is None:
            metadata["warning"] = "OpenCV not installed"
        return metadata

    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():  # pragma: no cover - depends on system codecs
        cap.release()
        metadata["warning"] = "Unable to open video"
        return metadata

    fps = float(cap.get(cv2.CAP_PROP_FPS) or 0.0)
    frame_count = float(cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0.0)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) or 0)
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) or 0)
    cap.release()

    duration = frame_count / fps if fps > 0 and frame_count > 0 else None
    metadata.update(
        {
            "fps": fps,
            "frame_count": frame_count,
            "duration_seconds": duration,
            "resolution": {"width": width, "height": height} if width and height else None,
        }
    )
    return metadata


def _collect_image_metadata(image_path: Path) -> Dict[str, object]:
    metadata: Dict[str, object] = {
        "size_bytes": image_path.stat().st_size if image_path.exists() else 0,
        "exists": image_path.exists(),
    }
    if not image_path.exists() or Image is None:
        if Image is None:
            metadata["warning"] = "Pillow not installed"
        return metadata
    try:
        with Image.open(image_path) as img:
            metadata.update(
                {
                    "format": img.format,
                    "mode": img.mode,
                    "dimensions": {"width": img.width, "height": img.height},
                }
            )
    except Exception as exc:  # pragma: no cover - depends on image decoder
        metadata["warning"] = str(exc)
    return metadata


def _collect_video_ocr(
    job: ScreenRecordingJob, options: AnalysisOptions, job_out_dir: Path
) -> List[OcrResult]:
    if job.precomputed_frames:
        return [
            OcrResult(
                text=text,
                source="precomputed",
                success=True,
                frame_id=frame_id,
            )
            for frame_id, text in sorted(job.precomputed_frames.items())
        ]

    if not options.enable_video_ocr:
        return []

    frames_dir = job_out_dir / "frames"
    frames_dir.mkdir(parents=True, exist_ok=True)

    frame_paths, error = _extract_frames(job.source, frames_dir, options)
    if error:
        return [
            OcrResult(
                text=None,
                source="frame-extraction",
                success=False,
                error=error,
            )
        ]

    results: List[OcrResult] = []
    for idx, frame_path in enumerate(frame_paths):
        text, engine, success, err = _perform_image_ocr(frame_path, True)
        results.append(
            OcrResult(
                text=text,
                source=engine,
                success=success,
                error=err,
                frame_id=f"frame_{idx:03d}",
                image_path=str(frame_path),
            )
        )
    return results


def _extract_frames(
    video_path: Path, frames_dir: Path, options: AnalysisOptions
) -> Tuple[List[Path], Optional[str]]:
    if cv2 is None:
        return [], "OpenCV not installed; cannot sample frames"
    if not video_path.exists() or video_path.stat().st_size == 0:
        return [], "Video file unavailable or empty"

    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():  # pragma: no cover - depends on system codecs
        cap.release()
        return [], "Unable to open video file"

    fps = float(cap.get(cv2.CAP_PROP_FPS) or 0.0)
    if fps <= 0:
        fps = 30.0
    frame_interval = max(int(round(fps * options.frame_interval_seconds)), 1)

    frames: List[Path] = []
    frame_index = 0
    captured = 0
    while captured < options.max_frames:
        success, frame = cap.read()
        if not success:
            break
        if frame_index % frame_interval == 0:
            frame_path = frames_dir / f"frame_{frame_index:06d}.png"
            try:  # pragma: no cover - depends on codec support
                cv2.imwrite(str(frame_path), frame)
                frames.append(frame_path)
                captured += 1
            except Exception as exc:
                cap.release()
                return [], str(exc)
        frame_index += 1

    cap.release()
    if not frames:
        return [], "No frames captured"
    return frames, None


def _perform_image_ocr(
    image_path: Path, enabled: bool
) -> Tuple[Optional[str], str, bool, Optional[str]]:
    if not enabled:
        return None, "ocr-disabled", False, "OCR disabled by configuration"
    if Image is None:
        return None, "pillow-missing", False, "Pillow not installed"
    if pytesseract is None:
        return None, "pytesseract-missing", False, "pytesseract not installed"
    try:  # pragma: no cover - depends on tesseract availability
        with Image.open(image_path) as img:
            text = pytesseract.image_to_string(img)
        return text.strip(), "pytesseract", True, None
    except Exception as exc:  # pragma: no cover - depends on tesseract runtime
        return None, "pytesseract", False, str(exc)


def _extract_audio(
    video_path: Path, job_out_dir: Path
) -> Tuple[Optional[Path], Optional[str]]:
    if not video_path.exists():
        return None, "Video file does not exist"
    ffmpeg = shutil.which("ffmpeg")
    if ffmpeg is None:
        return None, "ffmpeg binary not available"

    audio_path = job_out_dir / f"{video_path.stem}_audio.wav"
    cmd = [
        ffmpeg,
        "-i",
        str(video_path),
        "-y",
        "-vn",
        "-acodec",
        "pcm_s16le",
        "-ar",
        "16000",
        "-ac",
        "1",
        str(audio_path),
    ]
    proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if proc.returncode != 0:  # pragma: no cover - depends on ffmpeg runtime
        return None, f"ffmpeg failed with code {proc.returncode}"
    return audio_path, None


def _transcribe_audio(
    audio_path: Optional[Path], model_name: str
) -> Tuple[Optional[str], str, bool, Optional[str]]:
    if audio_path is None:
        return None, "audio-missing", False, "Audio extraction failed"
    try:  # pragma: no cover - optional dependency
        import whisper  # type: ignore
    except Exception as exc:  # pragma: no cover - optional dependency
        return None, "whisper-missing", False, str(exc)

    try:  # pragma: no cover - depends on model download
        model = whisper.load_model(model_name)
        result = model.transcribe(str(audio_path))
        text = (result.get("text") or "").strip()
        return text, f"whisper-{model_name}", True, None
    except Exception as exc:  # pragma: no cover - depends on runtime
        return None, "whisper", False, str(exc)


def _generate_insights(transcript_text: Optional[str], ocr_texts: List[Optional[str]]) -> Dict[str, object]:
    combined_parts = [part.strip() for part in [transcript_text, *(ocr_texts or [])] if part]
    combined_text = "\n\n".join(combined_parts)
    insights: Dict[str, object] = {
        "combined_text_length": len(combined_text),
        "keywords": [],
    }
    if not combined_text:
        return insights

    insights["keywords"] = _detect_keywords(combined_text)
    try:
        from legal_case_workflow import analyze_communication_patterns_nlp

        insights["nlp"] = analyze_communication_patterns_nlp(combined_text)
    except Exception as exc:  # pragma: no cover - defensive
        insights["nlp_error"] = str(exc)
    return insights


KEYWORD_MAP: Dict[str, Sequence[str]] = {
    "digital_stalking": ("stalk", "monitor", "screen recording", "recording"),
    "messaging_apps": ("telegram", "signal", "whatsapp", "facebook", "messenger"),
    "access_codes": ("code", "password", "login", "2fa", "otp"),
    "threats": ("threat", "hurt", "harm", "kill", "suicide"),
    "control": ("allowed", "permission", "forbid", "can't", "keys"),
}


def _detect_keywords(text: str) -> List[str]:
    lowered = text.lower()
    hits = []
    for label, tokens in KEYWORD_MAP.items():
        if any(token in lowered for token in tokens):
            hits.append(label)
    return hits


def _write_screen_outputs(result: ScreenRecordingResult, out_dir: Path) -> None:
    data = _dataclass_to_dict(result)
    (out_dir / "analysis.json").write_text(
        json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    if result.transcript.text:
        (out_dir / "transcript.txt").write_text(result.transcript.text, encoding="utf-8")
    if result.ocr_frames:
        lines: List[str] = []
        for frame in result.ocr_frames:
            if frame.text:
                header = frame.frame_id or frame.source
                lines.append(f"## {header}")
                lines.append(frame.text)
        if lines:
            (out_dir / "ocr.txt").write_text("\n\n".join(lines), encoding="utf-8")


def _write_screenshot_outputs(result: ScreenshotResult, out_dir: Path) -> None:
    data = _dataclass_to_dict(result)
    (out_dir / "analysis.json").write_text(
        json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    if result.ocr.text:
        (out_dir / "ocr.txt").write_text(result.ocr.text, encoding="utf-8")


def _write_summary_files(summary: MediaAnalysisSummary, output_dir: Path) -> None:
    summary_data = _dataclass_to_dict(summary)
    (output_dir / "analysis_summary.json").write_text(
        json.dumps(summary_data, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    (output_dir / "analysis_summary.md").write_text(
        _build_summary_markdown(summary), encoding="utf-8"
    )


def _build_summary_markdown(summary: MediaAnalysisSummary) -> str:
    lines: List[str] = []
    lines.append("# Media Analysis Summary")
    lines.append("")
    lines.append(f"Generated at {summary.generated_at}")
    lines.append("")
    lines.append("## Screen Recordings")
    if not summary.screen_recordings:
        lines.append("No screen recordings processed.")
    else:
        for result in summary.screen_recordings:
            lines.append(f"### {result.label}")
            lines.append(f"- Source: `{result.source}`")
            transcript = result.transcript
            if transcript.text:
                lines.append(
                    f"- Transcript: {len(transcript.text.split())} words from {transcript.source}"
                )
            if transcript.error:
                lines.append(f"- Transcript error: {transcript.error}")
            successful_frames = [frame for frame in result.ocr_frames if frame.success and frame.text]
            if successful_frames:
                lines.append(f"- OCR frames captured: {len(successful_frames)}")
            elif result.ocr_frames:
                lines.append("- OCR frames captured: 0 (see analysis.json for errors)")
            if result.insights.get("keywords"):
                lines.append(f"- Keywords: {', '.join(result.insights['keywords'])}")
            nlp_summary = _extract_nlp_summary(result.insights)
            if nlp_summary:
                lines.append(f"- NLP Summary: {nlp_summary}")
            for note in result.notes:
                lines.append(f"- Note: {note}")
            lines.append("")

    lines.append("## Screenshots")
    if not summary.screenshots:
        lines.append("No screenshots processed.")
    else:
        for result in summary.screenshots:
            lines.append(f"### {result.label}")
            lines.append(f"- Source: `{result.source}`")
            if result.ocr.text:
                lines.append(
                    f"- OCR text length: {len(result.ocr.text.split())} words from {result.ocr.source}"
                )
            if result.ocr.error:
                lines.append(f"- OCR error: {result.ocr.error}")
            if result.insights.get("keywords"):
                lines.append(f"- Keywords: {', '.join(result.insights['keywords'])}")
            nlp_summary = _extract_nlp_summary(result.insights)
            if nlp_summary:
                lines.append(f"- NLP Summary: {nlp_summary}")
            for note in result.notes:
                lines.append(f"- Note: {note}")
            lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def _extract_nlp_summary(insights: Dict[str, object]) -> Optional[str]:
    nlp_info = insights.get("nlp")
    if isinstance(nlp_info, dict):
        summary = nlp_info.get("summary")
        if isinstance(summary, str) and summary.strip():
            return summary.strip()
    return None


def _dataclass_to_dict(obj: object) -> object:
    if dataclasses.is_dataclass(obj):
        return {k: _dataclass_to_dict(v) for k, v in dataclasses.asdict(obj).items()}
    if isinstance(obj, dict):
        return {k: _dataclass_to_dict(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_dataclass_to_dict(v) for v in obj]
    if isinstance(obj, Path):
        return str(obj)
    return obj


__all__ = [
    "AnalysisOptions",
    "MediaAnalysisSummary",
    "ScreenshotJob",
    "ScreenshotResult",
    "ScreenRecordingJob",
    "ScreenRecordingResult",
    "run_media_analysis",
]
