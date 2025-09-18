from dataclasses import dataclass, asdict
from typing import Any, Dict, Optional

@dataclass
class ManipulationInstance:
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

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
