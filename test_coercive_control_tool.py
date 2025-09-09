#!/usr/bin/env python3
"""
Test script for the Coercive Control Documentation Tool
"""

import os
import sys
import tempfile
import shutil
from coercive_control_documentation import CoerciveControlDetector, DocumentationGenerator


def test_pattern_detection():
    """Test that the tool correctly detects coercive control patterns."""
    print("Testing Coercive Control Pattern Detection...")
    
    # Create test text with known patterns
    test_texts = {
        "isolation_test": "He controls my passwords and tracks my location on GPS. I'm not allowed to see friends.",
        "financial_test": "She withholds money and sabotages my work. I'm completely financially dependent.",
        "gaslighting_test": "That never happened, you're imagining things. You're being crazy and dramatic.",
        "threats_test": "If you leave me, I'll hurt myself. You'll be responsible for what happens to me.",
        "procedural_test": "Filing another complaint in court to control and harass through legal processes."
    }
    
    detector = CoerciveControlDetector()
    
    total_patterns_detected = 0
    for test_name, test_text in test_texts.items():
        results = detector.scan_text(test_text, test_name)
        patterns_found = len(results)
        total_patterns_detected += patterns_found
        
        print(f"  {test_name}: {patterns_found} pattern categories detected")
        for pattern_name, matches in results.items():
            print(f"    - {pattern_name.replace('_', ' ').title()}: {len(matches)} instances")
    
    print(f"\nTotal pattern categories detected across all tests: {total_patterns_detected}")
    
    # Basic validation
    if total_patterns_detected > 0:
        print("✓ Pattern detection is working correctly")
        return True
    else:
        print("✗ No patterns detected - check implementation")
        return False


def test_report_generation():
    """Test that the tool generates proper reports."""
    print("\nTesting Report Generation...")
    
    # Create temporary directory for test
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create a test text file
        test_file = os.path.join(temp_dir, "test_document.txt")
        with open(test_file, 'w') as f:
            f.write("He controls my passwords and tracks my location. I'm not allowed to see friends. "
                   "She withholds money and I'm financially dependent. That never happened, you're crazy.")
        
        detector = CoerciveControlDetector()
        scan_results = detector.scan_directory(temp_dir)
        
        generator = DocumentationGenerator(detector)
        
        # Test checklist report generation
        checklist_report = generator.generate_checklist_report(scan_results)
        
        # Test JSON report generation
        json_report = generator.generate_json_report(scan_results)
        
        # Basic validation
        if len(checklist_report) > 1000 and len(json_report) > 500:
            print("✓ Report generation is working correctly")
            print(f"  Checklist report: {len(checklist_report)} characters")
            print(f"  JSON report: {len(json_report)} characters")
            return True
        else:
            print("✗ Reports are too short - check implementation")
            return False


def test_file_scanning():
    """Test that the tool can scan different file types."""
    print("\nTesting File Scanning...")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create test text file
        txt_file = os.path.join(temp_dir, "test.txt")
        with open(txt_file, 'w') as f:
            f.write("Control through surveillance and monitoring behavior patterns.")
        
        detector = CoerciveControlDetector()
        
        # Test text file scanning
        txt_results = detector.scan_text_file(txt_file)
        
        print(f"  Text file scanning: {len(txt_results)} pattern categories detected")
        
        if len(txt_results) > 0:
            print("✓ File scanning is working correctly")
            return True
        else:
            print("✗ No patterns detected in file - check implementation")
            return False


def main():
    """Run all tests."""
    print("Coercive Control Documentation Tool - Test Suite")
    print("=" * 55)
    
    tests = [
        test_pattern_detection,
        test_report_generation,
        test_file_scanning
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"✗ Test failed with error: {e}")
    
    print("\n" + "=" * 55)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("✓ All tests passed - tool is ready for use!")
        return True
    else:
        print("✗ Some tests failed - check implementation")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)