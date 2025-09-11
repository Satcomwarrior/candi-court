# FULL AUTOMATED LEGAL CASE WORKFLOW SCRIPT
# Author: William Miller
# Date: 09/07/2025

import os
import json

# Uncomment and install if needed:
# pip install python-docx openai requests

# Import for document generation
from docx import Document

# Uncomment and configure your AI API
# import openai

# ==== CONFIGURATION ====

YOUR_NAME = "William Miller"
YOUR_PHONE = "206-226-2085"
YOUR_EMAIL = "wmiller@muddmonkiesinc.com"

# Your OpenAI API key here (replace with your key)
# openai.api_key = "your_openai_api_key"

# === STEP 1: DOCUMENT GENERATION ===

def generate_legal_document(template_path, case_data, output_path):
    """
    Generate a legal document from a Word template by replacing placeholders.
    """

    doc = Document(template_path)

    # Example simple replacement strategy (you can enhance with bookmarks or content controls)
    for para in doc.paragraphs:
        for key, value in case_data.items():
            placeholder = f"{{{{{key}}}}}"  # e.g., {{case_number}}
            if placeholder in para.text:
                para.text = para.text.replace(placeholder, str(value))

    doc.save(output_path)
    print(f"[INFO] Generated legal document saved at {output_path}")
    return output_path

# === STEP 1.5: DIRECTORY SETUP ===

def ensure_case_directories():
    """
    Create necessary case directories with proper error handling.
    This ensures the case_folder/exhibits directory exists for PDF storage.
    """
    directories = [
        'case_folder',
        'case_folder/exhibits',
        'outputs',
        'templates'
    ]
    
    for directory in directories:
        try:
            os.makedirs(directory, exist_ok=True)
            print(f"[INFO] Ensured directory exists: {directory}")
        except OSError as e:
            print(f"[ERROR] Failed to create directory {directory}: {e}")
            raise
        except Exception as e:
            print(f"[ERROR] Unexpected error creating directory {directory}: {e}")
            raise
    
    # Create README in exhibits folder if it doesn't exist
    readme_path = os.path.join('case_folder', 'exhibits', 'README.md')
    if not os.path.exists(readme_path):
        try:
            with open(readme_path, 'w', encoding='utf-8') as f:
                f.write("""# Case Exhibits Directory

This directory is for storing PDF documents and other exhibits related to your legal case.

## Usage
- Place PDF exhibits here for AI analysis
- Organize files with descriptive names
- Include dates in filenames when relevant

## File Types Supported
- PDF documents (.pdf)
- Text files (.txt)
- Markdown files (.md) 
- Word documents (.docx)

## Example Files
- motion_2025_01_15.pdf
- communications_transcript.txt
- medical_records_summary.pdf
- financial_documents.pdf

The AI analysis tools will automatically process files from this directory when specified in the workflow.
""")
            print(f"[INFO] Created README in exhibits directory: {readme_path}")
        except Exception as e:
            print(f"[WARNING] Could not create README file: {e}")

# === STEP 2: COMMUNICATIONS ANALYSIS (ChatGPT / Claude AI) ===

def analyze_communications_via_ai(text):
    """
    Sends communication text to Google AI Studio via call_studio_ai function.
    Returns analysis summary for coercive control patterns.
    """
    prompt = f"""Analyze the following communications for coercive control, manipulation, and perceived burdensomeness patterns:

{text}

Provide a detailed summary and identify key patterns relevant to family law matters."""

    print("[AI] Sending communication analysis prompt to Google AI Studio...")
    
    try:
        # Use the call_studio_ai function for real AI analysis
        from ai_studio_code import call_studio_ai
        response = call_studio_ai(prompt)
        return response
    except Exception as e:
        print(f"[AI] Error calling Google AI Studio: {e}")
        # Fallback to simulated response
        response = ("[AI LOGIC OUTPUT] Summary: Coercive control patterns evidenced "
                    "by repeated exclusion and isolative manipulation. Perceived burdensomeness "
                    "visible in language suggesting self-sacrifice for others' benefit.")
        return response

# === STEP 3: FACTS SUMMARIZATION AND ARGUMENT GENERATION ===

def summarize_case_facts(case_facts):
    prompt = f"Summarize these legal facts clearly for a Snohomish County family law motion:\n{case_facts}"

    print("[AI] Summarizing case facts with Google AI Studio...")
    
    try:
        # Use the call_studio_ai function for real AI analysis
        from ai_studio_code import call_studio_ai
        summary = call_studio_ai(prompt)
        return summary
    except Exception as e:
        print(f"[AI] Error calling Google AI Studio: {e}")
        # Fallback to simulated response
        summary = ("[Summary] The defendant engaged in repeated violations of "
                   "court orders, including financial abuse and property interference.")
        return summary

def generate_legal_arguments(summary_text):
    prompt = f"Generate 3-5 bullet points for legal arguments supporting a contempt or protective order motion based on this summary:\n{summary_text}"

    print("[AI] Generating legal arguments with Google AI Studio...")
    
    try:
        # Use the call_studio_ai function for real AI analysis
        from ai_studio_code import call_studio_ai
        arguments_text = call_studio_ai(prompt)
        # Try to parse bullet points from response
        arguments = [line.strip('- ').strip() for line in arguments_text.split('\n') if line.strip().startswith('-') or line.strip().startswith('•')]
        if not arguments:
            # If no bullet points found, split by newlines and filter
            arguments = [line.strip() for line in arguments_text.split('\n') if line.strip() and len(line.strip()) > 10]
        return arguments[:5]  # Limit to 5 arguments
    except Exception as e:
        print(f"[AI] Error calling Google AI Studio: {e}")
        # Fallback to simulated response
        arguments = [
            "Defendant willfully violated the protection order repeatedly.",
            "Financial transactions show ongoing support by plaintiff despite abuse.",
            "Pattern of coercive control demonstrated by property exclusion.",
            "Insurance cancellation during medical crisis constitutes bad faith.",
            "Digital trespass evidences unauthorized surveillance."
        ]
        return arguments

# === STEP 4: AI STUDIO DATA EXTRACTION (Google AI Studio Integration) ===

def ai_studio_extract_metadata(doc_paths):
    """
    Extract document metadata and entity extraction using Google AI Studio.
    Integrates with the call_studio_ai function for real AI analysis.
    """
    print("[AI Studio] Extracting metadata from documents...")
    
    try:
        # Import the call_studio_ai function
        from ai_studio_code import call_studio_ai
        
        # Prepare the prompt for metadata extraction
        prompt = """
        Analyze the provided documents and extract the following metadata:
        1. Important dates (format: YYYY-MM-DD)
        2. Person names mentioned
        3. Document categories (Evidence, Financial Records, Communications, etc.)
        4. Financial summaries (amounts, transactions, etc.)
        
        Please return the information in JSON format with these keys:
        - dates: array of dates found
        - persons: array of person names
        - categories: array of document categories
        - financial_summaries: object with financial data
        
        Focus on legal case information, particularly for family law and financial analysis.
        """
        
        # Call Google AI Studio with the documents
        response = call_studio_ai(prompt, files=doc_paths)
        
        # Try to parse JSON response, fallback to simulated data if needed
        try:
            import json
            # Look for JSON in the response
            import re
            json_match = re.search(r'\{[^}]*\}', response, re.DOTALL)
            if json_match:
                extracted = json.loads(json_match.group())
                return extracted
        except:
            pass
            
        # Fallback to simulated data if AI response cannot be parsed
        print("[AI Studio] Using fallback data due to parsing issues")
        extracted = {
            "dates": ["2024-09-13", "2025-03-08", "2025-06-28"],
            "persons": ["William Miller", "Candi Brightwell"],
            "categories": ["Evidence", "Financial Records", "Communications"],
            "financial_summaries": {"PayPalTransfers2025": 7355.0}
        }
        return extracted
        
    except Exception as e:
        print(f"[AI Studio] Error: {e}")
        print("[AI Studio] Using simulated data due to error")
        # Fallback to simulated data
        extracted = {
            "dates": ["2024-09-13", "2025-03-08", "2025-06-28"],
            "persons": ["William Miller", "Candi Brightwell"],
            "categories": ["Evidence", "Financial Records", "Communications"],
            "financial_summaries": {"PayPalTransfers2025": 7355.0}
        }
        return extracted

# === STEP 5: EXPERT WITNESS OUTREACH EMAIL GENERATION ===

def generate_intake_email(expert_type, provider_name):
    templates = {
        "psychologist": f"""Subject: Expert Psychological Evaluation and Testimony Inquiry for Snohomish County Family Law Case

Dear {provider_name},

I am preparing a family law case involving committed intimate relationship dissolution, psychological coercion, and trauma. I seek an expert psychologist for evaluation, expert testimony, and reporting.

Please provide your experience in forensic evaluations, availability for remote or in-person consultations, fee structure, and engagement procedures.

Thank you for your time.

Best regards,
{YOUR_NAME}
Phone: {YOUR_PHONE}
Email: {YOUR_EMAIL}
""",
        "financial_forensic": f"""Subject: Request for Financial Forensics Consultation and Expert Witness Services

Dear {provider_name},

I am involved in a family law proceeding needing a financial forensic expert to assess business valuation, asset tracing, and related financial abuse issues.

Kindly share your experience with family law cases, availability, fees, and how to engage your services.

Thank you.

Sincerely,
{YOUR_NAME}
Phone: {YOUR_PHONE}
Email: {YOUR_EMAIL}
""",
        "domestic_violence": f"""Subject: Inquiry Regarding Domestic Violence Expert Services for Family Law Case

Dear {provider_name},

I require an expert witness in domestic violence and coercive control to assist with expert reports and testimony in a family law matter.

Please share your experience, availability for remote/in-person services, fee schedule, and intake process.

Thank you for your assistance.

Kind regards,
{YOUR_NAME}
Phone: {YOUR_PHONE}
Email: {YOUR_EMAIL}
"""
    }
    return templates.get(expert_type, "")

def send_email(email_text):
    """Simulate sending or saving email drafts."""
    print("\n=== EMAIL DRAFT ===\n")
    print(email_text)
    print("\n=== END EMAIL ===\n")

# === MAIN EXECUTION FUNCTION ===

def main():
    # Create necessary directories first
    print("[SETUP] Creating case directory structure...")
    ensure_case_directories()
    
    # Case facts & communications
    # Pull facts from markdown summary
    case_data = {
        "case_number": "2025-PA-000123",
        "facts": (
            "William Miller qualifies as a vulnerable adult under RCW 74.34.020 due to medical vulnerability, PTSD, cognitive impairment, and physical incapacitation. "
            "Evidence shows systematic abuse by Candi Brightwell, including property rights violations, medical emergency exploitation, and business interference. "
            "Court filings and declarations confirm Miller as the primary victim, with Candi as the aggressor using DARVO tactics. "
            "Critical legal issues include lockout during recovery, tool disposal, and withholding of property and business assets. "
            "Legal standards and RCW analysis support modification/termination of protection orders and recognition of Miller's status."
        )
    }

    communications_text = (
        "Text/call transcripts show Candi as primary aggressor. "
        "Police reports document Miller's suicidal ideation and garage banishment. "
        "Medical records confirm vulnerable adult status. "
        "Pattern of DARVO manipulation tactics by Candi. "
        "Surveillance admission and EMS records document medical crisis events."
    )

    # 1) Generate Draft Legal Document
    output_doc = generate_legal_document("templates/motion_template.docx", case_data, f"outputs/{case_data['case_number']}_motion.docx")

    # 2) Analyze Communications with AI
    comms_analysis = analyze_communications_via_ai(communications_text)
    print("[COMMUNICATIONS ANALYSIS]\n", comms_analysis)

    # 3) Summarize Facts and Generate Arguments
    fact_summary = summarize_case_facts(case_data["facts"])
    arguments = generate_legal_arguments(fact_summary)
    print("[CASE SUMMARY]\n", fact_summary)
    print("[LEGAL ARGUMENTS]")
    for arg in arguments:
        print("- ", arg)

    # 4) Extract Document Metadata via AI Studio
    extracted_data = ai_studio_extract_metadata([output_doc])
    print("[AI STUDIO EXTRACTED DATA]\n", json.dumps(extracted_data, indent=2))

    # 5) Prepare and output expert witness outreach emails
    expert_list = [
        {"type": "psychologist", "provider": "Wilson Psychological & Forensic Services"},
        {"type": "psychologist", "provider": "Snohomish Counseling Collective"},
        {"type": "psychologist", "provider": "Dr. Rachael Silverman"},
        {"type": "financial_forensic", "provider": "4 Corners Financial Forensics"},
        {"type": "financial_forensic", "provider": "Family Law Consulting"},
        {"type": "domestic_violence", "provider": "LCADV Expert Witness Project"}
    ]

    for expert in expert_list:
        email_body = generate_intake_email(expert["type"], expert["provider"])
        send_email(email_body)

if __name__ == "__main__":
    main()
