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

Install the core dependencies:

```bash
pip install -r requirements.txt
```

For development (includes testing tools):

```bash
pip install -r requirements-dev.txt
```

To build the documentation:

```bash
pip install -r requirements-doc.txt
```
