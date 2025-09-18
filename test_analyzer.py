#!/usr/bin/env python3
"""
Test suite for the Reasonableness Analyzer

Run with: python test_analyzer.py
"""

import unittest
from reasonableness_analyzer import ReasonablenessAnalyzer, ReasonablenessLevel, analyze_text


class TestReasonablenessAnalyzer(unittest.TestCase):
    """Test cases for the ReasonablenessAnalyzer class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.analyzer = ReasonablenessAnalyzer()
    
    def test_reasonable_request(self):
        """Test analysis of a reasonable request."""
        text = """
        I am writing to request a refund of $150.00 for the defective product I purchased
        on January 15, 2024. The item (Invoice #12345) stopped working after two days.
        I have the receipt and photos of the defect. Please process this refund within
        10 business days as stated in your return policy.
        """
        
        result = self.analyzer.analyze(text)
        
        self.assertGreater(result.overall_score, 3.0)
        self.assertIn(result.reasonableness_level, [
            ReasonablenessLevel.NEUTRAL, 
            ReasonablenessLevel.REASONABLE, 
            ReasonablenessLevel.VERY_REASONABLE
        ])
        
        # Should have good specificity (dates, amounts, invoice number)
        self.assertGreater(result.criteria_scores['specificity'], 3.5)
        
        # Should have reasonable evidence (receipt, photos mentioned)
        self.assertGreater(result.criteria_scores['evidence'], 2.5)
    
    def test_unreasonable_demand(self):
        """Test analysis of an unreasonable demand."""
        text = """
        YOU IDIOTS MESSED UP MY ORDER AND I DEMAND $10,000 IN DAMAGES!!!
        THIS IS OUTRAGEOUS!!! I'M GOING TO SUE EVERYONE AND CALL THE FBI!!!
        FIX THIS NOW OR I'LL DESTROY YOUR BUSINESS!!!
        """
        
        result = self.analyzer.analyze(text)
        
        self.assertLess(result.overall_score, 3.0)
        self.assertIn(result.reasonableness_level, [
            ReasonablenessLevel.VERY_UNREASONABLE,
            ReasonablenessLevel.UNREASONABLE
        ])
        
        # Should have poor tone due to aggressive language and caps
        self.assertLess(result.criteria_scores['tone'], 2.5)
        
        # Should have poor legal merit due to unrealistic claims
        self.assertLess(result.criteria_scores['legal_merit'], 3.0)
    
    def test_vague_complaint(self):
        """Test analysis of a vague complaint."""
        text = """
        Something went wrong with my thing and I'm not happy about it.
        Someone should fix this somehow. This is sort of urgent I guess.
        """
        
        result = self.analyzer.analyze(text)
        
        # Should have poor clarity and specificity
        self.assertLess(result.criteria_scores['clarity'], 3.0)
        self.assertLess(result.criteria_scores['specificity'], 3.0)
        
        # Should have poor evidence
        self.assertLess(result.criteria_scores['evidence'], 3.0)
    
    def test_professional_legal_request(self):
        """Test analysis of a professional legal request."""
        text = """
        Dear Counsel,
        
        I respectfully request that you cease and desist from the ongoing violation
        of our contract dated March 1, 2024 (Section 4.2). Your client's failure
        to perform under the agreement constitutes a material breach as defined
        in Section 8.1. 
        
        We have documented evidence of non-performance including emails dated
        March 15, 2024, and witness statements from John Doe and Jane Smith.
        Please respond within 30 days to avoid further legal action.
        
        Respectfully,
        [Attorney Name]
        """
        
        result = self.analyzer.analyze(text)
        
        self.assertGreater(result.overall_score, 3.5)
        self.assertIn(result.reasonableness_level, [
            ReasonablenessLevel.REASONABLE,
            ReasonablenessLevel.VERY_REASONABLE
        ])
        
        # Should have good tone
        self.assertGreater(result.criteria_scores['tone'], 3.0)
        
        # Should have good legal merit (legal terms, contract references)
        self.assertGreater(result.criteria_scores['legal_merit'], 3.5)
        
        # Should have good evidence (documents, witnesses)
        self.assertGreater(result.criteria_scores['evidence'], 3.5)
    
    def test_text_preprocessing(self):
        """Test text preprocessing functionality."""
        messy_text = "   This   has   extra   spaces   and\n\n\nline breaks  "
        cleaned = self.analyzer._preprocess_text(messy_text)
        
        self.assertEqual(cleaned, "This has extra spaces and line breaks")
    
    def test_clarity_analysis(self):
        """Test clarity analysis with different text types."""
        # Clear, simple text
        clear_text = "I want a refund. The product is broken. Please help me."
        clear_score = self.analyzer._analyze_clarity(clear_text)
        
        # Complex, unclear text
        unclear_text = ("This thing that I got from you guys somehow doesn't work "
                       "and I sort of need it fixed because it's kind of important "
                       "for the stuff I'm doing and whatever.")
        unclear_score = self.analyzer._analyze_clarity(unclear_text)
        
        self.assertGreater(clear_score, unclear_score)
    
    def test_specificity_analysis(self):
        """Test specificity analysis."""
        # Specific text with dates and amounts
        specific_text = ("On January 15, 2024, at 3:30 PM, I purchased item #12345 "
                        "for $99.99 from John Smith at the Seattle store.")
        specific_score = self.analyzer._analyze_specificity(specific_text)
        
        # Vague text
        vague_text = ("Some time ago I bought something from someone and it cost "
                     "some money and now there are various problems.")
        vague_score = self.analyzer._analyze_specificity(vague_text)
        
        self.assertGreater(specific_score, vague_score)
    
    def test_evidence_analysis(self):
        """Test evidence analysis."""
        # Text with evidence
        evidence_text = ("I have the receipt, photos of the damage, witness statements, "
                        "and email correspondence as proof. See Exhibit A and page 5 "
                        "of the contract.")
        evidence_score = self.analyzer._analyze_evidence(evidence_text)
        
        # Text without evidence
        no_evidence_text = "I think something bad happened and you should fix it."
        no_evidence_score = self.analyzer._analyze_evidence(no_evidence_text)
        
        self.assertGreater(evidence_score, no_evidence_score)
    
    def test_tone_analysis(self):
        """Test tone analysis."""
        # Professional tone
        professional_text = ("I respectfully request your consideration of this matter. "
                           "Please let me know if you need additional information.")
        professional_score = self.analyzer._analyze_tone(professional_text)
        
        # Aggressive tone
        aggressive_text = ("YOU PEOPLE ARE IDIOTS!!! This is OUTRAGEOUS and RIDICULOUS!!! "
                          "I DEMAND immediate action or I'll sue everyone!!!")
        aggressive_score = self.analyzer._analyze_tone(aggressive_text)
        
        self.assertGreater(professional_score, aggressive_score)
    
    def test_legal_merit_analysis(self):
        """Test legal merit analysis."""
        # Text with legal merit
        legal_text = ("This constitutes a breach of contract under RCW 62A.2-601. "
                     "The defendant's negligence caused damages as defined in Section 4. "
                     "We have standing to pursue this cause of action.")
        legal_score = self.analyzer._analyze_legal_merit(legal_text)
        
        # Text with poor legal merit
        frivolous_text = ("I want a billion dollars because someone looked at me funny. "
                         "I'm calling the FBI and suing everyone for criminal charges.")
        frivolous_score = self.analyzer._analyze_legal_merit(frivolous_text)
        
        self.assertGreater(legal_score, frivolous_score)
    
    def test_convenience_function(self):
        """Test the convenience analyze_text function."""
        text = "I would like to request a refund for my purchase. Thank you."
        result = analyze_text(text)
        
        self.assertIsNotNone(result)
        self.assertIsInstance(result.overall_score, float)
        self.assertIsInstance(result.reasonableness_level, ReasonablenessLevel)
    
    def test_custom_config(self):
        """Test analyzer with custom configuration."""
        custom_config = {
            'weights': {
                'clarity': 0.5,  # Higher weight on clarity
                'specificity': 0.2,
                'evidence': 0.1,
                'tone': 0.1,
                'legal_merit': 0.1
            }
        }
        
        analyzer = ReasonablenessAnalyzer(custom_config)
        text = "This is a very clear and simple request."
        result = analyzer.analyze(text)
        
        # With higher clarity weight, clear text should score better
        self.assertGreater(result.overall_score, 3.0)


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and error conditions."""
    
    def test_empty_text(self):
        """Test analysis of empty text."""
        analyzer = ReasonablenessAnalyzer()
        result = analyzer.analyze("")
        
        # Should return low scores for empty text
        self.assertLess(result.overall_score, 3.0)
    
    def test_very_short_text(self):
        """Test analysis of very short text."""
        analyzer = ReasonablenessAnalyzer()
        result = analyzer.analyze("No.")
        
        # Short text should have limitations
        self.assertLess(result.overall_score, 4.0)
    
    def test_very_long_text(self):
        """Test analysis of very long text."""
        analyzer = ReasonablenessAnalyzer()
        # Create a long repetitive text
        long_text = "This is a sentence. " * 100
        result = analyzer.analyze(long_text)
        
        # Should still return valid results
        self.assertIsNotNone(result)
        self.assertGreater(result.overall_score, 0)


if __name__ == "__main__":
    print("Running Reasonableness Analyzer Tests...")
    unittest.main(verbosity=2)