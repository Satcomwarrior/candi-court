import requests
import os
from pathlib import Path

def download_family_law_forms():
    """
    Download official family law forms from Washington Courts, Snohomish County, and Law Help resources.
    Enhanced to include comprehensive templates for family law cases.
    """
    # Use relative path from repository root
    forms_dir = Path("templates/family_law_forms")
    forms_dir.mkdir(parents=True, exist_ok=True)

    # Comprehensive list of WA family law forms for committed intimate relationships, 
    # domestic violence, contempt, and property disputes
    wa_court_forms = [
        # Domestic Violence Protection Orders
        ("FL DVPO 001", "https://www.courts.wa.gov/forms/docs/FL%20All%20Family%20001%20Petition%20for%20Protection%20Order_2020%2006.docx"),
        ("FL DVPO 002", "https://www.courts.wa.gov/forms/docs/FL%20All%20Family%20002%20Confidential%20Info%20Form_2020%2006.docx"),
        ("FL DVPO 003", "https://www.courts.wa.gov/forms/docs/FL%20All%20Family%20003%20Notice%20of%20Hearing%20Protection%20Order_2020%2006.docx"),
        ("FL DVPO 004", "https://www.courts.wa.gov/forms/docs/FL%20All%20Family%20004%20Temporary%20Protection%20Order_2021%2007.docx"),
        ("FL DVPO 005", "https://www.courts.wa.gov/forms/docs/FL%20All%20Family%20005%20Full%20Protection%20Order_2021%2007.docx"),

        # Anti-Harassment and No Contact Orders  
        ("FL AHPO 001", "https://www.courts.wa.gov/forms/docs/FL%20All%20Family%20011%20Petition%20for%20Anti-Harassment%20Protection%20Order_2020%2006.docx"),
        ("FL AHPO 004", "https://www.courts.wa.gov/forms/docs/FL%20All%20Family%20014%20Temporary%20Anti-Harassment%20Protection%20Order_2020%2006.docx"),
        ("FL AHPO 005", "https://www.courts.wa.gov/forms/docs/FL%20All%20Family%20015%20Full%20Anti-Harassment%20Protection%20Order_2020%2006.docx"),

        # Contempt and Motion Forms
        ("FL Contempt 151", "https://www.courts.wa.gov/forms/docs/FL%20All%20Family%20151%20Motion%20and%20Declaration%20for%20Order%20to%20Show%20Cause%20Re%20Contempt%20and%20Other%20Relief_2020%2006.docx"),
        ("FL Contempt 152", "https://www.courts.wa.gov/forms/docs/FL%20All%20Family%20152%20Notice%20of%20Hearing%20Re%20Contempt_2020%2006.docx"),
        ("FL Contempt 161", "https://www.courts.wa.gov/forms/docs/FL%20All%20Family%20161%20Order%20on%20Motion%20for%20Contempt_2020%2006.docx"),

        # Committed Intimate Relationship (CIR) Forms
        ("FL CIR 401", "https://www.courts.wa.gov/forms/docs/FL%20Parentage%20401%20Petition%20to%20Establish%20Parentage_2020%2006.docx"),
        ("FL CIR 402", "https://www.courts.wa.gov/forms/docs/FL%20Parentage%20402%20Response%20to%20Petition%20Parentage_2020%2006.docx"),

        # Property and Financial Forms
        ("FL Property 171", "https://www.courts.wa.gov/forms/docs/FL%20All%20Family%20171%20Motion%20for%20Temporary%20Family%20Law%20Order_2020%2006.docx"),
        ("FL Property 172", "https://www.courts.wa.gov/forms/docs/FL%20All%20Family%20172%20Declaration%20in%20Support%20of%20Motion%20for%20Temporary%20Order_2020%2006.docx"),
        ("FL Property 181", "https://www.courts.wa.gov/forms/docs/FL%20All%20Family%20181%20Temporary%20Family%20Law%20Order_2020%2006.docx"),

        # Motion and Declaration Forms
        ("FL Motion 131", "https://www.courts.wa.gov/forms/docs/FL%20All%20Family%20131%20Motion%20and%20Declaration%20for%20Temporary%20Order_2020%2006.docx"),
        ("FL Motion 135", "https://www.courts.wa.gov/forms/docs/FL%20All%20Family%20135%20Response%20to%20Motion%20for%20Temporary%20Order_2020%2006.docx"),

        # Service and Notice Forms
        ("FL Service 101", "https://www.courts.wa.gov/forms/docs/FL%20All%20Family%20101%20Proof%20of%20Personal%20Service_2020%2006.docx"),
        ("FL Service 102", "https://www.courts.wa.gov/forms/docs/FL%20All%20Family%20102%20Proof%20of%20Mailing_2020%2006.docx"),

        # UCCJEA Forms (for cases involving children)
        ("FL UCCJEA 801", "https://www.courts.wa.gov/forms/docs/FL_UCCJEA_801.doc"),
        ("FL UCCJEA 802", "https://www.courts.wa.gov/forms/docs/FL_UCCJEA_802.doc"),
        ("FL UCCJEA 803", "https://www.courts.wa.gov/forms/docs/FL_UCCJEA_803.doc"),
    ]

    # Download WA Court forms
    print("[INFO] Downloading Washington State Court Forms...")
    downloaded_count = 0
    failed_count = 0
    
    for form_name, url in wa_court_forms:
        try:
            response = requests.get(url, timeout=30)
            if response.status_code == 200:
                # Determine file extension from URL or content-type
                if url.endswith('.docx'):
                    filename = f"{form_name.replace(' ', '_')}.docx"
                elif url.endswith('.doc'):
                    filename = f"{form_name.replace(' ', '_')}.doc"
                elif url.endswith('.pdf'):
                    filename = f"{form_name.replace(' ', '_')}.pdf"
                else:
                    filename = f"{form_name.replace(' ', '_')}.docx"  # Default to docx
                
                filepath = forms_dir / filename
                with open(filepath, 'wb') as f:
                    f.write(response.content)
                print(f"[DOWNLOADED] {form_name} -> {filepath}")
                downloaded_count += 1
            else:
                print(f"[FAILED] {form_name} - Status: {response.status_code}")
                failed_count += 1
        except Exception as e:
            print(f"[ERROR] {form_name} - {e}")
            failed_count += 1

    # Create a catalog of downloaded forms
    catalog_file = forms_dir / "form_catalog.txt"
    with open(catalog_file, 'w') as f:
        f.write("# Washington State Family Law Forms Catalog\n")
        f.write("# Downloaded for automated legal case workflow\n\n")
        f.write("## Domestic Violence Protection Orders\n")
        f.write("- FL DVPO 001: Petition for Protection Order\n")
        f.write("- FL DVPO 002: Confidential Information Form\n")
        f.write("- FL DVPO 003: Notice of Hearing Protection Order\n")
        f.write("- FL DVPO 004: Temporary Protection Order\n")
        f.write("- FL DVPO 005: Full Protection Order\n\n")
        
        f.write("## Anti-Harassment Protection Orders\n") 
        f.write("- FL AHPO 001: Petition for Anti-Harassment Protection Order\n")
        f.write("- FL AHPO 004: Temporary Anti-Harassment Protection Order\n")
        f.write("- FL AHPO 005: Full Anti-Harassment Protection Order\n\n")
        
        f.write("## Contempt and Motion Forms\n")
        f.write("- FL Contempt 151: Motion and Declaration for Order to Show Cause Re Contempt\n")
        f.write("- FL Contempt 152: Notice of Hearing Re Contempt\n")
        f.write("- FL Contempt 161: Order on Motion for Contempt\n\n")
        
        f.write("## Property and Financial Forms\n")
        f.write("- FL Property 171: Motion for Temporary Family Law Order\n")
        f.write("- FL Property 172: Declaration in Support of Motion for Temporary Order\n")
        f.write("- FL Property 181: Temporary Family Law Order\n\n")
        
        f.write("## Service and Proof Forms\n")
        f.write("- FL Service 101: Proof of Personal Service\n")
        f.write("- FL Service 102: Proof of Mailing\n\n")

    print(f"\n[COMPLETE] Downloaded {downloaded_count} forms, {failed_count} failed")
    print(f"[COMPLETE] Forms saved to: {forms_dir}")
    print(f"[COMPLETE] Form catalog created: {catalog_file}")

def get_available_templates():
    """
    Return a list of available template files for use in document generation.
    """
    forms_dir = Path("templates/family_law_forms")
    if not forms_dir.exists():
        return []
    
    templates = []
    for template_file in forms_dir.glob("*.doc*"):
        templates.append({
            "name": template_file.stem,
            "path": str(template_file),
            "type": "official_wa_court_form"
        })
    
    return templates

if __name__ == "__main__":
    download_family_law_forms()
