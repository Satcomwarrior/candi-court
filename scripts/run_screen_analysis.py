#!/usr/bin/env python3
"""Command line entry-point for the media analysis pipeline."""

from __future__ import annotations

import argparse
from pathlib import Path

from media_analysis import AnalysisOptions, run_media_analysis


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run screen recording analysis with OCR and transcription support",
    )
    parser.add_argument(
        "--screen-recordings",
        type=Path,
        help="Directory containing screen recording video files",
    )
    parser.add_argument(
        "--screenshots",
        type=Path,
        help="Directory containing screenshot image files",
    )
    parser.add_argument(
        "--transcripts",
        type=Path,
        help="Directory with pre-generated transcript or frame OCR text files",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("media_analysis_output"),
        help="Directory where analysis artifacts will be written",
    )
    parser.add_argument(
        "--frame-interval",
        type=float,
        default=10.0,
        help="Seconds between sampled frames for OCR when extracting from video",
    )
    parser.add_argument(
        "--max-frames",
        type=int,
        default=8,
        help="Maximum number of frames to OCR per video when extraction is enabled",
    )
    parser.add_argument(
        "--skip-audio",
        action="store_true",
        help="Disable automatic audio transcription attempts",
    )
    parser.add_argument(
        "--skip-video-ocr",
        action="store_true",
        help="Disable OCR extraction from video frames",
    )
    parser.add_argument(
        "--skip-screenshot-ocr",
        action="store_true",
        help="Disable OCR on screenshot images",
    )
    parser.add_argument(
        "--whisper-model",
        default="base",
        help="Whisper model size to use when transcription is enabled",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Remove any existing output directory before running",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    options = AnalysisOptions(
        enable_audio_transcription=not args.skip_audio,
        enable_video_ocr=not args.skip_video_ocr,
        enable_screenshot_ocr=not args.skip_screenshot_ocr,
        frame_interval_seconds=args.frame_interval,
        whisper_model=args.whisper_model,
        max_frames=args.max_frames,
    )
    run_media_analysis(
        screen_recordings_dir=args.screen_recordings,
        screenshots_dir=args.screenshots,
        transcripts_dir=args.transcripts,
        output_dir=args.output_dir,
        options=options,
        force=args.force,
    )


if __name__ == "__main__":
    main()
