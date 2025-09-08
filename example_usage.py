#!/usr/bin/env python3
"""
Example usage of the Coercive Control Documentation Tool

This script demonstrates different ways to use the tool for documenting
coercive control patterns in legal and personal documents.
"""

import os
from coercive_control_documentation import CoerciveControlDetector, DocumentationGenerator


def example_single_text_analysis():
    """Example: Analyze a single piece of text for patterns."""
    print("Example 1: Single Text Analysis")
    print("-" * 40)
    
    # Sample text that might contain coercive control patterns
    sample_text = """
    He always checks my phone and knows my passwords. I'm not allowed to go out
    with friends anymore. When I try to work, he sabotages it by creating drama.
    He says if I ever leave him, he'll hurt himself and it will be my fault.
    When I bring up concerns, he tells me I'm being dramatic and overreacting.
    He files complaints about me to control what I can do.
    """
    
    detector = CoerciveControlDetector()
    results = detector.scan_text(sample_text, "sample_text")
    
    print(f"Patterns detected: {len(results)}")
    for pattern_name, matches in results.items():
        pattern_display = pattern_name.replace("_", " ").title()
        print(f"  • {pattern_display}: {len(matches)} instances")
    
    print()


def example_directory_analysis():
    """Example: Analyze all documents in a directory."""
    print("Example 2: Directory Analysis")
    print("-" * 40)
    
    # Analyze current directory (excluding reports to avoid recursion)
    detector = CoerciveControlDetector()
    scan_results = detector.scan_directory(".")
    
    print(f"Files scanned: {scan_results['summary']['files_scanned']}")
    print(f"Pattern categories detected: {scan_results['summary']['total_patterns_detected']}")
    
    # Show top 5 most detected patterns
    if scan_results['patterns']:
        pattern_counts = [(name, len(matches)) for name, matches in scan_results['patterns'].items()]
        pattern_counts.sort(key=lambda x: x[1], reverse=True)
        
        print("\nTop 5 most detected patterns:")
        for pattern_name, count in pattern_counts[:5]:
            pattern_display = pattern_name.replace("_", " ").title()
            print(f"  • {pattern_display}: {count} instances")
    
    print()


def example_generate_reports():
    """Example: Generate professional reports."""
    print("Example 3: Generate Professional Reports")
    print("-" * 40)
    
    # Sample analysis results
    detector = CoerciveControlDetector()
    sample_text = """
    Control through surveillance, monitoring, and isolating from family.
    Financial control through withholding money and sabotaging work.
    Gaslighting by denying events and claiming victim is imagining things.
    """
    
    results = detector.scan_text(sample_text, "example_document")
    
    # Package results in expected format
    scan_results = {
        "summary": {
            "files_scanned": 1,
            "total_patterns_detected": len(results),
            "scan_timestamp": "2025-09-08T21:30:00.000000"
        },
        "patterns": results
    }
    
    generator = DocumentationGenerator(detector)
    
    # Generate checklist report
    print("Generating checklist report for mental health professionals...")
    checklist_report = generator.generate_checklist_report(scan_results)
    print(f"✓ Checklist report generated ({len(checklist_report)} characters)")
    
    # Generate JSON report
    print("Generating JSON report for programmatic analysis...")
    json_report = generator.generate_json_report(scan_results)
    print(f"✓ JSON report generated ({len(json_report)} characters)")
    
    print()


def example_pattern_information():
    """Example: Display information about detected patterns."""
    print("Example 4: Pattern Information")
    print("-" * 40)
    
    detector = CoerciveControlDetector()
    
    print("Available pattern categories:")
    for i, (pattern_name, pattern_data) in enumerate(detector.patterns.items(), 1):
        pattern_display = pattern_name.replace("_", " ").title()
        print(f"{i:2}. {pattern_display}")
        print(f"    Description: {pattern_data['description']}")
        print(f"    Keywords: {len(pattern_data['keywords'])} terms monitored")
        print()


def main():
    """Run all examples."""
    print("Coercive Control Documentation Tool - Usage Examples")
    print("=" * 60)
    print()
    
    examples = [
        example_single_text_analysis,
        example_directory_analysis,
        example_generate_reports,
        example_pattern_information
    ]
    
    for example in examples:
        try:
            example()
        except Exception as e:
            print(f"Error in example: {e}")
            print()
    
    print("=" * 60)
    print("For full documentation, see README.md")
    print("To scan documents: python coercive_control_documentation.py [directory]")


if __name__ == "__main__":
    main()