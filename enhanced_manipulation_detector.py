#!/usr/bin/env python3
"""
Enhanced Manipulation Detection Script for Legal Case Workflow

This module combines:
- Keyword/Phrase matching with paraphrased variants
- Regular expression matching for complex patterns
- Semantic similarity checks using spaCy's transformer model
- Sentiment & subjectivity analysis
- Contextual & behavioral features (timing, escalation patterns)

As specified in the problem statement requirements.
"""

import os
import re
import json
import spacy
import numpy as np
from datetime import datetime, timedelta
from collections import defaultdict, Counter
from typing import Dict, List, Tuple, Any, Optional
from dataclasses import dataclass, asdict
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
from textstat import flesch_reading_ease, flesch_kincaid_grade

try:
    from transformers import pipeline, AutoTokenizer, AutoModel
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False
    print("Warning: transformers not available, falling back to spaCy only")


@dataclass
class ManipulationInstance:
    """Data class for manipulation detection instances."""
    pattern_type: str
    pattern_name: str
    text_excerpt: str
    confidence_score: float
    semantic_similarity: float
    sentiment_score: float
    subjectivity_score: float
    context_features: Dict[str, Any]
    timestamp: str
    source_file: str
    line_number: Optional[int] = None


class EnhancedManipulationDetector:
    """Enhanced manipulation detector with semantic analysis and contextual features."""
    
    def __init__(self):
        """Initialize the enhanced detector with NLP models and patterns."""
        print("Initializing Enhanced Manipulation Detector...")
        
        # Load spaCy model
        try:
            self.nlp = spacy.load("en_core_web_sm")
            print("✓ spaCy English model loaded")
        except OSError:
            print("Error: spaCy model not found. Please run: python -m spacy download en_core_web_sm")
            raise
        
        # Initialize sentiment analysis
        self.sentiment_analyzer = None
        if TRANSFORMERS_AVAILABLE:
            try:
                self.sentiment_analyzer = pipeline(
                    "sentiment-analysis", 
                    model="cardiffnlp/twitter-roberta-base-sentiment-latest",
                    return_all_scores=True
                )
                print("✓ Transformer sentiment analyzer loaded")
            except Exception as e:
                print(f"Warning: Could not load transformer sentiment analyzer: {e}")
        
        # Initialize patterns
        self.keyword_patterns = self._initialize_keyword_patterns()
        self.regex_patterns = self._initialize_regex_patterns()
        self.semantic_patterns = self._initialize_semantic_patterns()
        
        # Initialize context tracking
        self.context_history = defaultdict(list)
        self.escalation_tracker = defaultdict(list)
        
        print("✓ Enhanced Manipulation Detector initialized successfully")

    def _initialize_keyword_patterns(self) -> Dict[str, Dict[str, List[str]]]:
        """Initialize expanded keyword patterns with paraphrased variants."""
        return {
            "isolation_tactics": {
                "description": "Attempts to isolate victim from support networks",
                "keywords": [
                    # Direct isolation
                    "isolate", "isolation", "cut off contact", "block contact", 
                    "restrict access", "limit contact", "forbid seeing",
                    # Surveillance variants
                    "tracking", "monitoring", "checking up", "surveillance", "watching",
                    "following", "stalking", "keeping tabs", "spying on",
                    # Permission-based control
                    "need permission", "ask permission", "not allowed", "can't see",
                    "forbidden to", "must ask", "have to check"
                ],
                "paraphrased_variants": [
                    "keeping you away from", "making sure you don't talk to",
                    "I don't want you seeing", "you shouldn't be around",
                    "they're not good for you", "influencing you against me"
                ]
            },
            "gaslighting_patterns": {
                "description": "Reality distortion and memory manipulation",
                "keywords": [
                    "never happened", "didn't say that", "you're imagining",
                    "you're crazy", "you're being dramatic", "overreacting",
                    "that's not what happened", "you remember wrong"
                ],
                "paraphrased_variants": [
                    "you're making that up", "you're being too sensitive",
                    "you always exaggerate", "you're paranoid",
                    "you have trust issues", "you're unstable"
                ]
            },
            "financial_control": {
                "description": "Economic manipulation and dependency creation",
                "keywords": [
                    "money control", "spending control", "financial control",
                    "hide money", "secret account", "withhold funds",
                    "sabotage work", "quit job", "financial dependency"
                ],
                "paraphrased_variants": [
                    "you can't afford", "you need my money", "I pay for everything",
                    "you'd be nothing without me", "you can't survive alone"
                ]
            },
            "threatening_behavior": {
                "description": "Direct and indirect threats",
                "keywords": [
                    "hurt myself", "kill myself", "end it all", "without you",
                    "if you leave", "consequences", "you'll regret",
                    "threaten", "warning", "or else"
                ],
                "paraphrased_variants": [
                    "you'll be sorry", "you don't know what I'm capable of",
                    "I have nothing to lose", "you made me this way"
                ]
            },
            "guilt_manipulation": {
                "description": "Emotional manipulation through guilt and obligation",
                "keywords": [
                    "after everything", "sacrifice", "ungrateful", "owe me",
                    "poor me", "victim", "suffering", "hurt feelings"
                ],
                "paraphrased_variants": [
                    "how could you do this to me", "I gave you everything",
                    "you're being selfish", "think about what I've done for you"
                ]
            }
        }

    def _initialize_regex_patterns(self) -> Dict[str, List[str]]:
        """Initialize regular expression patterns for complex manipulation detection."""
        return {
            "conditional_threats": [
                r"if you (?:leave|go|don't|won't).*(?:i'll|i will|going to).*(?:hurt|kill|end|destroy)",
                r"unless you.*(?:something bad|consequences|regret|sorry)",
                r"you (?:made|forced) me (?:to|into).*(?:this|hurt|angry)"
            ],
            "blame_shifting": [
                r"(?:you|your) fault.*(?:i|me|my).*(?:had to|forced|made)",
                r"(?:look what|see what) you (?:made|forced) me (?:to )?do",
                r"(?:if you hadn't|if you just).*(?:this wouldn't|i wouldn't)"
            ],
            "minimization": [
                r"(?:not that bad|wasn't that|just|only|barely).*(?:hurt|touched|said)",
                r"you're (?:overreacting|being dramatic|too sensitive) (?:to|about)",
                r"(?:everyone|other people) (?:does|says|thinks) (?:that|this)"
            ],
            "love_bombing": [
                r"(?:i love you|you're perfect|my everything|can't live without).*(?:so much|more than|forever)",
                r"(?:you're the only|no one else|never felt).*(?:one|like this|this way)",
                r"(?:we're|you and i|together).*(?:meant to be|perfect|soulmates)"
            ],
            "control_language": [
                r"you (?:need to|have to|must|should|will).*(?:understand|realize|know|see)",
                r"(?:i know|i understand|i can tell).*(?:what's best|better than|you better)",
                r"(?:let me|i'll|allow me to).*(?:take care|handle|deal with|manage)"
            ]
        }

    def _initialize_semantic_patterns(self) -> Dict[str, List[str]]:
        """Initialize semantic pattern examples for similarity matching."""
        return {
            "dependency_creation": [
                "You can't survive without me",
                "You need me to take care of you",
                "You're helpless on your own",
                "I'm the only one who really understands you"
            ],
            "reality_questioning": [
                "You're imagining things",
                "That never happened",
                "You're being paranoid",
                "You can't trust your own memory"
            ],
            "emotional_blackmail": [
                "If you really loved me you would",
                "You're hurting me by doing this",
                "How can you be so cruel to me",
                "After everything I've done for you"
            ],
            "social_isolation": [
                "Your friends don't really care about you",
                "They're trying to turn you against me",
                "You don't need anyone else but me",
                "They're just jealous of what we have"
            ]
        }

    def analyze_text(self, text: str, source_file: str = "", 
                    context_metadata: Dict[str, Any] = None) -> List[ManipulationInstance]:
        """
        Comprehensive analysis of text for manipulation patterns.
        
        Args:
            text: Text to analyze
            source_file: Source file name
            context_metadata: Additional context (timestamps, participants, etc.)
            
        Returns:
            List of detected manipulation instances
        """
        instances = []
        
        # Preprocess text
        doc = self.nlp(text)
        sentences = [sent.text for sent in doc.sents]
        
        for i, sentence in enumerate(sentences):
            # Keyword pattern matching
            instances.extend(self._detect_keyword_patterns(sentence, source_file, i))
            
            # Regex pattern matching
            instances.extend(self._detect_regex_patterns(sentence, source_file, i))
            
            # Semantic similarity matching
            instances.extend(self._detect_semantic_patterns(sentence, source_file, i))
            
            # Add sentiment and contextual analysis
            for instance in instances[-10:]:  # Process recent instances
                instance.sentiment_score = self._analyze_sentiment(sentence)
                instance.subjectivity_score = self._analyze_subjectivity(sentence)
                instance.context_features = self._extract_context_features(
                    sentence, context_metadata or {}
                )
        
        # Analyze behavioral patterns across instances
        self._analyze_behavioral_patterns(instances, source_file, context_metadata)
        
        return instances

    def _detect_keyword_patterns(self, text: str, source_file: str, 
                                line_num: int) -> List[ManipulationInstance]:
        """Detect manipulation using keyword and phrase patterns."""
        instances = []
        text_lower = text.lower()
        
        for pattern_name, pattern_data in self.keyword_patterns.items():
            # Check main keywords
            for keyword in pattern_data["keywords"]:
                if keyword.lower() in text_lower:
                    confidence = self._calculate_keyword_confidence(keyword, text)
                    instances.append(ManipulationInstance(
                        pattern_type="keyword",
                        pattern_name=pattern_name,
                        text_excerpt=text,
                        confidence_score=confidence,
                        semantic_similarity=0.0,
                        sentiment_score=0.0,
                        subjectivity_score=0.0,
                        context_features={},
                        timestamp=datetime.now().isoformat(),
                        source_file=source_file,
                        line_number=line_num
                    ))
            
            # Check paraphrased variants
            for variant in pattern_data.get("paraphrased_variants", []):
                similarity = self._calculate_semantic_similarity(text, variant)
                if similarity > 0.7:  # High similarity threshold
                    instances.append(ManipulationInstance(
                        pattern_type="paraphrased",
                        pattern_name=pattern_name,
                        text_excerpt=text,
                        confidence_score=similarity,
                        semantic_similarity=similarity,
                        sentiment_score=0.0,
                        subjectivity_score=0.0,
                        context_features={},
                        timestamp=datetime.now().isoformat(),
                        source_file=source_file,
                        line_number=line_num
                    ))
        
        return instances

    def _detect_regex_patterns(self, text: str, source_file: str, 
                              line_num: int) -> List[ManipulationInstance]:
        """Detect manipulation using regular expression patterns."""
        instances = []
        
        for pattern_name, patterns in self.regex_patterns.items():
            for pattern in patterns:
                matches = re.finditer(pattern, text, re.IGNORECASE)
                for match in matches:
                    confidence = 0.8  # High confidence for regex matches
                    instances.append(ManipulationInstance(
                        pattern_type="regex",
                        pattern_name=pattern_name,
                        text_excerpt=text,
                        confidence_score=confidence,
                        semantic_similarity=0.0,
                        sentiment_score=0.0,
                        subjectivity_score=0.0,
                        context_features={"regex_match": match.group()},
                        timestamp=datetime.now().isoformat(),
                        source_file=source_file,
                        line_number=line_num
                    ))
        
        return instances

    def _detect_semantic_patterns(self, text: str, source_file: str, 
                                 line_num: int) -> List[ManipulationInstance]:
        """Detect manipulation using semantic similarity analysis."""
        instances = []
        
        for pattern_name, examples in self.semantic_patterns.items():
            for example in examples:
                similarity = self._calculate_semantic_similarity(text, example)
                if similarity > 0.6:  # Moderate similarity threshold
                    instances.append(ManipulationInstance(
                        pattern_type="semantic",
                        pattern_name=pattern_name,
                        text_excerpt=text,
                        confidence_score=similarity,
                        semantic_similarity=similarity,
                        sentiment_score=0.0,
                        subjectivity_score=0.0,
                        context_features={"matched_example": example},
                        timestamp=datetime.now().isoformat(),
                        source_file=source_file,
                        line_number=line_num
                    ))
        
        return instances

    def _calculate_semantic_similarity(self, text1: str, text2: str) -> float:
        """Calculate semantic similarity between two texts using spaCy."""
        try:
            doc1 = self.nlp(text1)
            doc2 = self.nlp(text2)
            
            # Use spaCy's built-in similarity
            similarity = doc1.similarity(doc2)
            return float(similarity)
        except Exception:
            # Fallback to simple word overlap
            words1 = set(text1.lower().split())
            words2 = set(text2.lower().split())
            overlap = len(words1.intersection(words2))
            union = len(words1.union(words2))
            return overlap / union if union > 0 else 0.0

    def _calculate_keyword_confidence(self, keyword: str, text: str) -> float:
        """Calculate confidence score for keyword matches."""
        text_lower = text.lower()
        keyword_lower = keyword.lower()
        
        # Base confidence for exact match
        confidence = 0.6
        
        # Boost for multiple occurrences
        count = text_lower.count(keyword_lower)
        confidence += min(count * 0.1, 0.3)
        
        # Boost for context words
        context_boost_words = ['always', 'never', 'constantly', 'repeatedly']
        for word in context_boost_words:
            if word in text_lower:
                confidence += 0.1
        
        return min(confidence, 1.0)

    def _analyze_sentiment(self, text: str) -> float:
        """Analyze sentiment of text."""
        if self.sentiment_analyzer:
            try:
                results = self.sentiment_analyzer(text)
                # Find negative sentiment score
                for result in results[0]:
                    if result['label'].lower() in ['negative', 'neg']:
                        return result['score']
                return 0.0
            except Exception:
                pass
        
        # Fallback: simple negative word counting
        negative_words = [
            'hate', 'terrible', 'awful', 'horrible', 'disgusting',
            'stupid', 'worthless', 'pathetic', 'useless', 'failure'
        ]
        text_lower = text.lower()
        negative_count = sum(1 for word in negative_words if word in text_lower)
        return min(negative_count / 10.0, 1.0)

    def _analyze_subjectivity(self, text: str) -> float:
        """Analyze subjectivity/objectivity of text."""
        # Simple subjectivity measure based on personal pronouns and opinion words
        personal_pronouns = ['i', 'you', 'we', 'my', 'your', 'our', 'me', 'us']
        opinion_words = ['think', 'feel', 'believe', 'seem', 'appear', 'probably', 'maybe']
        
        text_lower = text.lower()
        words = text_lower.split()
        
        if not words:
            return 0.0
        
        subjective_count = 0
        for word in words:
            if word in personal_pronouns or word in opinion_words:
                subjective_count += 1
        
        return min(subjective_count / len(words), 1.0)

    def _extract_context_features(self, text: str, 
                                 metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Extract contextual features from text and metadata."""
        features = {
            'text_length': len(text),
            'word_count': len(text.split()),
            'reading_ease': flesch_reading_ease(text) if text.strip() else 0,
            'has_metadata': bool(metadata)
        }
        
        # Add metadata features
        if metadata:
            features.update({
                'timestamp': metadata.get('timestamp'),
                'participant': metadata.get('participant'),
                'communication_type': metadata.get('type', 'unknown')
            })
        
        # Detect urgency indicators
        urgency_words = ['urgent', 'emergency', 'now', 'immediately', 'asap']
        features['urgency_score'] = sum(
            1 for word in urgency_words if word in text.lower()
        ) / len(urgency_words)
        
        # Detect repetition patterns
        words = text.lower().split()
        word_counts = Counter(words)
        features['repetition_score'] = sum(
            count for count in word_counts.values() if count > 1
        ) / len(words) if words else 0
        
        return features

    def _analyze_behavioral_patterns(self, instances: List[ManipulationInstance], 
                                   source_file: str, 
                                   context_metadata: Dict[str, Any]):
        """Analyze behavioral patterns across multiple instances."""
        if not instances:
            return
        
        # Track escalation patterns
        timestamps = []
        confidence_scores = []
        
        for instance in instances:
            try:
                timestamps.append(datetime.fromisoformat(instance.timestamp))
                confidence_scores.append(instance.confidence_score)
            except ValueError:
                continue
        
        if len(timestamps) >= 2:
            # Calculate escalation trend
            if timestamps == sorted(timestamps):  # Chronological order
                escalation_trend = np.corrcoef(range(len(confidence_scores)), confidence_scores)[0, 1]
                for instance in instances:
                    instance.context_features['escalation_trend'] = float(escalation_trend)
        
        # Detect frequency patterns
        pattern_counts = Counter(instance.pattern_name for instance in instances)
        for instance in instances:
            instance.context_features['pattern_frequency'] = pattern_counts[instance.pattern_name]
            instance.context_features['total_patterns_detected'] = len(instances)

    def generate_comprehensive_report(self, instances: List[ManipulationInstance], 
                                    output_file: str = None) -> str:
        """Generate a comprehensive analysis report."""
        report = []
        
        # Header
        report.append("=" * 80)
        report.append("ENHANCED MANIPULATION DETECTION ANALYSIS REPORT")
        report.append("=" * 80)
        report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"Total Instances Detected: {len(instances)}")
        report.append("")
        
        # Summary statistics
        if instances:
            avg_confidence = np.mean([i.confidence_score for i in instances])
            avg_sentiment = np.mean([i.sentiment_score for i in instances])
            avg_semantic = np.mean([i.semantic_similarity for i in instances])
            
            report.append("SUMMARY STATISTICS:")
            report.append("-" * 30)
            report.append(f"Average Confidence Score: {avg_confidence:.3f}")
            report.append(f"Average Sentiment Score: {avg_sentiment:.3f}")
            report.append(f"Average Semantic Similarity: {avg_semantic:.3f}")
            report.append("")
            
            # Pattern type breakdown
            pattern_types = Counter(i.pattern_type for i in instances)
            report.append("DETECTION METHOD BREAKDOWN:")
            report.append("-" * 30)
            for ptype, count in pattern_types.most_common():
                report.append(f"{ptype.title()}: {count} instances")
            report.append("")
            
            # Pattern name breakdown
            pattern_names = Counter(i.pattern_name for i in instances)
            report.append("MANIPULATION PATTERN BREAKDOWN:")
            report.append("-" * 30)
            for pname, count in pattern_names.most_common():
                report.append(f"{pname.replace('_', ' ').title()}: {count} instances")
            report.append("")
        
        # Detailed findings
        report.append("DETAILED FINDINGS:")
        report.append("=" * 50)
        
        # Group by pattern name
        pattern_groups = defaultdict(list)
        for instance in instances:
            pattern_groups[instance.pattern_name].append(instance)
        
        for pattern_name, pattern_instances in pattern_groups.items():
            if not pattern_instances:
                continue
            
            report.append(f"\n{pattern_name.replace('_', ' ').upper()}")
            report.append("-" * len(pattern_name))
            
            for i, instance in enumerate(pattern_instances[:5], 1):  # Show top 5
                report.append(f"\n  Instance {i}:")
                report.append(f"    Method: {instance.pattern_type}")
                report.append(f"    Confidence: {instance.confidence_score:.3f}")
                report.append(f"    Sentiment: {instance.sentiment_score:.3f}")
                report.append(f"    Text: {instance.text_excerpt[:200]}...")
                report.append(f"    Source: {instance.source_file}")
        
        # Recommendations
        report.append("\n\nRECOMMendations FOR DOCUMENTATION:")
        report.append("=" * 50)
        report.append("• Document specific dates, times, and witnesses for each incident")
        report.append("• Track frequency and escalation patterns over time")
        report.append("• Note the function and payoff of manipulative behaviors")
        report.append("• Collect third-party corroboration when possible")
        report.append("• Monitor for retaliation when manipulation tactics are resisted")
        
        if instances:
            high_confidence = [i for i in instances if i.confidence_score > 0.8]
            if high_confidence:
                report.append(f"• Focus on {len(high_confidence)} high-confidence instances for court presentation")
        
        report_text = "\n".join(report)
        
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(report_text)
            print(f"Comprehensive report saved to: {output_file}")
        
        return report_text

    def export_to_json(self, instances: List[ManipulationInstance], 
                      output_file: str) -> None:
        """Export instances to JSON format for further analysis."""
        data = {
            "metadata": {
                "tool_version": "2.0.0",
                "generation_timestamp": datetime.now().isoformat(),
                "total_instances": len(instances),
                "analysis_capabilities": [
                    "keyword_matching",
                    "regex_patterns", 
                    "semantic_similarity",
                    "sentiment_analysis",
                    "contextual_features",
                    "behavioral_patterns"
                ]
            },
            "instances": [asdict(instance) for instance in instances]
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        print(f"JSON export saved to: {output_file}")


def main():
    """Demo and testing function."""
    detector = EnhancedManipulationDetector()
    
    # Test texts demonstrating various manipulation patterns
    test_texts = [
        "You're overreacting as usual. This never happened the way you remember it.",
        "If you leave me, I'll hurt myself and it will be your fault.",
        "You can't survive without me. You need me to take care of everything.",
        "Your friends are just trying to turn you against me because they're jealous.",
        "After everything I've done for you, how can you be so ungrateful?",
        "You made me angry, so I had to yell at you. It's not my fault.",
        "I love you more than anything. You're my whole world and I can't live without you."
    ]
    
    print("Testing Enhanced Manipulation Detector...")
    all_instances = []
    
    for i, text in enumerate(test_texts):
        print(f"\nAnalyzing text {i+1}: {text[:50]}...")
        instances = detector.analyze_text(text, f"test_text_{i+1}.txt")
        all_instances.extend(instances)
        print(f"  Detected {len(instances)} manipulation patterns")
    
    # Generate reports
    print(f"\nTotal instances detected: {len(all_instances)}")
    
    # Create reports directory
    reports_dir = "manipulation_analysis_reports"
    os.makedirs(reports_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Generate comprehensive report
    report_file = os.path.join(reports_dir, f"manipulation_analysis_{timestamp}.txt")
    report = detector.generate_comprehensive_report(all_instances, report_file)
    
    # Export to JSON
    json_file = os.path.join(reports_dir, f"manipulation_data_{timestamp}.json")
    detector.export_to_json(all_instances, json_file)
    
    print(f"\nReports generated in: {reports_dir}/")
    print("\nSample findings:")
    for instance in all_instances[:3]:
        print(f"  • {instance.pattern_name}: {instance.confidence_score:.3f} confidence")


if __name__ == "__main__":
    main()