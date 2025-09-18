#!/usr/bin/env python3
"""
Reasonableness Analyzer for Legal Requests and Complaints

This module provides functionality to analyze the reasonableness of legal requests
and complaints based on various criteria including clarity, specificity, evidence,
tone, and legal merit.
"""

import re
import math
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum


class ReasonablenessLevel(Enum):
    """Enumeration for reasonableness levels."""
    VERY_UNREASONABLE = 1
    UNREASONABLE = 2
    NEUTRAL = 3
    REASONABLE = 4
    VERY_REASONABLE = 5


@dataclass
class AnalysisResult:
    """Results of reasonableness analysis."""
    overall_score: float
    reasonableness_level: ReasonablenessLevel
    criteria_scores: Dict[str, float]
    details: Dict[str, str]
    suggestions: List[str]


class ReasonablenessAnalyzer:
    """Analyzes the reasonableness of requests and complaints."""
    
    def __init__(self, config: Optional[Dict] = None):
        """Initialize the analyzer with optional configuration."""
        default_config = self._default_config()
        if config:
            # Merge with defaults to ensure all required keys exist
            for key, value in default_config.items():
                if key not in config:
                    config[key] = value
                elif isinstance(value, dict) and isinstance(config[key], dict):
                    # Merge nested dictionaries
                    for nested_key, nested_value in value.items():
                        if nested_key not in config[key]:
                            config[key][nested_key] = nested_value
            self.config = config
        else:
            self.config = default_config
        
    def _default_config(self) -> Dict:
        """Default configuration for the analyzer."""
        return {
            'weights': {
                'clarity': 0.25,
                'specificity': 0.20,
                'evidence': 0.20,
                'tone': 0.15,
                'legal_merit': 0.20
            },
            'thresholds': {
                'very_unreasonable': 1.5,
                'unreasonable': 2.5,
                'neutral': 3.5,
                'reasonable': 4.5
            }
        }
    
    def analyze(self, text: str) -> AnalysisResult:
        """
        Analyze the reasonableness of a request or complaint.
        
        Args:
            text: The text to analyze
            
        Returns:
            AnalysisResult containing the analysis results
        """
        # Clean and preprocess text
        cleaned_text = self._preprocess_text(text)
        
        # Analyze each criterion
        criteria_scores = {
            'clarity': self._analyze_clarity(cleaned_text),
            'specificity': self._analyze_specificity(cleaned_text),
            'evidence': self._analyze_evidence(cleaned_text),
            'tone': self._analyze_tone(cleaned_text),
            'legal_merit': self._analyze_legal_merit(cleaned_text)
        }
        
        # Calculate overall score
        overall_score = self._calculate_overall_score(criteria_scores)
        
        # Determine reasonableness level
        reasonableness_level = self._get_reasonableness_level(overall_score)
        
        # Generate details and suggestions
        details = self._generate_details(criteria_scores, cleaned_text)
        suggestions = self._generate_suggestions(criteria_scores, reasonableness_level)
        
        return AnalysisResult(
            overall_score=overall_score,
            reasonableness_level=reasonableness_level,
            criteria_scores=criteria_scores,
            details=details,
            suggestions=suggestions
        )
    
    def _preprocess_text(self, text: str) -> str:
        """Clean and preprocess the input text."""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text.strip())
        
        # Remove document artifacts
        text = re.sub(r'Page \d+ of \d+', '', text)
        text = re.sub(r'^\s*\d+\.\s*', '', text, flags=re.MULTILINE)
        
        return text
    
    def _analyze_clarity(self, text: str) -> float:
        """Analyze clarity of the text (1-5 scale)."""
        score = 3.0  # Start with neutral
        
        # Check sentence length (shorter sentences are generally clearer)
        sentences = [s.strip() for s in re.split(r'[.!?]+', text) if s.strip()]
        if sentences:
            avg_sentence_length = sum(len(s.split()) for s in sentences) / len(sentences)
            if avg_sentence_length < 15:
                score += 0.5
            elif avg_sentence_length > 30:
                score -= 0.5
        
        # Check for clear structure indicators
        structure_indicators = ['first', 'second', 'third', 'therefore', 'because', 'specifically']
        indicator_count = sum(1 for indicator in structure_indicators if indicator.lower() in text.lower())
        score += min(indicator_count * 0.2, 1.0)
        
        # Check for unclear language
        unclear_phrases = ['thing', 'stuff', 'whatever', 'somehow', 'sort of', 'kind of']
        unclear_count = sum(1 for phrase in unclear_phrases if phrase.lower() in text.lower())
        score -= min(unclear_count * 0.3, 1.5)
        
        return max(1.0, min(5.0, score))
    
    def _analyze_specificity(self, text: str) -> float:
        """Analyze specificity of the request/complaint (1-5 scale)."""
        score = 2.5  # Start slightly below neutral
        
        # Check for specific dates, times, amounts
        date_patterns = [
            r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b',  # MM/DD/YYYY or MM-DD-YYYY
            r'\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}\b',
            r'\b\d{1,2}:\d{2}\s*(?:AM|PM)?\b'  # Time
        ]
        
        date_found = False
        for pattern in date_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                score += 0.4
                date_found = True
                break
        
        # Check for monetary amounts
        money_pattern = r'\$[\d,]+(?:\.\d{2})?'
        if re.search(money_pattern, text):
            score += 0.5
        
        # Check for specific identification numbers
        id_patterns = [
            r'#\d+',  # Invoice/reference numbers
            r'invoice\s*#?\s*\d+',
            r'order\s*#?\s*\d+',
            r'case\s*#?\s*\d+'
        ]
        
        for pattern in id_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                score += 0.3
                break
        
        # Check for specific names and places
        proper_nouns = len(re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', text))
        if proper_nouns > 2:
            score += min(proper_nouns * 0.15, 0.8)
        
        # Penalize vague language more heavily
        vague_words = ['some', 'many', 'several', 'various', 'numerous', 'multiple', 'often', 'sometimes', 'thing', 'stuff']
        vague_count = sum(1 for word in vague_words if word.lower() in text.lower())
        score -= min(vague_count * 0.3, 1.5)
        
        return max(1.0, min(5.0, score))
    
    def _analyze_evidence(self, text: str) -> float:
        """Analyze evidence provided in the text (1-5 scale)."""
        score = 2.0  # Start lower since evidence is crucial
        
        # Check for evidence indicators
        evidence_indicators = [
            'document', 'receipt', 'contract', 'email', 'letter', 'record',
            'witness', 'testimony', 'statement', 'proof', 'evidence',
            'attachment', 'exhibit', 'photo', 'video', 'recording'
        ]
        
        evidence_count = sum(1 for indicator in evidence_indicators if indicator.lower() in text.lower())
        score += min(evidence_count * 0.3, 2.0)
        
        # Check for references to specific documents or sources
        reference_patterns = [
            r'exhibit\s+[A-Z0-9]+',
            r'attachment\s+[A-Z0-9]+',
            r'page\s+\d+',
            r'section\s+\d+',
            r'paragraph\s+\d+'
        ]
        
        for pattern in reference_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                score += 0.4
        
        # Check for factual statements vs opinions
        factual_indicators = ['on', 'at', 'during', 'after', 'before', 'occurred', 'happened', 'received', 'sent']
        factual_count = sum(1 for indicator in factual_indicators if indicator.lower() in text.lower())
        score += min(factual_count * 0.1, 1.0)
        
        return max(1.0, min(5.0, score))
    
    def _analyze_tone(self, text: str) -> float:
        """Analyze the tone of the text (1-5 scale, 5 being most professional)."""
        score = 3.0  # Start with neutral
        
        # Check for professional language
        professional_words = [
            'request', 'respectfully', 'please', 'kindly', 'appreciate',
            'consideration', 'professional', 'appropriate', 'reasonable'
        ]
        professional_count = sum(1 for word in professional_words if word.lower() in text.lower())
        score += min(professional_count * 0.2, 1.5)
        
        # Penalize aggressive or inappropriate language more heavily
        aggressive_words = [
            'demand', 'insist', 'outrageous', 'ridiculous', 'stupid',
            'idiotic', 'incompetent', 'pathetic', 'disgraceful', 'idiot'
        ]
        aggressive_count = sum(1 for word in aggressive_words if word.lower() in text.lower())
        score -= min(aggressive_count * 0.6, 2.5)
        
        # Check for excessive capitalization (indicates shouting)
        caps_ratio = sum(1 for c in text if c.isupper()) / max(len(text), 1)
        if caps_ratio > 0.3:
            score -= 1.5
        elif caps_ratio > 0.15:
            score -= 0.8
        
        # Check for excessive punctuation
        exclamation_count = text.count('!')
        if exclamation_count > 5:
            score -= 1.0
        elif exclamation_count > 2:
            score -= 0.3
        
        return max(1.0, min(5.0, score))
    
    def _analyze_legal_merit(self, text: str) -> float:
        """Analyze potential legal merit (1-5 scale)."""
        score = 3.0  # Start with neutral
        
        # Check for legal terminology (indicates understanding of legal process)
        legal_terms = [
            'breach', 'contract', 'violation', 'statute', 'regulation',
            'liability', 'damages', 'remedy', 'jurisdiction', 'standing',
            'cause of action', 'due process', 'negligence', 'misconduct'
        ]
        legal_count = sum(1 for term in legal_terms if term.lower() in text.lower())
        score += min(legal_count * 0.2, 1.5)
        
        # Check for citation of laws, rules, or procedures
        citation_patterns = [
            r'\b\d+\s*U\.?S\.?C\.?\s*§?\s*\d+',  # USC citations
            r'\bRCW\s+\d+\.\d+\.\d+',  # Washington state law
            r'\bRule\s+\d+',
            r'\bSection\s+\d+'
        ]
        
        for pattern in citation_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                score += 0.5
        
        # Check for unrealistic expectations or frivolous claims
        frivolous_indicators = [
            'million dollars', 'billion', 'sue everyone', 'jail time',
            'criminal charges', 'FBI', 'federal investigation', 'destroy your business'
        ]
        frivolous_count = sum(1 for indicator in frivolous_indicators if indicator.lower() in text.lower())
        score -= min(frivolous_count * 0.8, 2.5)
        
        return max(1.0, min(5.0, score))
    
    def _calculate_overall_score(self, criteria_scores: Dict[str, float]) -> float:
        """Calculate weighted overall score."""
        weights = self.config['weights']
        total_score = sum(criteria_scores[criterion] * weights[criterion] 
                         for criterion in criteria_scores)
        return round(total_score, 2)
    
    def _get_reasonableness_level(self, score: float) -> ReasonablenessLevel:
        """Determine reasonableness level based on score."""
        thresholds = self.config['thresholds']
        
        if score <= thresholds['very_unreasonable']:
            return ReasonablenessLevel.VERY_UNREASONABLE
        elif score <= thresholds['unreasonable']:
            return ReasonablenessLevel.UNREASONABLE
        elif score <= thresholds['neutral']:
            return ReasonablenessLevel.NEUTRAL
        elif score <= thresholds['reasonable']:
            return ReasonablenessLevel.REASONABLE
        else:
            return ReasonablenessLevel.VERY_REASONABLE
    
    def _generate_details(self, criteria_scores: Dict[str, float], text: str) -> Dict[str, str]:
        """Generate detailed explanations for each criterion."""
        details = {}
        
        for criterion, score in criteria_scores.items():
            if score >= 4.0:
                level = "Excellent"
            elif score >= 3.5:
                level = "Good"
            elif score >= 2.5:
                level = "Fair"
            elif score >= 1.5:
                level = "Poor"
            else:
                level = "Very Poor"
            
            details[criterion] = f"{level} ({score:.1f}/5.0)"
        
        return details
    
    def _generate_suggestions(self, criteria_scores: Dict[str, float], 
                            reasonableness_level: ReasonablenessLevel) -> List[str]:
        """Generate suggestions for improvement."""
        suggestions = []
        
        if criteria_scores['clarity'] < 3.0:
            suggestions.append("Improve clarity by using shorter sentences and avoiding ambiguous language.")
        
        if criteria_scores['specificity'] < 3.0:
            suggestions.append("Provide more specific details including dates, times, amounts, and names.")
        
        if criteria_scores['evidence'] < 3.0:
            suggestions.append("Include supporting evidence such as documents, receipts, or witness statements.")
        
        if criteria_scores['tone'] < 3.0:
            suggestions.append("Use more professional language and avoid aggressive or emotional terms.")
        
        if criteria_scores['legal_merit'] < 3.0:
            suggestions.append("Consider consulting with a legal professional to strengthen legal arguments.")
        
        if reasonableness_level in [ReasonablenessLevel.VERY_UNREASONABLE, ReasonablenessLevel.UNREASONABLE]:
            suggestions.append("Consider revising the request to be more reasonable and achievable.")
        
        return suggestions


def analyze_text(text: str, config: Optional[Dict] = None) -> AnalysisResult:
    """Convenience function to analyze text with default analyzer."""
    analyzer = ReasonablenessAnalyzer(config)
    return analyzer.analyze(text)


if __name__ == "__main__":
    # Example usage
    sample_text = """
    I am writing to request a refund of $150.00 for the defective product I purchased
    on January 15, 2024. The item (Invoice #12345) stopped working after two days.
    I have the receipt and photos of the defect. Please process this refund within
    10 business days as stated in your return policy.
    """
    
    result = analyze_text(sample_text)
    print(f"Overall Score: {result.overall_score}")
    print(f"Reasonableness Level: {result.reasonableness_level.name}")
    print(f"Criteria Scores: {result.criteria_scores}")
    print(f"Suggestions: {result.suggestions}")