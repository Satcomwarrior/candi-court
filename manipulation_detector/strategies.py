"""Detection strategy classes."""
from __future__ import annotations
import re
from datetime import datetime
from typing import List

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from .models import ManipulationInstance

class KeywordDetector:
    def __init__(self, patterns):
        self.patterns = patterns

    def detect(self, text: str, source_file: str, line_num: int | None) -> List[ManipulationInstance]:
        results: List[ManipulationInstance] = []
        lowered = text.lower()
        for name, info in self.patterns.items():
            keywords = info.get("keywords", []) + info.get("paraphrased_variants", [])
            for kw in keywords:
                if kw.lower() in lowered:
                    results.append(
                        ManipulationInstance(
                            pattern_type="keyword",
                            pattern_name=name,
                            text_excerpt=text,
                            confidence_score=1.0,
                            semantic_similarity=1.0,
                            sentiment_score=0.0,
                            subjectivity_score=0.0,
                            context_features={},
                            timestamp=datetime.utcnow().isoformat(),
                            source_file=source_file,
                            line_number=line_num,
                        )
                    )
                    break
        return results

class RegexDetector:
    def __init__(self, patterns):
        self.patterns = {name: [re.compile(p, re.I) for p in pats] for name, pats in patterns.items()}

    def detect(self, text: str, source_file: str, line_num: int | None) -> List[ManipulationInstance]:
        results: List[ManipulationInstance] = []
        for name, pats in self.patterns.items():
            for pat in pats:
                if pat.search(text):
                    results.append(
                        ManipulationInstance(
                            pattern_type="regex",
                            pattern_name=name,
                            text_excerpt=text,
                            confidence_score=1.0,
                            semantic_similarity=1.0,
                            sentiment_score=0.0,
                            subjectivity_score=0.0,
                            context_features={},
                            timestamp=datetime.utcnow().isoformat(),
                            source_file=source_file,
                            line_number=line_num,
                        )
                    )
                    break
        return results

class SemanticDetector:
    def __init__(self, patterns, vectorizer: TfidfVectorizer | None = None, threshold: float = 0.3):
        self.threshold = threshold
        self.vectorizer = vectorizer or TfidfVectorizer()
        corpus = []
        self.labels = []
        for name, examples in patterns.items():
            corpus.extend(examples)
            self.labels.extend([name] * len(examples))
        if corpus:
            self.matrix = self.vectorizer.fit_transform(corpus)
        else:
            self.matrix = None

    def detect(self, text: str, source_file: str, line_num: int | None) -> List[ManipulationInstance]:
        if self.matrix is None:
            return []
        vec = self.vectorizer.transform([text])
        sims = cosine_similarity(vec, self.matrix)[0]
        idx = sims.argmax()
        if sims[idx] < self.threshold:
            return []
        name = self.labels[idx]
        return [
            ManipulationInstance(
                pattern_type="semantic",
                pattern_name=name,
                text_excerpt=text,
                confidence_score=float(sims[idx]),
                semantic_similarity=float(sims[idx]),
                sentiment_score=0.0,
                subjectivity_score=0.0,
                context_features={},
                timestamp=datetime.utcnow().isoformat(),
                source_file=source_file,
                line_number=line_num,
            )
        ]
