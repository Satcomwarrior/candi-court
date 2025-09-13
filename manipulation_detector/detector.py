"""Enhanced manipulation detector built from modular strategies."""
from __future__ import annotations
from typing import List, Optional

from .models import ManipulationInstance
from .patterns import KEYWORD_PATTERNS, REGEX_PATTERNS, SEMANTIC_PATTERNS
from .strategies import KeywordDetector, RegexDetector, SemanticDetector

class EnhancedManipulationDetector:
    def __init__(self, *,
                 keyword_patterns=None,
                 regex_patterns=None,
                 semantic_patterns=None,
                 nlp=None,
                 sentiment_analyzer=None):
        """Create detector with optional dependency injection."""
        self.keyword_detector = KeywordDetector(keyword_patterns or KEYWORD_PATTERNS)
        self.regex_detector = RegexDetector(regex_patterns or REGEX_PATTERNS)
        self.semantic_detector = SemanticDetector(semantic_patterns or SEMANTIC_PATTERNS)
        self.nlp = nlp
        self.sentiment_analyzer = sentiment_analyzer

    def analyze_text(self, text: str, source_file: str = "") -> List[ManipulationInstance]:
        """Run all detection strategies against given text."""
        instances: List[ManipulationInstance] = []
        lines = text.splitlines() or [text]
        for i, line in enumerate(lines, start=1):
            instances.extend(self.keyword_detector.detect(line, source_file, i))
            instances.extend(self.regex_detector.detect(line, source_file, i))
            instances.extend(self.semantic_detector.detect(line, source_file, i))
        return instances
