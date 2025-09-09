# Coercive Control Patterns Documentation Tool

A specialized tool for documenting and analyzing coercive control patterns and emotional manipulation tactics in legal and personal documents. This tool is designed to create structured documentation for mental health professionals and legal proceedings.

## Overview

This tool scans documents for evidence of coercive control behaviors, which can be crucial in demonstrating a sustained course of conduct rather than isolated events. It identifies 14 distinct pattern categories and generates comprehensive reports suitable for professional review.

## Pattern Categories Detected

The tool identifies the following coercive control patterns:

### 1. Isolation and Monitoring
- Restricting contact with others
- Tracking devices and excessive check-ins
- Password control and blocking access
- Limiting transportation and finances to restrict autonomy

### 2. Rule-Making and Enforcement
- Imposing arbitrary rules and shifting expectations
- Punishing deviations with silent treatment, rage, or threats
- Creating compliance through fear and control

### 3. Minimizing, Denying, Blaming
- Flipping the script and reframing concerns as "overreactions"
- Claiming the victim "made" them act in certain ways
- Denying obvious facts or rewriting history

### 4. Financial Control
- Withholding funds and dictating spending
- Sabotaging work or creating financial dependency
- Using economic leverage for control

### 5. Emotional Blackmail and Manipulation
- **Self-harm threats**: "If you leave, I'll hurt myself"
- **Guilt, fear, obligation cycles**: Using pity, tears, or staged victimhood
- Making the partner responsible for their emotional survival

### 6. Gaslighting and Reality Distortion
- Denying obvious facts and manufacturing confusion
- Making targets doubt their own judgment and memory
- Systematic reality distortion

### 7. Weaponized Incompetence
- Performing tasks poorly to force partner responsibility
- Using created imbalances to control outcomes
- Strategic helplessness

### 8. Credibility Attacks and Legal Misuse
- Exaggerating mental health issues to depict "instability"
- Misrepresenting fitness, especially in custody proceedings
- Character assassination tactics

### 9. Third-Party Enlistment
- Recruiting friends, family, or professionals to validate narratives
- Creating isolation and pressure through others
- "Flying monkey" tactics

### 10. Procedural Coercion
- Filing serial complaints and exploiting court processes
- Tactical "concern" requests for surveillance rather than protection
- Abuse of legal systems

### 11. Seduction-to-Control Escalation
- Love-bombing that evolves into surveillance and control
- High-intensity care that becomes dependency
- Decision-seizing and curtailed freedom

### 12. Jealousy Reframed as Care
- "I'm just worried" becoming constant checking
- Dictating clothing and escorting to limit independence
- Possessive control disguised as protection

### 13. Communication Red Flags
- Punisher, self-punisher, sufferer, tantalizer patterns
- Chronic ambiguity and moving goalposts
- Conditional love/approval contingent on obedience

### 14. Pattern Markers
- Frequency and timing analysis
- Function and payoff documentation
- Generalization across contexts

## Installation

1. Ensure Python 3.7+ is installed
2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Basic Usage
```bash
python coercive_control_documentation.py [directory_path]
```

If no directory is specified, the tool will scan the current directory.

### Example Usage
```bash
# Scan current directory
python coercive_control_documentation.py

# Scan specific directory
python coercive_control_documentation.py /path/to/documents

# Scan specific legal case folder
python coercive_control_documentation.py ./case_documents
```

## Supported File Types

- **Word Documents (.docx)**: Full text extraction and analysis
- **Text Files (.txt)**: Direct content analysis
- **Markdown Files (.md)**: Text content analysis

## Output Reports

The tool generates two types of reports in the `coercive_control_reports/` directory:

### 1. Checklist Report (.txt)
- Structured documentation for mental health professionals
- Pattern detection summary with checkboxes
- Detailed findings with context and timestamps
- Documentation tracking template
- Pattern markers guidance

### 2. JSON Data Report (.json)
- Machine-readable format for programmatic analysis
- Complete pattern definitions and findings
- Metadata and recommendations
- Suitable for integration with other tools

## Report Features

### Documentation Tracking Template
Each report includes a template for tracking additional information:
- [ ] Pattern: ________________________
- [ ] Date/Time: ______________________
- [ ] Witnesses: ______________________
- [ ] Outcome/Response: ________________
- [ ] Frequency: ______________________
- [ ] Function/Payoff: _________________
- [ ] Third-party Corroboration: _______

### Pattern Markers Guidance
The tool provides guidance on documenting:
- **Frequency and timing**: Crises at key decision points
- **Function and payoff**: Behaviors that secure control outcomes
- **Generalization**: Tactics across contexts that escalate when resisted
- **Third-party corroboration**: Professional records for objective anchoring

## Legal and Professional Use

This tool is designed to assist in:
- Mental health professional assessments
- Legal documentation for court proceedings
- Pattern recognition for safety planning
- Evidence compilation for protection orders
- Custody evaluation support

## Important Notes

### Professional Use Only
This tool is intended for use by:
- Mental health professionals
- Legal professionals
- Domestic violence advocates
- Court personnel
- Licensed counselors and therapists

### Documentation Best Practices
- Pair findings with third-party corroboration
- Document dates, times, and witnesses
- Track frequency and timing patterns
- Note escalation when tactics are resisted
- Maintain objective, factual documentation

### Privacy and Confidentiality
- Ensure all document scanning complies with privacy laws
- Protect confidential information in reports
- Use secure storage for generated reports
- Follow professional ethics guidelines

## Technical Details

### Algorithm Approach
- Keyword-based pattern recognition
- Context extraction for evidence preservation
- Frequency analysis and pattern clustering
- Temporal tracking for timing analysis

### Accuracy Considerations
- Tool provides initial screening and pattern identification
- Professional interpretation required for clinical assessment
- Context review necessary for accurate evaluation
- False positives possible - professional review essential

## Troubleshooting

### Common Issues
1. **Error reading .docx files**: Some older or corrupted Word documents may not be readable
2. **Permission errors**: Ensure read access to all document directories
3. **Large file processing**: Very large documents may take longer to process

### Performance Tips
- Organize documents in focused directories
- Remove unnecessary files before scanning
- Consider processing large document sets in batches

## Updates and Maintenance

### Pattern Updates
The tool's pattern definitions can be updated by modifying the `_initialize_patterns()` method in the `CoerciveControlDetector` class.

### Keyword Enhancement
Additional keywords can be added to pattern categories based on emerging research and professional feedback.

## Support and Feedback

For issues, suggestions, or professional feedback on pattern detection accuracy, please document findings and recommendations for tool improvement.

## Disclaimer

This tool is designed to assist professionals in pattern recognition and documentation. It does not replace professional judgment, clinical assessment, or legal advice. All findings should be reviewed and interpreted by qualified professionals in the appropriate context.

## Version History

- **v1.0.0**: Initial release with 14 pattern categories and comprehensive reporting features