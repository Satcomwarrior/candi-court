#!/usr/bin/env python3
"""Command line interface for the modular manipulation detector."""
import argparse
from manipulation_detector import EnhancedManipulationDetector
from manipulation_detector.reporting import generate_comprehensive_report, export_to_json


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyze text for manipulation patterns")
    parser.add_argument("text", help="Text to analyze")
    parser.add_argument("--json", help="Optional path to export JSON report")
    args = parser.parse_args()

    detector = EnhancedManipulationDetector()
    instances = detector.analyze_text(args.text, source_file="cli")
    report = generate_comprehensive_report(instances)
    print(report)
    if args.json:
        export_to_json(instances, args.json)
        print(f"Report written to {args.json}")


if __name__ == "__main__":
    main()
