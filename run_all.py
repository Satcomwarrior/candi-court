#!/usr/bin/env python3
"""
Unified runner for core automations in this repo.

Commands:
  - nlp: demo NLP communication analysis
  - forms: download WA forms + create templates
  - analyze-doc: analyze a DOCX for structure and patterns
  - reason: run reasonableness analyzer on a file or text

This script is additive and does not change existing imports.
"""

import argparse
import sys
from pathlib import Path
import subprocess


def cmd_nlp(args):
    from legal_case_workflow import analyze_communication_patterns_nlp
    text = args.text or "You're overreacting and you're imagining things. You better not do that."
    res = analyze_communication_patterns_nlp(text)
    print("Summary:", res.get("summary"))
    print("Sentiment:", res.get("sentiment"))
    print("Coercive patterns:", res.get("coercive_patterns"))


def cmd_forms(args):
    from download_family_law_forms import WashingtonFormsDownloader
    dl = WashingtonFormsDownloader()
    stats = dl.download_all_forms()
    dl.create_snohomish_county_templates()
    dl.save_download_log()
    dl.generate_summary_report(stats)


def cmd_analyze_doc(args):
    from document_pattern_analyzer import LegalDocumentAnalyzer
    p = Path(args.file)
    if not p.exists():
        print(f"File not found: {p}", file=sys.stderr)
        sys.exit(1)
    analyzer = LegalDocumentAnalyzer()
    res = analyzer.analyze_document_file(str(p))
    if not res:
        print("No analysis produced")
        return
    print("Document type:", res.get("document_type"))
    s = res.get("structure_analysis", {})
    print("Structure score:", s.get("structure_score"))


def cmd_reason(args):
    from cli import read_text_file, extract_text_from_docx
    from reasonableness_analyzer import analyze_text
    text = None
    if args.file:
        p = Path(args.file)
        text = extract_text_from_docx(str(p)) if p.suffix.lower() == ".docx" else read_text_file(str(p))
    elif args.text:
        text = args.text
    else:
        text = sys.stdin.read()
    result = analyze_text(text)
    print("Overall score:", result.overall_score)
    print("Level:", result.reasonableness_level.name)


def cmd_powershell(args):
    script_path = Path("powershell") / args.script
    if not script_path.exists():
        print(f"Script not found: {script_path}", file=sys.stderr)
        sys.exit(1)
    # Drop leading '--' in remainder if present
    psargs = args.psargs
    if psargs and psargs[0] == "--":
        psargs = psargs[1:]
    cmd = [
        "powershell",
        "-NoProfile",
        "-ExecutionPolicy",
        "Bypass",
        "-File",
        str(script_path),
        *psargs,
    ]
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        sys.exit(e.returncode)


def main():
    ap = argparse.ArgumentParser(description="Unified legal automations runner")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p1 = sub.add_parser("nlp", help="Run NLP communication analysis")
    p1.add_argument("--text", help="Text to analyze")
    p1.set_defaults(func=cmd_nlp)

    p2 = sub.add_parser("forms", help="Download WA forms and create templates")
    p2.set_defaults(func=cmd_forms)

    p3 = sub.add_parser("analyze-doc", help="Analyze a DOCX document")
    p3.add_argument("file", help="Path to .docx")
    p3.set_defaults(func=cmd_analyze_doc)

    p4 = sub.add_parser("reason", help="Reasonableness analysis for a file or text")
    p4.add_argument("--file", help="Path to .txt or .docx")
    p4.add_argument("--text", help="Raw text input")
    p4.set_defaults(func=cmd_reason)

    p5 = sub.add_parser("intake-email", help="Send intake email to recipients from CSVs")
    p5.add_argument("--subject", default="Case Intake: Background and Next Steps")
    p5.add_argument("--body", default=str(Path("intake_email_draft.txt")))
    p5.add_argument("--attach", action="append", default=[])
    p5.add_argument("--dry-run", action="store_true")
    def _cmd_intake(ns):
        from automation.automate_intake_email import main as intake_main
        argv = [
            "--subject", ns.subject,
            "--body", ns.body,
        ]
        for a in ns.attach:
            argv += ["--attach", a]
        if ns.dry_run:
            argv.append("--dry-run")
        sys.argv = ["automate_intake_email.py"] + argv
        intake_main()
    p5.set_defaults(func=_cmd_intake)

    p6 = sub.add_parser("powershell", help="Run a PowerShell script from powershell/")
    p6.add_argument("script", help="Script filename in powershell/")
    p6.add_argument("psargs", nargs=argparse.REMAINDER, help="Arguments passed to PowerShell (prefix with --)")
    p6.set_defaults(func=cmd_powershell)

    p7 = sub.add_parser("generate-docs", help="Generate Snohomish templates into filled documents")
    p7.add_argument("--input", required=True, help="Path to case data JSON")
    p7.add_argument("--output-dir", default=str(Path("outputs") / "generated_docs"))
    p7.add_argument("--only", nargs="*", choices=["motion", "declaration", "contempt"], help="Limit which docs")
    def _cmd_gen(ns):
        from scripts.generate_case_documents import main as gen_main
        argv = ["--input", ns.input, "--output-dir", ns.output_dir]
        if ns.only:
            argv += ["--only", *ns.only]
        import sys as _sys
        _sys.argv = ["generate_case_documents.py"] + argv
        gen_main()
    p7.set_defaults(func=_cmd_gen)

    p8 = sub.add_parser("screen-analysis", help="Run screen recording analysis with OCR")
    p8.add_argument("--screen-recordings", help="Directory of screen recording video files")
    p8.add_argument("--screenshots", help="Directory of screenshot images")
    p8.add_argument("--transcripts", help="Directory containing transcript or OCR sidecar text files")
    p8.add_argument("--output-dir", default="media_analysis_output", help="Directory for generated analysis artifacts")
    p8.add_argument("--frame-interval", type=float, default=10.0, help="Seconds between sampled frames for OCR")
    p8.add_argument("--max-frames", type=int, default=8, help="Maximum frames to OCR per video")
    p8.add_argument("--skip-audio", action="store_true", help="Disable audio transcription attempts")
    p8.add_argument("--skip-video-ocr", action="store_true", help="Disable OCR sampling from video frames")
    p8.add_argument("--skip-screenshot-ocr", action="store_true", help="Disable OCR on screenshots")
    p8.add_argument("--whisper-model", default="base", help="Whisper model size to use when enabled")
    p8.add_argument("--force", action="store_true", help="Remove existing output directory before running")

    def _cmd_screen(ns):
        from pathlib import Path as _Path
        from media_analysis import AnalysisOptions, run_media_analysis

        options = AnalysisOptions(
            enable_audio_transcription=not ns.skip_audio,
            enable_video_ocr=not ns.skip_video_ocr,
            enable_screenshot_ocr=not ns.skip_screenshot_ocr,
            frame_interval_seconds=ns.frame_interval,
            whisper_model=ns.whisper_model,
            max_frames=ns.max_frames,
        )

        run_media_analysis(
            screen_recordings_dir=_Path(ns.screen_recordings) if ns.screen_recordings else None,
            screenshots_dir=_Path(ns.screenshots) if ns.screenshots else None,
            transcripts_dir=_Path(ns.transcripts) if ns.transcripts else None,
            output_dir=_Path(ns.output_dir),
            options=options,
            force=ns.force,
        )

    p8.set_defaults(func=_cmd_screen)

    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
