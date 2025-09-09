import os
import glob
from dotenv import load_dotenv
from anthropic import Anthropic
from google.cloud import aiplatform
from google.oauth2 import service_account
import PyPDF2
import pandas as pd
from datetime import datetime

# Load environment variables
load_dotenv()
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

# Initialize clients
anthropic = Anthropic(api_key=ANTHROPIC_API_KEY)

# For Google AI Platform (you'll need to set up credentials)
# aiplatform.init(project="your-project-id", location="us-central1")

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

    # Directory containing legal documents
    docs_dir = r"c:\Users\Muddm\Downloads"

    # Process documents
    results = process_documents(docs_dir)

    # Generate report
    generate_report(results)

    print("Analysis complete!")

if __name__ == "__main__":
    main()
