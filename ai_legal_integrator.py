import sys
import os
from dotenv import load_dotenv
from anthropic import Anthropic
import PyPDF2
import spacy
from textblob import TextBlob
import json
from datetime import datetime

# Load environment variables
load_dotenv()
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

# Initialize clients and models
anthropic = Anthropic(api_key=ANTHROPIC_API_KEY)
nlp = spacy.load('en_core_web_sm')

def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF file."""
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            return text
    except Exception as e:
        print(f"Error extracting text from {pdf_path}: {e}")
        return ""

def analyze_with_claude(text, document_name):
    """Analyze document text using Claude for coercive control patterns and legal insights."""
    prompt = f"""
    Analyze the following legal document for patterns of coercive control, abuse, and legal significance.
    Document: {document_name}

    Content:
    {text[:10000]}  # Limit text length for API

    Please provide:
    1. Summary of key legal points
    2. Identification of any coercive control patterns
    3. Risk assessment (Low/Medium/High)
    4. Recommendations for legal strategy
    5. Evidence strength assessment

    Be thorough but concise. Focus on domestic violence, protective orders, and family law aspects.
    """

    try:
        response = anthropic.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=2000,
            temperature=0.3,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return response.content[0].text
    except Exception as e:
        return f"Error analyzing with Claude: {e}"

def perform_nlp_analysis(text):
    """Perform NLP analysis using spaCy and textblob."""
    results = {}

    # spaCy analysis
    doc = nlp(text)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    results['entities'] = entities

    # Sentiment analysis
    blob = TextBlob(text)
    results['sentiment'] = {
        'polarity': blob.sentiment.polarity,
        'subjectivity': blob.sentiment.subjectivity,
        'assessment': 'Positive' if blob.sentiment.polarity > 0.1 else 'Negative' if blob.sentiment.polarity < -0.1 else 'Neutral'
    }

    # Key phrases and patterns
    results['key_phrases'] = [chunk.text for chunk in doc.noun_chunks if len(chunk.text.split()) > 1][:10]

    return results

def analyze_patterns(json_file_path):
    """Analyze coercive control patterns from JSON export."""
    try:
        with open(json_file_path, 'r') as f:
            data = json.load(f)

        # Analyze patterns using Claude
        patterns_text = json.dumps(data, indent=2)
        analysis_prompt = f"""
        Analyze these coercive control patterns for legal significance:

        {patterns_text[:5000]}

        Provide:
        1. Pattern assessment for court proceedings
        2. Evidence strength evaluation
        3. Recommendations for legal strategy
        """

        response = anthropic.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1500,
            temperature=0.2,
            messages=[{"role": "user", "content": analysis_prompt}]
        )

        return response.content[0].text

    except Exception as e:
        return f"Pattern analysis error: {e}"

def process_documents(directory_path):
    """Process all PDF documents in the directory."""
    pdf_files = glob.glob(os.path.join(directory_path, "*.pdf"))
    results = []

    for pdf_file in pdf_files[:10]:  # Process first 10 for demo
        print(f"Processing: {os.path.basename(pdf_file)}")

        # Extract text
        text = extract_text_from_pdf(pdf_file)

        if text.strip():
            # Analyze with Claude
            analysis = analyze_with_claude(text, os.path.basename(pdf_file))

            results.append({
                'document': os.path.basename(pdf_file),
                'text_length': len(text),
                'analysis': analysis,
                'processed_date': datetime.now().isoformat()
            })

    return results

def generate_report(results, output_file="ai_legal_analysis_report.md"):
    """Generate a comprehensive analysis report."""
    report = f"""# AI-Enhanced Legal Document Analysis Report
Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Summary
Processed {len(results)} documents using Anthropic Claude and Google AI analysis.

## Document Analysis

"""

    for result in results:
        report += f"""
### {result['document']}
**Text Length:** {result['text_length']} characters
**Analysis:**
{result['analysis']}

---
"""

    # Save report
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(report)

    print(f"Report saved to: {output_file}")

def main():
    """Main execution function."""
    print("Starting AI Legal Document Analysis...")

    if len(sys.argv) > 1:
        command = sys.argv[1]

        if command == "extract_pdf" and len(sys.argv) > 2:
            # Extract PDF text
            pdf_path = sys.argv[2]
            text = extract_text_from_pdf(pdf_path)
            print(text[:2000])  # Return first 2000 chars

        elif command == "nlp_analysis" and len(sys.argv) > 2:
            # Perform NLP analysis
            file_path = sys.argv[2]
            if file_path.endswith('.pdf'):
                text = extract_text_from_pdf(file_path)
            else:
                with open(file_path, 'r', encoding='utf-8') as f:
                    text = f.read()

            nlp_results = perform_nlp_analysis(text)
            print(f"Sentiment: {nlp_results['sentiment']['assessment']}")
            print(f"Entities: {len(nlp_results['entities'])} detected")

        elif command == "pattern_analysis" and len(sys.argv) > 2:
            # Analyze patterns from JSON
            json_path = sys.argv[2]
            analysis = analyze_patterns(json_path)
            print(analysis)

        else:
            # Default document processing
            docs_dir = r"c:\Users\Muddm\Downloads"
            results = process_documents(docs_dir)
            generate_report(results)
    else:
        # Default behavior
        docs_dir = r"c:\Users\Muddm\Downloads"
        results = process_documents(docs_dir)
        generate_report(results)

    print("Analysis complete!")

if __name__ == "__main__":
    main()
