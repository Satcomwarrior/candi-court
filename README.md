# Reasonableness Analyzer for Legal Requests and Complaints

This tool analyzes the reasonableness of legal requests and complaints based on multiple criteria including clarity, specificity, evidence, tone, and legal merit.

## Features

- **Multi-criteria Analysis**: Evaluates text across 5 key dimensions
- **Scoring System**: Provides numerical scores (1-5) and overall reasonableness levels
- **Detailed Feedback**: Offers specific suggestions for improvement
- **Flexible Input**: Supports text files, DOCX documents, and direct text input
- **Configurable**: Customizable weights and thresholds
- **CLI Interface**: Easy-to-use command-line tool

## Analysis Criteria

### 1. Clarity (Weight: 25%)
- Sentence structure and length
- Use of clear, unambiguous language
- Logical organization

### 2. Specificity (Weight: 20%)
- Inclusion of dates, times, and amounts
- Specific names and locations
- Concrete details vs. vague language

### 3. Evidence (Weight: 20%)
- Supporting documentation mentioned
- References to exhibits or attachments
- Factual statements vs. opinions

### 4. Tone (Weight: 15%)
- Professional language
- Appropriate level of formality
- Absence of aggressive or inappropriate language

### 5. Legal Merit (Weight: 20%)
- Use of proper legal terminology
- Citations of relevant laws or regulations
- Realistic vs. frivolous claims

## Installation

No external dependencies required for basic functionality. For DOCX support:

```bash
pip install python-docx
```

## Usage

### Command Line Interface

```bash
# Analyze a text file
python cli.py -f request.txt

# Analyze a DOCX document
python cli.py -f complaint.docx

# Analyze direct text input
python cli.py -t "I request a refund for my defective product."

# Read from standard input
echo "Sample text" | python cli.py --stdin

# Output as JSON
python cli.py -f request.txt --format json

# Save output to file
python cli.py -f request.txt -o analysis_results.txt

# Use custom configuration
python cli.py -f request.txt --config custom_config.json

# Override specific weights
python cli.py -f request.txt --weights '{"clarity": 0.4, "tone": 0.3}'
```

### Python API

```python
from reasonableness_analyzer import analyze_text, ReasonablenessAnalyzer

# Simple analysis
text = "I would like to request a refund for my purchase."
result = analyze_text(text)

print(f"Score: {result.overall_score}")
print(f"Level: {result.reasonableness_level.name}")
print(f"Suggestions: {result.suggestions}")

# Advanced usage with custom configuration
config = {
    'weights': {
        'clarity': 0.3,
        'specificity': 0.25,
        'evidence': 0.2,
        'tone': 0.15,
        'legal_merit': 0.1
    }
}

analyzer = ReasonablenessAnalyzer(config)
result = analyzer.analyze(text)
```

## Configuration

The analyzer can be customized using a JSON configuration file:

```json
{
  "weights": {
    "clarity": 0.25,
    "specificity": 0.20,
    "evidence": 0.20,
    "tone": 0.15,
    "legal_merit": 0.20
  },
  "thresholds": {
    "very_unreasonable": 1.5,
    "unreasonable": 2.5,
    "neutral": 3.5,
    "reasonable": 4.5
  }
}
```

## Reasonableness Levels

- **Very Unreasonable (1.0-1.5)**: Highly problematic requests with multiple issues
- **Unreasonable (1.6-2.5)**: Significant problems that need addressing
- **Neutral (2.6-3.5)**: Average requests with room for improvement
- **Reasonable (3.6-4.5)**: Well-structured requests with minor issues
- **Very Reasonable (4.6-5.0)**: Excellent requests meeting all criteria

## Testing

Run the test suite to verify functionality:

```bash
python test_analyzer.py
```

## Examples

### Reasonable Request
```
Score: 4.2/5.0
Level: Very Reasonable

I am writing to request a refund of $150.00 for the defective product I purchased
on January 15, 2024. The item (Invoice #12345) stopped working after two days.
I have the receipt and photos of the defect. Please process this refund within
10 business days as stated in your return policy.
```

### Unreasonable Demand
```
Score: 1.8/5.0
Level: Unreasonable

YOU IDIOTS MESSED UP MY ORDER AND I DEMAND $10,000 IN DAMAGES!!!
THIS IS OUTRAGEOUS!!! I'M GOING TO SUE EVERYONE!!!
```

## File Structure

```
├── reasonableness_analyzer.py  # Main analyzer module
├── cli.py                     # Command-line interface
├── config.json               # Default configuration
├── test_analyzer.py          # Test suite
└── README.md                 # This documentation
```

## Use Cases

- **Legal Professionals**: Evaluate client requests and complaints
- **Customer Service**: Assess customer complaint reasonableness
- **Document Review**: Screen legal documents for quality
- **Training**: Help individuals improve their written requests
- **Quality Control**: Ensure consistent standards in legal communications

## Limitations

- Analysis is based on text patterns and may not capture all nuances
- Legal advice should always be sought from qualified professionals
- Cultural and jurisdictional differences in legal communication are not accounted for
- Works best with English-language text

## Contributing

To extend the analyzer:

1. Modify the analysis criteria in `reasonableness_analyzer.py`
2. Update configuration options in `config.json`
3. Add new test cases in `test_analyzer.py`
4. Update documentation as needed

## License

This tool is provided as-is for educational and professional use. Users are responsible for ensuring appropriate use in their specific context.