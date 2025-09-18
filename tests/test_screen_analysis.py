import base64
import json
from pathlib import Path

from media_analysis import AnalysisOptions, run_media_analysis


def _write_png(path: Path) -> None:
    # 1x1 transparent PNG pixel
    png_bytes = base64.b64decode(
        "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/w8AAwMCAO5+jL8AAAAASUVORK5CYII="
    )
    path.write_bytes(png_bytes)


def test_media_analysis_uses_sidecar_transcripts_and_ocr(tmp_path: Path) -> None:
    screen_dir = tmp_path / "screen"
    screen_dir.mkdir()
    transcripts_dir = tmp_path / "transcripts"
    transcripts_dir.mkdir()
    screenshots_dir = tmp_path / "screenshots"
    screenshots_dir.mkdir()
    output_dir = tmp_path / "output"

    # Fake screen recording file with accompanying transcript + frame OCR text
    video_path = screen_dir / "recording1.mp4"
    video_path.write_bytes(b"fake video data")
    transcript_path = transcripts_dir / "recording1.txt"
    transcript_text = (
        "Screen recording shows coercive threats: you better not leave. This proves ongoing stalking."
    )
    transcript_path.write_text(transcript_text, encoding="utf-8")
    frame_sidecar = transcripts_dir / "recording1_frame001.txt"
    frame_text = "Telegram login prompt requesting security code."
    frame_sidecar.write_text(frame_text, encoding="utf-8")

    # Screenshot with OCR sidecar text
    screenshot_path = screenshots_dir / "screenshot1.png"
    _write_png(screenshot_path)
    screenshot_ocr = screenshots_dir / "screenshot1.txt"
    screenshot_text = "Telegram chat shows surveillance and stalking directives."
    screenshot_ocr.write_text(screenshot_text, encoding="utf-8")

    summary = run_media_analysis(
        screen_recordings_dir=screen_dir,
        screenshots_dir=screenshots_dir,
        transcripts_dir=transcripts_dir,
        output_dir=output_dir,
        options=AnalysisOptions(enable_audio_transcription=False, enable_video_ocr=True),
    )

    assert summary.screen_recordings, "Expected a screen recording result"
    recording = summary.screen_recordings[0]
    assert recording.transcript.text == transcript_text
    assert recording.ocr_frames and recording.ocr_frames[0].text == frame_text
    assert "digital_stalking" in recording.insights.get("keywords", [])

    assert summary.screenshots, "Expected a screenshot result"
    screenshot = summary.screenshots[0]
    assert screenshot.ocr.text == screenshot_text
    assert "messaging_apps" in screenshot.insights.get("keywords", [])

    # Output artifacts should exist
    summary_json = output_dir / "analysis_summary.json"
    assert summary_json.exists()
    summary_data = json.loads(summary_json.read_text())
    assert summary_data["screen_recordings"]
    assert (output_dir / "analysis_summary.md").exists()
    assert (output_dir / "screen_recordings" / "recording1" / "analysis.json").exists()
    assert (output_dir / "screen_recordings" / "recording1" / "transcript.txt").read_text() == transcript_text
    assert (output_dir / "screenshots" / "screenshot1" / "ocr.txt").read_text() == screenshot_text
