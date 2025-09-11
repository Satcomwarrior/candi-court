# Google AI Studio Integration Guide

## Overview

This repository now includes a properly configured `call_studio_ai` function that integrates with Google AI Studio (aistudio.google.com) using the Gemini API. The integration allows the legal case workflow to leverage AI for document analysis, communications review, and case fact summarization.

## Configuration

### API Endpoint and Model
- **Endpoint**: `https://generativelanguage.googleapis.com/v1beta`
- **Model**: `gemini-1.5-pro-latest`

These are configured as constants in `ai_studio_code.py`:
```python
STUDIO_AI_ENDPOINT = "https://generativelanguage.googleapis.com/v1beta"
STUDIO_AI_MODEL = "gemini-1.5-pro-latest"
```

### API Key Setup

To use the Studio.ai integration, you need to set up your Google AI API key:

1. Visit [Google AI Studio](https://aistudio.google.com)
2. Create an API key
3. Set it as an environment variable:
   ```bash
   export GEMINI_API_KEY="your_api_key_here"
   ```

Or add it to your `.env` file:
```
GEMINI_API_KEY=your_api_key_here
```

## Function Usage

### Basic Usage

```python
from ai_studio_code import call_studio_ai

# Simple text analysis
response = call_studio_ai("Analyze this legal document for key points.")

# Analysis with files
response = call_studio_ai(
    "Extract metadata from these documents", 
    files=["case_folder/exhibits/document.pdf"]
)

# Custom model
response = call_studio_ai(
    "Summarize this case", 
    model_name="gemini-1.5-pro-latest"
)
```

### Supported File Types

The `call_studio_ai` function supports:
- **PDF files**: Automatically encoded and sent to the API
- **Text files (.txt, .md)**: Content is read and included in the prompt
- **Any file path**: Function will attempt to process based on extension

## Integration Points

### Legal Case Workflow

The function is integrated into `legal_case_workflow.py` in several places:

1. **Communications Analysis**: `analyze_communications_via_ai()`
2. **Case Facts Summarization**: `summarize_case_facts()`
3. **Legal Arguments Generation**: `generate_legal_arguments()`
4. **Document Metadata Extraction**: `ai_studio_extract_metadata()`

### Fallback Behavior

All integration points include graceful fallback to simulated responses when:
- API key is not configured
- Network issues occur
- API rate limits are hit
- Any other errors occur

This ensures the workflow continues to function for demonstration and testing purposes.

## PDF Exhibits Directory

### Directory Structure
```
case_folder/
└── exhibits/
    ├── README.md
    └── [your_pdf_files.pdf]
```

### Usage
1. Place your PDF legal documents in `case_folder/exhibits/`
2. The AI functions will automatically process these files when analyzing cases
3. Supported formats: PDF, TXT, MD

### Example
```python
# Process all PDFs in exhibits folder
import os
exhibits_dir = "case_folder/exhibits"
pdf_files = [f for f in os.listdir(exhibits_dir) if f.endswith('.pdf')]
file_paths = [os.path.join(exhibits_dir, f) for f in pdf_files]

response = call_studio_ai(
    "Analyze these legal exhibits and provide a comprehensive summary",
    files=file_paths
)
```

## Testing

Run the test suite to verify the integration:

```bash
python test_studio_ai.py
```

This will test:
1. Basic API configuration and connectivity
2. File processing capabilities
3. Integration with legal workflow functions

## Error Handling

The integration includes comprehensive error handling:

- **Missing API Key**: Graceful fallback to simulated responses
- **Network Errors**: Retry logic and fallback responses
- **File Processing Errors**: Individual file error handling
- **API Rate Limiting**: Proper error messages and fallback

## Examples

### Legal Document Analysis
```python
# Analyze a complex legal document
prompt = """
Analyze this legal document for:
1. Key dates and deadlines
2. Party names and relationships  
3. Financial amounts and obligations
4. Legal issues and claims
5. Requested relief
"""

response = call_studio_ai(prompt, files=["case_folder/exhibits/motion.pdf"])
```

### Communications Pattern Analysis
```python
# Analyze communication patterns
text = "Historical text messages showing escalation patterns..."
analysis = call_studio_ai(f"""
Analyze these communications for evidence of:
- Coercive control patterns
- Escalation indicators
- Manipulation tactics
- Threats or intimidation
- Timeline of events

Communications: {text}
""")
```

### Case Strategy Development
```python
# Generate legal strategy
facts = "Documented case facts and evidence..."
strategy = call_studio_ai(f"""
Based on these facts, develop a legal strategy including:
- Strongest legal arguments
- Supporting evidence priorities  
- Potential weaknesses to address
- Recommended next steps

Case Facts: {facts}
""")
```

## Dependencies

Required packages (see `requirements.txt`):
```
python-docx==0.8.11
google-genai>=1.33.0
```

Install with:
```bash
pip install -r requirements.txt
```

## Security Notes

- API keys are loaded from environment variables only
- No API keys are stored in code or configuration files
- All communication with Google AI Studio uses HTTPS
- Local file processing only - no files uploaded to external services without explicit user action

## Troubleshooting

### Common Issues

1. **"Module not found: google"**
   ```bash
   pip install google-genai
   ```

2. **"GEMINI_API_KEY not set"**
   - Set the environment variable with your API key
   - Check that `.env` file is properly formatted

3. **"No response generated"**
   - Check API key validity
   - Verify network connectivity
   - Check API quota/billing status

4. **File processing errors**
   - Ensure files exist and are readable
   - Check file formats are supported
   - Verify file sizes are within API limits

### Debug Mode

Enable detailed error logging by setting:
```bash
export DEBUG_AI_STUDIO=1
```

This will provide additional debug information about API calls and file processing.