#!/usr/bin/env python3
"""
Command Line Interface for Reasonableness Analyzer

This script provides a command-line interface to analyze the reasonableness
of legal requests and complaints from text files or direct input.
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Optional

from reasonableness_analyzer import ReasonablenessAnalyzer, analyze_text


def read_text_file(file_path: str) -> str:
    """Read text from a file, handling various encodings."""
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    # Try different encodings
    encodings = ['utf-8', 'utf-16', 'cp1252', 'latin1']
    
    for encoding in encodings:
        try:
            with open(path, 'r', encoding=encoding) as f:
                return f.read()
        except UnicodeDecodeError:
            continue
    
    raise ValueError(f"Could not decode file {file_path} with any supported encoding")


def extract_text_from_docx(file_path: str) -> str:
    """Extract text from a DOCX file."""
    try:
        from docx import Document
        doc = Document(file_path)
        return '\n'.join([paragraph.text for paragraph in doc.paragraphs])
    except ImportError:
        print("Warning: python-docx not installed. Cannot read DOCX files.")
        print("Install with: pip install python-docx")
        return ""


def print_analysis_results(result, format_type: str = "text"):
    """Print analysis results in the specified format."""
    if format_type == "json":
        output = {
            "overall_score": result.overall_score,
            "reasonableness_level": result.reasonableness_level.name,
            "criteria_scores": result.criteria_scores,
            "details": result.details,
            "suggestions": result.suggestions
        }
        print(json.dumps(output, indent=2))
    else:
        print("=" * 60)
        print("REASONABLENESS ANALYSIS RESULTS")
        print("=" * 60)
        print(f"Overall Score: {result.overall_score:.2f}/5.0")
        print(f"Reasonableness Level: {result.reasonableness_level.name.replace('_', ' ').title()}")
        print()
        
        print("CRITERIA BREAKDOWN:")
        print("-" * 30)
        for criterion, score in result.criteria_scores.items():
            detail = result.details.get(criterion, "")
            print(f"{criterion.replace('_', ' ').title()}: {score:.2f}/5.0 - {detail}")
        print()
        
        if result.suggestions:
            print("SUGGESTIONS FOR IMPROVEMENT:")
            print("-" * 30)
            for i, suggestion in enumerate(result.suggestions, 1):
                print(f"{i}. {suggestion}")
        print()


def main():
    """Main CLI function."""
    parser = argparse.ArgumentParser(
        description="Analyze the reasonableness of legal requests and complaints",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s -f request.txt
  %(prog)s -f complaint.docx --format json
  %(prog)s -t "I demand a full refund immediately!"
  %(prog)s --stdin < document.txt
        """
    )
    
    # Input options (mutually exclusive)
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument('-f', '--file', 
                           help='Input file (supports .txt, .docx)')
    input_group.add_argument('-t', '--text', 
                           help='Direct text input')
    input_group.add_argument('--stdin', action='store_true',
                           help='Read from standard input')
    
    # Output options
    parser.add_argument('--format', choices=['text', 'json'], default='text',
                       help='Output format (default: text)')
    parser.add_argument('-o', '--output',
                       help='Output file (default: stdout)')
    
    # Configuration options
    parser.add_argument('--config',
                       help='JSON configuration file for analyzer settings')
    parser.add_argument('--weights',
                       help='Custom weights as JSON string (e.g., \'{"clarity": 0.3}\')')
    
    args = parser.parse_args()
    
    # Load configuration
    config = None
    if args.config:
        try:
            with open(args.config, 'r') as f:
                config = json.load(f)
        except Exception as e:
            print(f"Error loading config file: {e}", file=sys.stderr)
            sys.exit(1)
    
    # Apply custom weights
    if args.weights:
        try:
            weights = json.loads(args.weights)
            if config is None:
                config = {}
            if 'weights' not in config:
                config['weights'] = {}
            config['weights'].update(weights)
        except Exception as e:
            print(f"Error parsing weights: {e}", file=sys.stderr)
            sys.exit(1)
    
    # Get input text
    try:
        if args.file:
            file_path = Path(args.file)
            if file_path.suffix.lower() == '.docx':
                text = extract_text_from_docx(args.file)
            else:
                text = read_text_file(args.file)
        elif args.text:
            text = args.text
        elif args.stdin:
            text = sys.stdin.read()
        
        if not text.strip():
            print("Error: No text found to analyze", file=sys.stderr)
            sys.exit(1)
            
    except Exception as e:
        print(f"Error reading input: {e}", file=sys.stderr)
        sys.exit(1)
    
    # Perform analysis
    try:
        result = analyze_text(text, config)
    except Exception as e:
        print(f"Error during analysis: {e}", file=sys.stderr)
        sys.exit(1)
    
    # Output results
    if args.output:
        try:
            with open(args.output, 'w') as f:
                original_stdout = sys.stdout
                sys.stdout = f
                print_analysis_results(result, args.format)
                sys.stdout = original_stdout
            print(f"Results written to {args.output}")
        except Exception as e:
            print(f"Error writing output file: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        print_analysis_results(result, args.format)


if __name__ == "__main__":
    main()