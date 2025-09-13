PowerShell Automations

This folder centralizes the external PowerShell orchestrators and helper scripts used alongside the Python tools.

Scripts
- RUN_UNIFIED_NOW.ps1: Minimal unified runner that sequences ingestion, analysis, and reporting steps.
- UNIFIED_LEGAL_AUTOMATION.ps1: Larger end-to-end workflow (evidence, coercive-control, financial, report, optional GitHub sync).
- EXECUTE_LEGAL_STRATEGY.ps1: Strategy execution orchestrator.
- ENHANCED_INGEST.ps1: Ingestion pipeline (zips, SMS, large text; optional OCR).
- ENHANCED_AUDIO_EVIDENCE_PROCESSOR.ps1: Audio evidence processing helpers.
- ocr_screen_recordings.ps1: OCR pass on screen recording assets.
- evidence_analysis_automation.ps1: Evidence analysis automation.
- generate_defense_exhibits.ps1, generate_defense_excerpts.ps1, export_exhibit_list_csv.ps1, compile_defense_notes.ps1: Evidence/defense helpers.
- DEFENSE_ONE_CLICK.ps1, GENERATE_DEFENSE_ONLY_REPORT.ps1, APPLY_REDACTIONS.ps1: Report/refinement utilities.

Usage
- Run directly in PowerShell:
  powershell -NoProfile -ExecutionPolicy Bypass -File powershell\RUN_UNIFIED_NOW.ps1

- From the Python unified runner:
  python run_all.py powershell RUN_UNIFIED_NOW.ps1 -- -EnableOCR
  python run_all.py powershell UNIFIED_LEGAL_AUTOMATION.ps1 -- -IncludeCoerciveControl -FullAnalysis

Notes
- Scripts expect environment variables and .env-managed secrets for API keys when applicable.
- This import is non-destructive; the original files remain in your Downloads. The repo copies are now the maintained versions.

