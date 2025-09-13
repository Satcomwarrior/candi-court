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

    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()

