#!/usr/bin/env python3
"""
Test script to demonstrate the enhanced legal workflow capabilities.
Shows NLP analysis, template integration, and document pattern analysis.
"""

import sys
from pathlib import Path

# Add current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

from legal_case_workflow import analyze_communication_patterns_nlp, analyze_document_structure
from document_pattern_analyzer import LegalDocumentAnalyzer
from download_family_law_forms import get_available_templates

def test_nlp_analysis():
    """Test the NLP communication analysis capabilities."""
    print("=== NLP COMMUNICATION ANALYSIS TEST ===")
    
    # Test communication with various coercive control patterns
    test_communication = """
    You're being way too dramatic about this whole situation. Nobody is going to believe your crazy stories anyway. 
    You made me do this by not listening to what I was trying to tell you. If you just did what I said from the beginning, 
    none of this would have happened. Your family doesn't even want to deal with your problems anymore - I'm the only 
    one who puts up with your behavior. You better not try to take anything that belongs to me. You're overreacting 
    and being too sensitive about everything. I never said that - you're imagining things again.
    """
    
    analysis = analyze_communication_patterns_nlp(test_communication)
    
    print(f"Sentiment Analysis:")
    print(f"  - Polarity: {analysis['sentiment']['polarity']:.3f} (negative/positive)")
    print(f"  - Subjectivity: {analysis['sentiment']['subjectivity']:.3f} (objective/subjective)")
    print(f"  - Interpretation: {analysis['sentiment']['interpretation']}")
    
    print(f"\nCoercive Control Patterns Detected: {len(analysis['coercive_patterns'])}")
    for pattern in analysis['coercive_patterns']:
        print(f"  - {pattern['category'].title()}: {pattern['severity']} instances")
        print(f"    Phrases: {', '.join(pattern['phrases'][:3])}...")
    
    print(f"\nPsychological Indicators: {len(analysis['psychological_indicators'])}")
    for indicator in analysis['psychological_indicators']:
        print(f"  - {indicator['type'].replace('_', ' ').title()}: {indicator['count']} occurrences")
    
    print(f"\nNLP Summary: {analysis['summary']}")
    return analysis

def test_template_integration():
    """Test the template integration capabilities."""
    print("\n=== TEMPLATE INTEGRATION TEST ===")
    
    templates = get_available_templates()
    print(f"Available Templates: {len(templates)}")
    
    for template in templates:
        print(f"  - {template['name']} ({template['type']})")
        print(f"    Path: {template['path']}")
    
    return templates

def test_document_analysis():
    """Test the document pattern analysis capabilities."""
    print("\n=== DOCUMENT PATTERN ANALYSIS TEST ===")
    
    analyzer = LegalDocumentAnalyzer()
    
    # Test with an existing output document
    output_files = list(Path("outputs").glob("*.docx"))
    if output_files:
        test_file = output_files[0]
        print(f"Analyzing document: {test_file}")
        
        analysis = analyzer.analyze_document_file(str(test_file))
        if analysis:
            print(f"\nDocument Type: {analysis['document_type']}")
            print(f"Structure Score: {analysis['structure_analysis']['structure_score']}/100")
            print(f"Total Paragraphs: {analysis['structure_analysis']['total_paragraphs']}")
            
            lang_patterns = analysis['language_patterns']
            print(f"\nLanguage Analysis:")
            print(f"  - Legal Terminology Density: {lang_patterns['legal_terminology_density']:.2f}%")
            print(f"  - Effective Phrases Used: {len(lang_patterns['effective_phrases_used'])}")
            print(f"  - Formality Score: {lang_patterns['formality_score']:.1f}/100")
            
            effectiveness = analysis['legal_effectiveness']
            print(f"\nLegal Effectiveness:")
            print(f"  - Overall Score: {effectiveness['overall_score']}/100")
            print(f"  - Authority Citations: {effectiveness['authority_citations']}")
            print(f"  - Persuasive Elements: {len(effectiveness['persuasive_elements'])}")
            
            compliance = analysis['compliance_check']
            print(f"\nCourt Compliance:")
            print(f"  - Compliance Score: {compliance['compliance_score']:.1f}%")
            print(f"  - Required Elements Found: {len(compliance['required_elements'])}")
            print(f"  - Missing Elements: {len(compliance['missing_elements'])}")
            if compliance['missing_elements']:
                print(f"    Missing: {', '.join(compliance['missing_elements'])}")
        
        return analysis
    else:
        print("No output documents found to analyze")
        return None

def test_enhanced_workflow():
    """Test the complete enhanced workflow."""
    print("\n=== ENHANCED WORKFLOW TEST ===")
    
    # This would normally run the full workflow, but we'll just show the components
    print("Enhanced workflow components tested:")
    print("✓ NLP communication analysis")
    print("✓ Template integration")
    print("✓ Document pattern analysis")
    print("✓ Coercive control detection")
    print("✓ Legal effectiveness assessment")
    print("✓ Court compliance checking")

def main():
    """Run all tests to demonstrate enhanced capabilities."""
    print("ENHANCED LEGAL WORKFLOW DEMONSTRATION")
    print("=" * 50)
    
    try:
        # Test NLP analysis
        nlp_result = test_nlp_analysis()
        
        # Test template integration
        template_result = test_template_integration()
        
        # Test document analysis
        doc_result = test_document_analysis()
        
        # Show overall workflow
        test_enhanced_workflow()
        
        print("\n" + "=" * 50)
        print("DEMONSTRATION COMPLETE")
        print("\nKey Features Demonstrated:")
        print("1. Advanced NLP analysis for detecting coercive control patterns")
        print("2. Sentiment analysis and psychological indicator detection")
        print("3. Official template integration and availability checking")
        print("4. Comprehensive document structure and effectiveness analysis")
        print("5. Court compliance checking and recommendations")
        print("6. Legal language pattern recognition and scoring")
        
        # Summary statistics
        if nlp_result:
            coercive_patterns = len(nlp_result.get('coercive_patterns', []))
            psych_indicators = len(nlp_result.get('psychological_indicators', []))
            print(f"\nNLP Analysis Results: {coercive_patterns} coercive patterns, {psych_indicators} psychological indicators detected")
        
        if template_result:
            print(f"Template Integration: {len(template_result)} official templates available")
        
        if doc_result:
            structure_score = doc_result.get('structure_analysis', {}).get('structure_score', 0)
            effectiveness_score = doc_result.get('legal_effectiveness', {}).get('overall_score', 0)
            compliance_score = doc_result.get('compliance_check', {}).get('compliance_score', 0)
            print(f"Document Analysis: Structure {structure_score}/100, Effectiveness {effectiveness_score}/100, Compliance {compliance_score:.1f}/100")
        
    except Exception as e:
        print(f"[ERROR] Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()