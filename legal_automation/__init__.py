"""
legal_automation package

Re-exports core tools so callers can import from one place:

from legal_automation import (
    LegalDocumentAnalyzer,
    WashingtonFormsDownloader,
    get_available_templates,
    analyze_communication_patterns_nlp,
    analyze_document_structure,
    analyze_communications_via_ai,
    generate_legal_document,
    ReasonablenessAnalyzer,
    analyze_text,
)
"""

from .document_pattern_analyzer import LegalDocumentAnalyzer  # type: ignore
from .download_family_law_forms import (  # type: ignore
    WashingtonFormsDownloader,
    get_available_templates,
)
from .legal_case_workflow import (  # type: ignore
    analyze_communication_patterns_nlp,
    analyze_document_structure,
    analyze_communications_via_ai,
    generate_legal_document,
)
from .reasonableness_analyzer import ReasonablenessAnalyzer, analyze_text  # type: ignore

