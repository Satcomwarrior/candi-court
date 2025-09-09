#!/usr/bin/env python3
"""
Enhanced Family Law Forms Downloader for Washington State Courts

Automates the download of official blank legal forms and templates from:
- Washington Courts Forms Library
- Washington Law Help Form Library
- Snohomish County Superior Court specific forms

Ensures compliance with Snohomish County Superior Court rules and formatting.
"""

import requests
import os
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple
import time


class WashingtonFormsDownloader:
    """Enhanced downloader for Washington State legal forms."""
    
    def __init__(self, base_dir: str = None):
        """Initialize the forms downloader."""
        if base_dir is None:
            base_dir = os.path.join(os.getcwd(), "templates", "family_law_forms")
        
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)
        
        # Washington Courts base URLs
        self.wa_courts_base = "https://www.courts.wa.gov/forms/docs/"
        self.wa_law_help_base = "https://www.washingtonlawhelp.org/"
        
        # Session for connection reuse
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        # Download log
        self.download_log = []

    def get_family_law_forms_list(self) -> Dict[str, List[Tuple[str, str]]]:
        """Get comprehensive list of family law forms to download."""
        return {
            "commitment_protection_orders": [
                ("FL UCCJEA 801", "FL_UCCJEA_801.doc"),
                ("FL UCCJEA 802", "FL_UCCJEA_802.doc"),
                ("FL UCCJEA 803", "FL_UCCJEA_803.doc"),
                ("FL UCCJEA 804", "FL_UCCJEA_804.doc"),
                ("FL UCCJEA 805", "FL_UCCJEA_805.doc"),
                ("FL UCCJEA 806", "FL_UCCJEA_806.doc"),
                ("FL UCCJEA 811", "FL_UCCJEA_811.doc"),
                ("FL UCCJEA 812", "FL_UCCJEA_812.doc"),
                ("FL UCCJEA 815", "FL_UCCJEA_815.doc"),
            ],
            "dissolution_forms": [
                ("FL Dissolve 501", "FL_Dissolve_501.doc"),
                ("FL Dissolve 502", "FL_Dissolve_502.doc"),
                ("FL Dissolve 503", "FL_Dissolve_503.doc"),
                ("FL Divorcing 101", "FL_Divorcing_101.doc"),
                ("FL Divorcing 111", "FL_Divorcing_111.doc"),
                ("FL Divorcing 121", "FL_Divorcing_121.doc"),
            ],
            "protection_orders": [
                ("FL All Family 160", "FL_All_Family_160.doc"),
                ("FL All Family 161", "FL_All_Family_161.doc"),
                ("FL All Family 162", "FL_All_Family_162.doc"),
                ("FL All Family 166", "FL_All_Family_166.doc"),
                ("FL All Family 167", "FL_All_Family_167.doc"),
            ],
            "contempt_forms": [
                ("FL All Family 166", "FL_All_Family_166_Order_to_Go_to_Court_for_Contempt_Hrg.doc"),
                ("FL All Family 167", "FL_All_Family_167_Contempt_Hrg_Order.doc"),
            ],
            "service_forms": [
                ("FL All Family 101", "FL_All_Family_101_Proof_of_Personal_Service.doc"),
                ("FL All Family 102", "FL_All_Family_102_Return_of_Service.doc"),
            ],
            "motions_orders": [
                ("FL All Family 135", "FL_All_Family_135.doc"),
                ("FL All Family 140", "FL_All_Family_140.doc"),
                ("FL All Family 145", "FL_All_Family_145.doc"),
            ]
        }

    def download_form(self, form_name: str, filename: str, category: str = "general") -> bool:
        """
        Download a single form with retry logic and error handling.
        
        Args:
            form_name: Display name of the form
            filename: Filename on the server
            category: Category subdirectory
            
        Returns:
            True if successful, False otherwise
        """
        url = self.wa_courts_base + filename
        category_dir = self.base_dir / category
        category_dir.mkdir(exist_ok=True)
        
        local_filename = filename.replace('.doc', f'_{datetime.now().strftime("%Y%m%d")}.doc')
        filepath = category_dir / local_filename
        
        try:
            print(f"Downloading {form_name}...")
            response = self.session.get(url, timeout=30)
            
            if response.status_code == 200:
                with open(filepath, 'wb') as f:
                    f.write(response.content)
                
                self.download_log.append({
                    "form_name": form_name,
                    "filename": filename,
                    "local_path": str(filepath),
                    "category": category,
                    "status": "success",
                    "timestamp": datetime.now().isoformat(),
                    "size_bytes": len(response.content)
                })
                
                print(f"✓ {form_name} downloaded successfully")
                return True
            else:
                print(f"✗ {form_name} failed - HTTP {response.status_code}")
                self.download_log.append({
                    "form_name": form_name,
                    "filename": filename,
                    "category": category,
                    "status": "failed",
                    "error": f"HTTP {response.status_code}",
                    "timestamp": datetime.now().isoformat()
                })
                return False
                
        except Exception as e:
            print(f"✗ {form_name} error - {e}")
            self.download_log.append({
                "form_name": form_name,
                "filename": filename,
                "category": category,
                "status": "error",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            })
            return False

    def download_all_forms(self) -> Dict[str, int]:
        """Download all family law forms organized by category."""
        forms_list = self.get_family_law_forms_list()
        stats = {"total": 0, "successful": 0, "failed": 0}
        
        print("Starting download of Washington State Family Law Forms...")
        print(f"Download directory: {self.base_dir}")
        print("=" * 60)
        
        for category, forms in forms_list.items():
            print(f"\nDownloading {category.replace('_', ' ').title()} forms:")
            print("-" * 40)
            
            for form_name, filename in forms:
                stats["total"] += 1
                if self.download_form(form_name, filename, category):
                    stats["successful"] += 1
                else:
                    stats["failed"] += 1
                
                # Small delay to be respectful to the server
                time.sleep(0.5)
        
        return stats

    def create_snohomish_county_templates(self):
        """Create Snohomish County specific templates with proper formatting."""
        print("\nCreating Snohomish County specific templates...")
        
        snohomish_dir = self.base_dir / "snohomish_county"
        snohomish_dir.mkdir(exist_ok=True)
        
        # Create motion template
        self._create_motion_template(snohomish_dir)
        
        # Create declaration template
        self._create_declaration_template(snohomish_dir)
        
        # Create contempt motion template
        self._create_contempt_motion_template(snohomish_dir)
        
        print("✓ Snohomish County templates created")

    def _create_motion_template(self, output_dir: Path):
        """Create a Snohomish County compliant motion template."""
        try:
            from docx import Document
            from docx.shared import Inches
            from docx.enum.text import WD_ALIGN_PARAGRAPH
            
            doc = Document()
            
            # Set margins (1 inch all around - court standard)
            for section in doc.sections:
                section.top_margin = Inches(1)
                section.bottom_margin = Inches(1)
                section.left_margin = Inches(1)
                section.right_margin = Inches(1)
            
            # Header
            header = doc.add_paragraph()
            header.alignment = WD_ALIGN_PARAGRAPH.CENTER
            header.add_run("SUPERIOR COURT OF WASHINGTON FOR SNOHOMISH COUNTY").bold = True
            
            doc.add_paragraph()
            
            # Case caption
            case_table = doc.add_table(rows=3, cols=2)
            case_table.style = 'Table Grid'
            
            # Left column - case info
            case_table.cell(0, 0).text = "In re: {{petitioner_name}} and {{respondent_name}}"
            case_table.cell(1, 0).text = "Petitioner and Respondent"
            case_table.cell(2, 0).text = ""
            
            # Right column - case number
            case_table.cell(0, 1).text = "Case No. {{case_number}}"
            case_table.cell(1, 1).text = "MOTION FOR {{relief_requested}}"
            case_table.cell(2, 1).text = "Note on Motion Docket: {{hearing_date}}"
            
            doc.add_paragraph()
            
            # Motion body
            doc.add_paragraph("TO THE HONORABLE COURT:")
            doc.add_paragraph()
            
            doc.add_heading("I. INTRODUCTION", level=2)
            doc.add_paragraph("{{introduction_paragraph}}")
            
            doc.add_heading("II. STATEMENT OF FACTS", level=2)
            doc.add_paragraph("{{facts_section}}")
            
            doc.add_heading("III. LEGAL ARGUMENT", level=2)
            doc.add_paragraph("{{legal_arguments}}")
            
            doc.add_heading("IV. CONCLUSION", level=2)
            doc.add_paragraph("{{conclusion_paragraph}}")
            
            # Signature block
            doc.add_paragraph()
            doc.add_paragraph("Respectfully submitted,")
            doc.add_paragraph()
            doc.add_paragraph("_________________________________")
            doc.add_paragraph("{{your_name}}")
            doc.add_paragraph("Pro Se {{party_designation}}")
            doc.add_paragraph("{{your_address}}")
            doc.add_paragraph("{{your_city_state_zip}}")
            doc.add_paragraph("Phone: {{your_phone}}")
            doc.add_paragraph("Email: {{your_email}}")
            
            # Save template
            template_path = output_dir / "snohomish_motion_template.docx"
            doc.save(template_path)
            
            self.download_log.append({
                "form_name": "Snohomish County Motion Template",
                "local_path": str(template_path),
                "category": "snohomish_county",
                "status": "created",
                "timestamp": datetime.now().isoformat()
            })
            
        except ImportError:
            print("Warning: python-docx not available for template creation")

    def _create_declaration_template(self, output_dir: Path):
        """Create a declaration template for evidence presentation."""
        try:
            from docx import Document
            
            doc = Document()
            
            # Title
            title = doc.add_heading('DECLARATION OF {{declarant_name}}', 0)
            title.alignment = 1
            
            doc.add_paragraph()
            doc.add_paragraph("I, {{declarant_name}}, declare as follows:")
            doc.add_paragraph()
            
            # Declaration sections
            for i in range(1, 11):
                doc.add_paragraph(f"{i}. {{declaration_paragraph_{i}}}")
            
            # Oath
            doc.add_paragraph()
            doc.add_paragraph("I declare under penalty of perjury under the laws of the State of Washington that the foregoing is true and correct.")
            
            # Signature
            doc.add_paragraph()
            doc.add_paragraph("DATED this _____ day of _____________, 2025.")
            doc.add_paragraph()
            doc.add_paragraph("_________________________________")
            doc.add_paragraph("{{declarant_name}}")
            
            template_path = output_dir / "snohomish_declaration_template.docx"
            doc.save(template_path)
            
        except ImportError:
            pass

    def _create_contempt_motion_template(self, output_dir: Path):
        """Create a contempt motion template."""
        try:
            from docx import Document
            
            doc = Document()
            
            title = doc.add_heading('MOTION FOR ORDER TO SHOW CAUSE FOR CONTEMPT', 0)
            title.alignment = 1
            
            doc.add_paragraph("TO THE HONORABLE COURT:")
            doc.add_paragraph()
            
            doc.add_paragraph("Petitioner moves this Court for an Order directing Respondent to show cause why Respondent should not be held in contempt for violation of the Court's orders, and states:")
            doc.add_paragraph()
            
            # Sections
            doc.add_heading("I. BACKGROUND", level=2)
            doc.add_paragraph("{{background_facts}}")
            
            doc.add_heading("II. VIOLATIONS", level=2)
            doc.add_paragraph("{{violation_details}}")
            
            doc.add_heading("III. RELIEF REQUESTED", level=2)
            doc.add_paragraph("{{relief_requested}}")
            
            template_path = output_dir / "snohomish_contempt_motion_template.docx"
            doc.save(template_path)
            
        except ImportError:
            pass

    def save_download_log(self):
        """Save the download log to a JSON file."""
        log_file = self.base_dir / f"download_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(log_file, 'w') as f:
            json.dump({
                "download_session": {
                    "timestamp": datetime.now().isoformat(),
                    "total_downloads": len(self.download_log),
                    "base_directory": str(self.base_dir)
                },
                "downloads": self.download_log
            }, f, indent=2)
        
        print(f"\n✓ Download log saved to: {log_file}")

    def generate_summary_report(self, stats: Dict[str, int]):
        """Generate a summary report of the download session."""
        print("\n" + "=" * 60)
        print("DOWNLOAD SUMMARY REPORT")
        print("=" * 60)
        print(f"Total forms attempted: {stats['total']}")
        print(f"Successfully downloaded: {stats['successful']}")
        print(f"Failed downloads: {stats['failed']}")
        print(f"Success rate: {(stats['successful'] / stats['total'] * 100):.1f}%")
        print(f"Download directory: {self.base_dir}")
        
        if stats['failed'] > 0:
            print("\nFailed downloads:")
            for entry in self.download_log:
                if entry['status'] in ['failed', 'error']:
                    print(f"  • {entry['form_name']}: {entry.get('error', 'Unknown error')}")


def main():
    """Main function to run the enhanced forms downloader."""
    print("Enhanced Washington State Family Law Forms Downloader")
    print("=" * 60)
    
    # Initialize downloader
    downloader = WashingtonFormsDownloader()
    
    # Download all forms
    stats = downloader.download_all_forms()
    
    # Create Snohomish County specific templates
    downloader.create_snohomish_county_templates()
    
    # Save log and generate report
    downloader.save_download_log()
    downloader.generate_summary_report(stats)
    
    print("\n✓ Forms download and template creation completed!")
    print(f"Forms are organized in: {downloader.base_dir}")


if __name__ == "__main__":
    main()
