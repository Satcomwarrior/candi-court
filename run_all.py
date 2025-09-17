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

    p8 = sub.add_parser("full", help="Run the full workflow end-to-end")
    p8.add_argument("--case-data", default=str(Path("case_data.sample.json")), help="Path to case data JSON")
    p8.add_argument("--output-dir", default=str(Path("outputs") / "generated_docs"))
    p8.add_argument("--send-intake", action="store_true", help="Actually send intake emails (omit for dry-run)")
    p8.add_argument("--ps-script", help="Optional PowerShell script from powershell/ to run at the end")
    p8.add_argument("--psargs", nargs=argparse.REMAINDER, help="Args passed to the PowerShell script (prefix with --)")

    def _cmd_full(ns):
        # 1) Forms + templates (skip if Snohomish templates already exist)
        try:
            snohomish_dir = Path("templates/family_law_forms/snohomish_county")
            required = [
                snohomish_dir / "snohomish_motion_template.docx",
                snohomish_dir / "snohomish_declaration_template.docx",
                snohomish_dir / "snohomish_contempt_motion_template.docx",
            ]
            def _valid(p: Path) -> bool:
                return p.exists() and p.stat().st_size > 1024
            if all(_valid(p) for p in required):
                print("[INFO] Templates already present; skipping forms download.")
            else:
                try:
                    # Try regenerating templates only (cheap)
                    from download_family_law_forms import WashingtonFormsDownloader
                    dl = WashingtonFormsDownloader()
                    dl.create_snohomish_county_templates()
                    print("[INFO] Recreated Snohomish templates.")
                except Exception:
                    # As a fallback, attempt full forms download if space permits
                    from download_family_law_forms import WashingtonFormsDownloader
                    dl = WashingtonFormsDownloader()
                    stats = dl.download_all_forms()
                    dl.create_snohomish_county_templates()
                    dl.save_download_log()
                    dl.generate_summary_report(stats)
        except Exception as e:
            print(f"[WARN] Forms step failed: {e}")

        # 2) Generate documents
        try:
            from scripts.generate_case_documents import main as gen_main
            argv = ["--input", ns.case_data, "--output-dir", ns.output_dir]
            import sys as _sys
            _sys.argv = ["generate_case_documents.py"] + argv
            gen_main()
        except Exception as e:
            print(f"[WARN] Document generation failed: {e}")

        # 3) Intake email (dry-run unless flagged)
        try:
            body_path = Path("intake_email_draft.txt")
            if not body_path.exists():
                print("[INFO] Skipping intake email: intake_email_draft.txt not found.")
            else:
                from automation.automate_intake_email import main as intake_main
                argv = ["--body", str(body_path)]
                if not ns.send_intake:
                    argv.append("--dry-run")
                import sys as _sys
                _sys.argv = ["automate_intake_email.py"] + argv
                intake_main()
        except Exception as e:
            print(f"[WARN] Intake email step failed: {e}")

        # 4) Optional PowerShell orchestrator
        if ns.ps_script:
            try:
                _args = argparse.Namespace(script=ns.ps_script, psargs=ns.psargs or [])
                cmd_powershell(_args)
            except SystemExit as se:
                raise
            except Exception as e:
                print(f"[WARN] PowerShell step failed: {e}")

    p8.set_defaults(func=_cmd_full)

    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
