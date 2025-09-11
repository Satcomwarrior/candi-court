import requests
import os

def download_family_law_forms():
    """
    Download official family law forms from Washington Courts and Law Help.
    """
    forms_dir = "c:/Users/Muddm/Downloads/templates/family_law_forms"
    os.makedirs(forms_dir, exist_ok=True)

    # List of FL forms to download (from Washington Courts)
    fl_forms = [
        ("FL UCCJEA 801", "https://www.courts.wa.gov/forms/docs/FL_UCCJEA_801.doc"),
        ("FL UCCJEA 802", "https://www.courts.wa.gov/forms/docs/FL_UCCJEA_802.doc"),
        ("FL UCCJEA 803", "https://www.courts.wa.gov/forms/docs/FL_UCCJEA_803.doc"),
        ("FL UCCJEA 804", "https://www.courts.wa.gov/forms/docs/FL_UCCJEA_804.doc"),
        ("FL UCCJEA 805", "https://www.courts.wa.gov/forms/docs/FL_UCCJEA_805.doc"),
        ("FL UCCJEA 806", "https://www.courts.wa.gov/forms/docs/FL_UCCJEA_806.doc"),
        ("FL UCCJEA 811", "https://www.courts.wa.gov/forms/docs/FL_UCCJEA_811.doc"),
        ("FL UCCJEA 812", "https://www.courts.wa.gov/forms/docs/FL_UCCJEA_812.doc"),
        ("FL UCCJEA 815", "https://www.courts.wa.gov/forms/docs/FL_UCCJEA_815.doc"),
    ]

    for form_name, url in fl_forms:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                filename = f"{form_name.replace(' ', '_')}.doc"
                filepath = os.path.join(forms_dir, filename)
                with open(filepath, 'wb') as f:
                    f.write(response.content)
                print(f"[DOWNLOADED] {form_name} -> {filepath}")
            else:
                print(f"[FAILED] {form_name} - Status: {response.status_code}")
        except Exception as e:
            print(f"[ERROR] {form_name} - {e}")

    print(f"\n[COMPLETE] Family law forms downloaded to: {forms_dir}")

if __name__ == "__main__":
    download_family_law_forms()
