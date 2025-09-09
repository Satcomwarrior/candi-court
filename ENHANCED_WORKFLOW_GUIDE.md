# Enhanced Legal Case Workflow - Usage Guide

## Overview

The enhanced legal case workflow system now includes advanced NLP analysis, official template integration, and document pattern recognition specifically designed for family law cases involving domestic violence, coercive control, and committed intimate relationship disputes.

## Key Features

### 1. Advanced NLP Communication Analysis
- **Sentiment Analysis**: Uses TextBlob to analyze emotional tone and objectivity
- **Coercive Control Detection**: Identifies 4 categories of controlling behavior:
  - Control patterns (demands, restrictions, commands)
  - Isolation tactics (alienation from support systems)
  - Intimidation (threats, consequences, power displays) 
  - Gaslighting (reality distortion, minimization)
- **Psychological Indicators**: Detects manipulation tactics:
  - Victim blaming language
  - Emotional manipulation
  - Minimization techniques
- **Legal Relevance**: Provides RCW 7.105.010 compliance analysis

### 2. Official Template Integration
- Downloads comprehensive WA court forms for family law cases
- Includes DVPO, AHPO, contempt, CIR, and property dispute forms
- Automatic template selection based on case type
- Enhanced form completion with placeholder replacement

### 3. Document Pattern Analysis
- **Structure Analysis**: Evaluates document organization and formatting
- **Legal Effectiveness**: Assesses persuasive elements and authority citations
- **Court Compliance**: Checks for required elements and proper formatting
- **Pattern Recognition**: Identifies successful language patterns across documents

## Installation and Setup

```bash
# Install required dependencies
pip install spacy textblob python-docx requests

# Download spaCy language model
python -m spacy download en_core_web_sm
```

## Usage Examples

### 1. Basic Enhanced Workflow
```bash
python legal_case_workflow.py
```

This runs the complete enhanced workflow including:
- Template download and selection
- NLP communication analysis
- Document generation with official forms
- Structure and compliance analysis

### 2. Download Official Templates
```bash
python download_family_law_forms.py
```

Downloads comprehensive WA court forms to `templates/family_law_forms/`

### 3. Analyze Document Patterns
```bash
python document_pattern_analyzer.py
```

Analyzes all documents in the repository for patterns and effectiveness

### 4. Test and Demonstration
```bash
python test_enhanced_workflow.py
```

Runs comprehensive tests showing all enhanced capabilities

## NLP Analysis Results

The system can detect and analyze:

### Coercive Control Patterns
- **Control**: Direct commands, restrictions on behavior
- **Isolation**: Alienation from family/friends, cutting off support
- **Intimidation**: Threats, consequences, displays of power
- **Gaslighting**: Reality distortion, "you're imagining things"

### Psychological Manipulation
- **Victim Blaming**: "You made me do this", "It's your fault"
- **Emotional Manipulation**: "I'm disappointed", "You don't care"
- **Minimization**: "It's not that bad", "You're overreacting"

### Example Output
```
Sentiment Analysis:
  - Polarity: -0.039 (negative)
  - Subjectivity: 0.717 (subjective)
  - Interpretation: neutral sentiment, subjective tone

Coercive Control Patterns Detected: 2
  - Control: 1 instances
  - Gaslighting: 2 instances

Psychological Indicators: 1
  - Victim Blaming: 1 occurrences
```

## Template Integration

### Available Forms
- **Protection Orders**: DVPO 001-005, AHPO 001-015
- **Contempt Motions**: Forms 151, 152, 161
- **Property Disputes**: Forms 171, 172, 181
- **CIR Forms**: Parentage 401, 402
- **Service Forms**: Proof of service, mailing

### Template Selection
The system automatically selects appropriate templates based on:
- Case type (protection order, contempt, property)
- Document purpose (petition, motion, declaration)
- Court requirements (Snohomish County specifics)

## Document Analysis Features

### Structure Assessment (0-100 score)
- Paragraph organization and length
- Heading structure and hierarchy
- Overall document balance

### Legal Effectiveness (0-100 score)
- Persuasive language elements
- Authority citations (RCW, case law)
- Factual assertions vs legal conclusions

### Court Compliance (0-100 score)
- Required elements present
- Proper formatting and styling
- Snohomish County specific requirements

## Integration with Existing Workflow

The enhanced system maintains compatibility with the existing workflow while adding:

1. **Pre-processing**: Template download and analysis
2. **Enhanced Analysis**: NLP + AI analysis combination
3. **Quality Assessment**: Document scoring and recommendations
4. **Compliance Checking**: Court rule validation

## Legal Applications

### Domestic Violence Cases
- Coercive control pattern documentation
- Evidence compilation and analysis
- Protection order preparation

### Family Law Disputes
- Communication pattern analysis
- Property dispute documentation
- CIR establishment support

### Contempt Proceedings
- Violation pattern identification
- Evidence organization
- Motion preparation

## Best Practices

1. **Use Official Templates**: Always prefer WA court forms when available
2. **Document Patterns**: Maintain detailed records of communication analysis
3. **Regular Updates**: Refresh templates periodically for latest versions
4. **Multiple Analysis**: Combine NLP with AI analysis for comprehensive results
5. **Compliance Focus**: Prioritize court compliance scoring for successful filings

## Troubleshooting

### Common Issues
- **Template Download Failures**: Check internet connectivity, use cached forms
- **NLP Model Missing**: Run `python -m spacy download en_core_web_sm`
- **Document Analysis Errors**: Ensure proper .docx format

### Performance Optimization
- Pre-download templates for offline use
- Cache NLP analysis results for repeated communications
- Use document templates to improve compliance scores

## Legal Disclaimer

This system is designed to assist with legal document preparation and analysis. It does not constitute legal advice and should be used in conjunction with qualified legal counsel, especially for complex domestic violence and family law matters.

## Support and Updates

The system is designed for continuous improvement. Pattern analysis helps identify successful legal strategies and language that can be incorporated into future documents and templates.