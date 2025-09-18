"""
FULL AUTOMATED LEGAL CASE WORKFLOW SCRIPT

Author: William Miller
Date: 09/07/2025
Version: 1.0

Enhanced with NLP analysis and official template integration.
"""
import os
import json
from typing import List, Dict, Any
from docx import Document
# Optional NLP imports
try:
    import spacy  # type: ignore
    _NLP = None
    try:
        _NLP = spacy.load("en_core_web_sm")
        print("[NLP] spaCy model loaded successfully")
    except Exception:
        print("[NLP] spaCy model not found. Run: python -m spacy download en_core_web_sm")
except Exception:
    spacy = None  # type: ignore
    _NLP = None
try:
    from textblob import TextBlob  # type: ignore
except Exception:
    TextBlob = None  # type: ignore
# === STEP 1: DOCUMENT GENERATION ===
def generate_legal_document(template_path: str, case_data: Dict[str, Any], output_path: str) -> str:
    """Generate a legal document from a Word template by replacing placeholders."""
    doc = Document(template_path)
    for para in doc.paragraphs:
        for key, value in case_data.items():
            placeholder = f"{{{{{key}}}}}"
            if placeholder in para.text:
                para.text = para.text.replace(placeholder, str(value))
    doc.save(output_path)
    print(f"[INFO] Generated legal document saved at {output_path}")
    return output_path
# === STEP 2: ENHANCED COMMUNICATIONS ANALYSIS (AI) ===
def analyze_communications_via_ai(text: str) -> str:
    """Enhanced analysis using Google AI Studio if available, with safe fallback."""
    prompt = (
        "Analyze the following communications for coercive control, manipulation, and perceived "
        "burdensomeness patterns, then summarize legal relevance for family law matters.\n\n" + text
    )
    print("[AI] Sending communication analysis prompt to Google AI Studio...")
    try:
        from ai_studio_code import call_studio_ai  # type: ignore
        return call_studio_ai(prompt)
    except Exception as e:
        print(f"[AI] Error calling Google AI Studio: {e}")
        return (
            "[AI Fallback] Possible coercive control language identified. Consider documenting instances, "
            "obtaining corroboration, and preparing exhibits for court review."
        )
# === NLP utilities (for tests and offline analysis) ===
def analyze_communication_patterns_nlp(text: str) -> Dict[str, Any]:
    """Pure-NLP analysis of communications for tests and offline use.
    Returns a dict with keys: sentiment, coercive_patterns, psychological_indicators,
    linguistic_patterns, entities, summary.
    """
    result: Dict[str, Any] = {
        "sentiment": {},
        "coercive_patterns": [],
        "psychological_indicators": [],
        "linguistic_patterns": {},
        "entities": [],
        "summary": "",
    }
    # Sentiment via TextBlob if available
    if TextBlob is not None:
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        subjectivity = blob.sentiment.subjectivity
        interp = "neutral"
        if polarity > 0.1:
            interp = "positive"
        elif polarity < -0.1:
            interp = "negative"
        tone = "objective" if subjectivity < 0.5 else "subjective"
        result["sentiment"] = {
            "polarity": float(polarity),
            "subjectivity": float(subjectivity),
            "interpretation": f"{interp} sentiment, {tone} tone",
        }
    else:
        result["sentiment"] = {
            "polarity": 0.0,
            "subjectivity": 0.0,
            "interpretation": "neutral sentiment, objective tone",
        }
    # spaCy-based analysis if model available
    doc = _NLP(text) if _NLP else None
    # Entities
    if doc is not None:
        entities: List[Dict[str, str]] = []
        for ent in doc.ents:
            try:
                desc = spacy.explain(ent.label_) or ""
            except Exception:
                desc = ""
            entities.append({"text": ent.text, "label": ent.label_, "description": desc})
        result["entities"] = entities
    else:
        result["entities"] = []
    # Linguistic patterns and coercive pattern detection
    text_lower = text.lower()
    patterns = {
        "imperative_sentences": text_lower.count(" you must ") + text_lower.count(" you should "),
        "question_frequency": text.count("?"),
        "personal_pronouns": {"first": 0, "second": 0, "third": 0},
        "modal_verbs": 0,
        "negative_words": 0,
    }
    if doc is not None:
        for token in doc:
            if token.tag_ == "MD":
                patterns["modal_verbs"] += 1
            if token.tag_ in ("PRP", "PRP$"):
                l = token.text.lower()
                if l in ("i", "me", "my", "mine"):
                    patterns["personal_pronouns"]["first"] += 1
                elif l in ("you", "your", "yours"):
                    patterns["personal_pronouns"]["second"] += 1
                else:
                    patterns["personal_pronouns"]["third"] += 1
            # BUG FIX: Replace token.sentiment with TextBlob sentiment analysis
            # spaCy tokens don't have sentiment attribute, use TextBlob instead
            try:
                # Remove the problematic token.sentiment code
                # Use TextBlob for negative word detection instead
                if TextBlob is not None:
                    token_blob = TextBlob(token.text)
                    if token_blob.sentiment.polarity < -0.1:
                        patterns["negative_words"] += 1
            except Exception:
                pass
    result["linguistic_patterns"] = patterns
    categories = [
        ("control", [
            "you can't", "you won't", "you're not allowed", "i forbid",
            "you better not", "need permission", "ask me first",
        ]),
        ("isolation", [
            "nobody likes you", "your friends don't care", "family doesn't want",
            "you have no one", "i'm all you have", "turn against",
        ]),
        ("intimidation", [
            "you'll regret", "you'll pay", "consequences", "don't make me",
        ]),
        ("gaslighting", [
            "you're crazy", "you're imagining", "that never happened",
            "you're overreacting", "too sensitive", "you're dramatic",
        ]),
    ]
    detected: List[Dict[str, Any]] = []
    for cat, phrases in categories:
        found = [p for p in phrases if p in text_lower]
        if found:
            detected.append({"category": cat, "phrases": found, "severity": len(found)})
    result["coercive_patterns"] = detected
    # Psychological indicators (simple heuristics)
    indicators: List[Dict[str, Any]] = []
    heuristics = {
        "threats_self_harm": ["hurt myself", "kill myself", "end it all"],
        "blame_shifting": ["you made me", "your fault", "forced me"],
        "minimization": ["not that bad", " just ", " only ", "overreacting", "too sensitive"],
    }
    for name, keys in heuristics.items():
        count = sum(text_lower.count(k) for k in keys)
        if count:
            indicators.append({"type": name, "count": count})
    result["psychological_indicators"] = indicators
    # Summary
    parts: List[str] = []
    if detected:
        parts.append("coercive control language present")
    if any(i["count"] > 0 for i in indicators):
        parts.append("psychological manipulation cues detected")
    if not parts:
        parts.append("no strong coercive indicators detected")
    result["summary"] = "; ".join(parts)
    return result
def analyze_document_structure(doc_path: str) -> Dict[str, Any]:
    """Wrapper to analyze document structure using LegalDocumentAnalyzer.
    Returns only the structure portion for convenience.
    """
    try:
        from document_pattern_analyzer import LegalDocumentAnalyzer  # type: ignore
        analyzer = LegalDocumentAnalyzer()
        analysis = analyzer.analyze_document_file(doc_path)
        return analysis["structure_analysis"] if analysis else {}
    except Exception as e:
        print(f"[WARN] analyze_document_structure failed: {e}")
        return {}
