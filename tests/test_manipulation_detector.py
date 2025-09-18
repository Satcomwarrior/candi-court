from manipulation_detector import EnhancedManipulationDetector


def test_keyword_detection():
    detector = EnhancedManipulationDetector()
    text = "You're being dramatic."
    instances = detector.analyze_text(text, source_file="test")
    names = [inst.pattern_name for inst in instances]
    assert "gaslighting_patterns" in names


def test_regex_detection():
    detector = EnhancedManipulationDetector()
    text = "If you leave I'll hurt you."
    instances = detector.analyze_text(text, source_file="test")
    names = [inst.pattern_name for inst in instances]
    assert "conditional_threats" in names


def test_semantic_detection():
    detector = EnhancedManipulationDetector()
    text = "You don't need anyone else but me."
    instances = detector.analyze_text(text, source_file="test")
    names = [inst.pattern_name for inst in instances]
    assert "social_isolation" in names
