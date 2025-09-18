"""Pattern definitions for manipulation detection."""
from typing import Dict, List

KEYWORD_PATTERNS: Dict[str, Dict[str, List[str]]] = {
    "isolation_tactics": {
        "description": "Attempts to isolate victim from support networks",
        "keywords": [
            "isolate", "isolation", "cut off contact", "block contact",
            "restrict access", "limit contact", "forbid seeing",
            "tracking", "monitoring", "checking up", "surveillance", "watching",
            "following", "stalking", "keeping tabs", "spying on",
            "need permission", "ask permission", "not allowed", "can't see",
            "forbidden to", "must ask", "have to check"
        ],
        "paraphrased_variants": [
            "keeping you away from", "making sure you don't talk to",
            "I don't want you seeing", "you shouldn't be around",
            "they're not good for you", "influencing you against me"
        ],
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
        ],
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
        ],
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
        ],
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
        ],
    },
}

REGEX_PATTERNS: Dict[str, List[str]] = {
    "conditional_threats": [
        r"if you (?:leave|go|don't|won't).*(?:i'll|i will|going to).*(?:hurt|kill|end|destroy)",
        r"unless you.*(?:something bad|consequences|regret|sorry)",
        r"you (?:made|forced) me (?:to|into).*(?:this|hurt|angry)",
    ],
    "blame_shifting": [
        r"(?:you|your) fault.*(?:i|me|my).*(?:had to|forced|made)",
        r"(?:look what|see what) you (?:made|forced) me (?:to )?do",
        r"(?:if you hadn't|if you just).*(?:this wouldn't|i wouldn't)",
    ],
    "minimization": [
        r"(?:not that bad|wasn't that|just|only|barely).*(?:hurt|touched|said)",
        r"you're (?:overreacting|being dramatic|too sensitive) (?:to|about)",
        r"(?:everyone|other people) (?:does|says|thinks) (?:that|this)",
    ],
}

SEMANTIC_PATTERNS: Dict[str, List[str]] = {
    "dependency_creation": [
        "You can't survive without me",
        "You need me to take care of you",
        "You're helpless on your own",
        "I'm the only one who really understands you",
    ],
    "reality_questioning": [
        "You're imagining things",
        "That never happened",
        "You're being paranoid",
        "You can't trust your own memory",
    ],
    "emotional_blackmail": [
        "If you really loved me you would",
        "You're hurting me by doing this",
        "How can you be so cruel to me",
        "After everything I've done for you",
    ],
    "social_isolation": [
        "Your friends don't really care about you",
        "They're trying to turn you against me",
        "You don't need anyone else but me",
        "They're just jealous of what we have",
    ],
}
