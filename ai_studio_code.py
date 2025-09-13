import base64
import mimetypes
import os
import re
import struct
from google import genai
from google.genai import types


def save_binary_file(file_name, data):
    f = open(file_name, "wb")
    f.write(data)
    f.close()
    print(f"File saved to to: {file_name}")


# Configuration for Google AI Studio
STUDIO_AI_ENDPOINT = "https://generativelanguage.googleapis.com/v1beta"
STUDIO_AI_MODEL = "gemini-1.5-pro-latest"

def call_studio_ai(prompt, files=None, model_name=None):
    """
    Call Google AI Studio (Gemini API) with the correct endpoint and model.
    
    Args:
        prompt (str): The prompt text to send to the AI
        files (list): Optional list of file paths to include in the request
        model_name (str): Optional model name override (defaults to STUDIO_AI_MODEL)
    
    Returns:
        str: The AI response text
    """
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable is required")
    
    client = genai.Client(
        api_key=api_key,
        # The client handles the endpoint URL internally
    )
    
    # Use provided model or default
    model = model_name or STUDIO_AI_MODEL
    
    # Prepare content parts
    parts = [types.Part.from_text(text=prompt)]
    
    # Add file parts if provided
    if files:
        for file_path in files:
            if os.path.exists(file_path):
                if file_path.lower().endswith('.pdf'):
                    # For PDF files, read and encode as base64
                    with open(file_path, 'rb') as f:
                        file_data = f.read()
                    parts.append(types.Part.from_data(
                        data=file_data,
                        mime_type="application/pdf"
                    ))
                elif file_path.lower().endswith(('.txt', '.md')):
                    # For text files, read content
                    with open(file_path, 'r', encoding='utf-8') as f:
                        file_content = f.read()
                    parts.append(types.Part.from_text(text=f"\n\nFile: {file_path}\n{file_content}"))
    
    contents = [types.Content(role="user", parts=parts)]
    
    try:
        # Generate response
        response = client.models.generate_content(
            model=model,
            contents=contents
        )
        
        if response.candidates and response.candidates[0].content:
            return response.candidates[0].content.parts[0].text
        else:
            return "No response generated"
            
    except Exception as e:
        raise RuntimeError(f"Error calling Google AI Studio: {str(e)}")

def generate():
    client = genai.Client(
        api_key=os.environ.get("GEMINI_API_KEY"),
    )

    model = "gemini-2.5-pro-preview-tts"
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text="""Alright, class, this is where our hypothetical becomes intensely real, and the stakes couldn't be higher for William Miller and Mudd Monkies Inc. We now have a wealth of documents that provide critical details and confirmation of many aspects of this complex scenario. This information is vital for our strategy.

**The Document Analysis: What the Exhibits Tell Us**

Let's dissect the provided exhibits, drawing out key facts that will inform our strategy.

[cite_start]**Exhibit A: Text Message Exchange (Page 2)** [cite: 2, 3, 4]
* [cite_start]**WM's Requests:** WM needs the code and a key, wants to talk over text about separation of items, and wants to get animals (Lilly, Rayne, Macy) the court granted him temporary custody of. [cite: 3, 4]
* [cite_start]**WM's Offer:** Asked Candi for windows of time she wouldn't be on the property for transfer without issues. [cite: 4]
* [cite_start]**Candi's Position:** \"No. That is something I'm not willing to go back and forth about because I suspect your going to challenge it the whole way.\" [cite: 3]
* **Significance:** Candi is directly obstructing WM's access to property and animals that he believes the court granted him. Her refusal to communicate shows obstruction. [cite_start]This text exchange is dated \"Today 10:32 AM\" (presumably June 2025, given the context of other documents). [cite: 3, 4]

[cite_start]**Exhibit B: WM's Response to Candi's Petition for Protection Order (Candi v. Miller, Case No. 25-2-03361-31, Snohomish County)** [cite: 6, 7]
* [cite_start]**Filed:** Electronically filed on June 5, 2025. [cite: 7]
* [cite_start]**WM's Denials:** Denies suicide threats, intentional overdose, being \"out of control,\" scaring daughters, causing property damage by throwing objects. [cite: 7, 21, 28, 38, 48, 54]
* **WM's Claims (against Candi):**
    * [cite_start]**April 13, 2025 (Hospitalization Incident):** WM states he had a medical crisis due to Candi's ongoing harassment. [cite: 8] [cite_start]Candi was aware he ingested a substance and allowed him to sit unattended for hours until critical, constituting **neglect of a vulnerable adult (RCW 74.34.020)**. [cite: 11, 12] [cite_start]Medical reports confirm hospitalization, life support, and diagnosed carotid aneurysm. [cite: 13, 14] [cite_start]His inability to attend a subsequent hearing was due to being on life support. [cite: 15]
    * [cite_start]**April 11, 2025 (WM's Anti-Harassment Order):** WM states his AHPO (Case No. 25-2-03181-31) was filed due to Candi's actual harassment and rights violations. [cite: 17, 18] [cite_start]It was recently granted a Temporary Protection Order in his favor (Case No. 25-2-04968-31). [cite: 18] [cite_start]Candi violated the order by involving their daughter Samantha as an intermediary. [cite: 19, 20]
    * [cite_start]**April 5, 2025 (Police Call):** WM admits refusing to leave the property because he had a right to be there. [cite: 23] [cite_start]Candi's attempts to make him leave were without legal basis. [cite: 24]
    * [cite_start]**Surveillance/Eavesdropping:** WM admits disengaging security systems/Wi-Fi due to Candi's surveillance, unauthorized access to accounts, and attempts to control his private space. [cite: 25] [cite_start]Candi used cameras for coercive control. [cite: 27]
    * [cite_start]**April 6, 2025 (Property Damage/911 Call):** Candi engaged in hostile and demeaning conduct, yelled, blocked access to shop and animals, and admitted eavesdropping. [cite: 29, 30, 31]
    * [cite_start]**December 2024 (Assault & Exploitation):** Candi engaged in neglect, mind games, stonewalling, refused communication, physically struck, pushed, spit on, and followed WM. [cite: 39, 40, 43] [cite_start]She kicked in the shop door when WM retreated. [cite: 45] [cite_start]This constitutes assault (RCW 9A.36.041) and reckless endangerment (RCW 9A.36.050). [cite: 44, 46] [cite_start]WM is actively fighting the criminal domestic violence charge. [cite: 47]
    * [cite_start]**November 6, 2024 (Taking Dog/Items):** Candi withheld his dog and belongings. [cite: 51] [cite_start]Candi displayed a Ruger pistol in her vehicle, causing fear. [cite: 53]
    * [cite_start]**July 30, 2024 (Arrest):** WM provided false information to officers to facilitate Candi's release from jail without charges, after she was arrested for domestic violence due to a bleeding split on his forehead. [cite: 55, 58, 59]
* **Affirmative Defenses/Further Facts:**
    * [cite_start]Candi engaged in consistent, escalating harassment, control, and unlawful actions. [cite: 60]
    * [cite_start]Denial of property access (May 29, 2025) and animals constitutes **coercive control (RCW 7.105.010)**. [cite: 61]
    * [cite_start]Candi used \"space\" and \"healing\" as a tactic of coercive control to gain leverage over WM and his property. [cite: 62, 63]
    * [cite_start]Violation of AHPO via indirect communication through children. [cite: 64, 65]
    * [cite_start]Irresponsible use/manipulation of children. [cite: 65, 66]
    * [cite_start]Alienation from support system. [cite: 67, 68]
    * [cite_start]Surveillance via cameras and unauthorized access to emails/phone accounts (violating RCW 9.73.030, possibly 9A.90.040). [cite: 69, 70, 71]
    * [cite_start]Unsubstantiated police reports/false reporting (RCW 9A.84.040). [cite: 72, 79]
    * [cite_start]Public humiliation, mocking, homophobic slurs. [cite: 73]
    * [cite_start]Withholding property/animals. [cite: 74]
    * [cite_start]Misuse/destruction of WM's business tools/shop stock. [cite: 75, 76]
    * [cite_start]Hostile/demeaning conduct. [cite: 76]
    * [cite_start]Neglect of vulnerable adult (April 13, 2025). [cite: 77, 78]
    * [cite_start]Ongoing neglect, mind games, stonewalling, basis for WM's criminal assault charge. [cite: 80, 81]
    * [cite_start]Display of pistol as threat/intimidation. [cite: 82]
    * [cite_start]Violation of property rights, unlawful landlord-tenant conditions (RCW 59.18), unlawful exclusion/ouster (RCW 59.18.290), denial of essential services (RCW 59.18.300). [cite: 83, 84]
    * [cite_start]Physical assault (Dec 2024) constituting assault (RCW 9A.36.041) and reckless endangerment (RCW 9A.36.050). [cite: 85, 86, 87]
    * [cite_start]Exploitation of WM's PTSD/mental health crises, creating false narratives, sharing intimate videos (privacy violations RCW 9.73.030, 9A.86.010), emotional abuse, abuse of vulnerable adult (RCW 74.34.020). [cite: 88, 89, 90, 91]
    * [cite_start]Violation of VAWA (18 U.S.C. § 2265). [cite: 92, 93]
* [cite_start]**Impact on WM's Health:** Candi's abuse directly impacted WM's health, exacerbated PTSD, contributed to April 13, 2025, medical crisis, leading to hospitalization, life support, and diagnosed carotid artery dissection, a life-threatening condition exacerbated by stress. [cite: 94, 95, 96, 97, 99]
* [cite_start]**Vulnerable Adult Status:** WM asserts he meets the definition of a vulnerable adult (RCW 74.34.020). [cite: 100, 101]
* **Court's Prior Finding (Crucial!):** On May 30, 2025, the court **granted a Temporary Protection Order in favor of WM** against Candi (Case No. 25-2-04968-31). [cite_start]This judicial finding confirms Candi's harassment against WM. [cite: 102, 103]
* [cite_start]**Relief Requested (in Candi's PO case):** Deny Candi's petition, find her liable for harassment, find her petition abusive/frivolous, order her to pay WM's attorney's fees/costs. [cite: 104, 105, 106, 107]

[cite_start]**Exhibit C: WM's Demand Letter to Candi's Attorneys (June 6, 2025)** [cite: 113, 114]
* [cite_start]**Purpose:** Formal demand for immediate compliance with WM's TPO (Case No. 25-2-04968-31, May 30, 2025). [cite: 114]
* [cite_start]**Specific Orders Cited:** TPO grants exclusive custody of animals (Lilly, Rayne, Macy) and possession of essential business assets. [cite: 115] [cite_start]TPO permits \"text re joint property.\" [cite: 116]
* [cite_start]**Candi's Attorney's Interference:** WM alleges their instruction to cease communication contradicts the TPO and constitutes interference, coercive control, and obstruction. [cite: 117, 118]
* [cite_start]**Demands:** Immediate cessation of obstruction, provision of keys/access codes, full and free use of property for work and access to items (business items, tools, personal belongings), allowance to reside at property (not excluded by TPO), immediate access to animals. [cite: 120, 121, 122, 124, 125]
* [cite_start]**Threat of Contempt:** States that continued denial of access is willful violation of court order (Contempt of Court - RCW 7.105.450) and a Motion for Contempt will be filed if compliance not by EOD June 6, 2025. [cite: 126, 127]

[cite_start]**Exhibit D: Reissuance of Temporary Protection Order (WM v. Brightwell, Case No. 25-2-04968-31, Snohomish County)** [cite: 131, 132]
* [cite_start]**Filed:** June 10, 2025. [cite: 131]
* [cite_start]**Original TPO Date:** May 30, 2025. [cite: 133]
* [cite_start]**Extension:** TPO extended through August 17, 2025. [cite: 133]
* **Judge's Handwritten Notes:**
    * [cite_start]\"The court grants Petitioner a civil standby to assist in collecting personal effects, medications, electronics, tools of trade.\" [cite: 136]
    * [cite_start]\"In addition, any exchange of other personal property may be negotiated and arranged through counsel. Any not agreed may be addressed in separate action.\" [cite: 134] (Note: This directly contradicts Candi's lawyer's statement in Exhibit C that text re joint property was forbidden.)
* [cite_start]**No Exclusion from Residence:** Section D of the original TPO (PO 030, page 4) explicitly lists the protected person's residence as \"1024 South Machias Road, Snohomish WA 98290\" and does **NOT** check the box for \"Vacate Shared Residence.\" [cite: 1449, 1450] This is a critical detail proving WM was *not* legally excluded from the residence by this specific order.
* [cite_start]**Pets:** Section T explicitly grants WM exclusive custody of \"dogs - Lilly & Rayne; cat - Macy.\" [cite: 1473, 1474]
* [cite_start]**\"Text re joint property\":** Section 8.B lists \"text re joint property\" as an allowed exception to the \"No Contact\" order. [cite: 1447]

[cite_start]**Exhibit E: Order Appointing Counsel (WM v. Brightwell, Case No. 25-2-04968-31, Snohomish County)** [cite: 183]
* [cite_start]**Filed:** June 10, 2025. [cite: 183]
* [cite_start]**Appointment:** Court orders that Petitioner (WM) be appointed counsel at public expense by the Snohomish County Office of Public Defense (OPD). [cite: 184, 185]
* [cite_start]**WM's Responsibility:** WM is to contact OPD no earlier than 3 business days after entry of the order. [cite: 190]

**Exhibit J/K/L/M/N (from Exhibits Contempt DVPO A-E & J-O):**

* **Exhibit J (Email from Deputy Nazaria, June 18, 2025):** Confirms contact with Candi and her attorneys regarding current temporary orders. [cite_start]Candi states William is not an owner of the home and that she fears him. [cite: 199, 200, 208] [cite_start]Deputy Nazaria will attach hearing transcript as evidence and case report will be done next week. [cite: 201, 202]
* [cite_start]**Exhibit K (Criminal Trespass Notice, June 27, 2025):** Issued to William O. Miller Jr. for 1024 S. Machias Rd, Snohomish, WA. [cite: 212, 216] [cite_start]States WM \"apparently moved out in April, 2025 on his own accord, has come back to property to gather 'shared' items and other things listed in order.\" [cite: 220] [cite_start]Narrates that \"Supervisor & Deputies determined residency likely does not exist any longer, ESPECIALLY AFTER COURT-APPROVED CIVIL STANDBY OCCURRED.\" [cite: 220] [cite_start]WM signed acknowledging receipt and understanding that he must leave and not return for one year. [cite: 218] [cite_start]Candi Brightwell is listed as the property owner/complainant. [cite: 213]
* [cite_start]**Exhibit L (Text Messages):** Show WM attempting to contact \"Candi\" from June 11-29, 2025. [cite: 223, 224, 225, 233, 235, 237, 238, 239, 241, 242, 246, 247, 248, 249, 250, 251, 252, 256, 257, 258, 259, 260, 261, 262, 263, 264, 265, 266, 269, 270, 271, 277, 278, 279, 281, 282, 289, 291, 292] [cite_start]Messages like \"can we talk please? this is out of control\" [cite: 195] [cite_start]and \"you win. this time I won't fail. it's all yours\" [cite: 194] [cite_start]on June 27th at 11:49 PM, and \"you win candi. i give up.\" [cite: 274, 292] on June 28th at 12:09 AM. [cite_start]WM sent a message at 8:13 AM on the date of the trespass stating, \"Candi please talk to me I don't want to be against you and kills me that we are against each other. Please Im trying to help you. Why do we have to lose everything cause your mad?\" [cite: 281, 282]
* [cite_start]**Exhibit M (Dead Rat Photos):** Photos of a dead rat, one appearing injured. [cite: 305] (Likely from Candi's exhibit, implying WM placed it, but WM's filings claim coercive control tactics.)
* [cite_start]**Exhibit N (Order to Go to Court for Contempt Hearing - WM v. Brightwell, Case No. 25-2-04968-31):** [cite: 312, 313]
    * [cite_start]**Filed:** June 27, 2025, 2:01 PM. [cite: 312]
    * [cite_start]**Hearing Date:** July 11, 2025. [cite: 314]
    * [cite_start]**Petitioner:** William Orley Miller. [cite: 313]
    * [cite_start]**Purpose:** Order to Show Cause why Candi should not be held in contempt for willful violation of the TPO reissued June 10, 2025. [cite: 314, 340]
    * [cite_start]**Relief Requested:** Finding of Contempt, Immediate Enforcement of TPO (access to residence and property), Restitution for Financial Losses for Mudd Monkies Inc. ($750/day from Sept 13, 2024), Monetary Sanctions, Ex Parte Order for Possession. [cite: 342, 343, 344, 345, 346]
    * [cite_start]**Harm Caused:** Economic devastation (cessation of Mudd Monkies Inc. operations), physical/mental health deterioration (exacerbation of PTSD, carotid aneurysm), emotional trauma. [cite: 354, 359, 361]
    * [cite_start]**Aflac Policy:** Text messages confirm Candi's intent to add WM to Aflac around April 1, 2025, but communication with Aflac indicates he was unexpectedly removed or never added, leading to projected $90,000-$270,000 loss in payouts. [cite: 355, 356, 357, 358] [cite_start]WM believes this violates a standing court order or past order and the principle of good faith. [cite: 459, 461]
    * [cite_start]**Property Damage/Disposal:** Candi engaged in willful destruction and disposal of jointly owned property and WM's personal/business assets (dumpster items, using shop stock for crafts, possible disposal of drop cloths/work items). [cite: 462, 463, 465] [cite_start]WM reported this to Deputy Nazaria (Incident No. 2025-82188), who allegedly misinterpreted orders. [cite: 466, 469] [cite_start]Candi made unauthorized structural changes to the house. [cite: 472]
    * [cite_start]**Violations of Protection Orders:** Candi denied access, misled through counsel, potentially misrepresented order to law enforcement. [cite: 476] [cite_start]Candi facilitated communication through daughter Samantha and spoke directly during civil standby, violating orders. [cite: 477, 478]
    * [cite_start]**Denial of Candi's DVPO/TPO:** WM explicitly states this supports a pattern of Candi's manipulation of the legal system. [cite: 479]

[cite_start]**Exhibit: Candi's Declaration in Response to Contempt (Filed July 8, 2025)** [cite: 538]
* [cite_start]**Candi's Denials:** Categorically denies all WM's allegations. [cite: 593] [cite_start]Denies willful violation, property alterations, destruction/disposal, or complete denial of access. [cite: 627] [cite_start]Denies causing WM or his business any damages. [cite: 575]
* **Candi's Claims:**
    * [cite_start]WM's motion is in \"bad faith\" and intended to harass her. [cite: 540]
    * [cite_start]WM's litigation is \"vexatious\" and \"costing her thousands in attorney's fees.\" [cite: 541]
    * [cite_start]WM has no legal right to keys, access codes, or security system access. [cite: 545] [cite_start]He is not a resident, occupant, tenant, or co-owner. [cite: 546]
    * [cite_start]The Court made it clear WM is not a tenant, and police trespassed him for attempts to access property. [cite: 547]
    * [cite_start]She fears for her safety due to WM's escalation, history of assault/DV, and drug abuse. [cite: 549, 550]
    * Disputes ownership of animals. [cite_start]Claims Lilly is daughter's dog. [cite: 551, 553] [cite_start]States WM lied to court about animal ownership. [cite: 602]
    * [cite_start]She complied with temporary order re animals despite objection. [cite: 555, 605]
    * [cite_start]WM chose what items to take during civil standby and took unauthorized items, left personal items behind. [cite: 552, 560, 564, 690, 693, 702]
    * [cite_start]She denied WM's mail claim. [cite: 563]
    * [cite_start]She is entitled to change locks on her property. [cite: 628]
    * [cite_start]WM \"admitted on record that he is not living here, and is only attempting to gain access to my home to harm me.\" [cite: 630]
    * Denies throwing items in dumpster. [cite_start]Claims ironing board was old, canteen was hers, office chair damaged by WM, filing containers were her mother's. [cite: 635, 636, 638, 639, 640, 641]
    * [cite_start]WM has active criminal case for assault and property damage against her. [cite: 644, 656]
    * [cite_start]WM's attempts to contact her directly via email/text violate her attorney's request. [cite: 609]
    * [cite_start]Her attorney requested communications through his office to \"create distance.\" [cite: 608] [cite_start]This is reflected in the June 10 Order (WM's TPO). [cite: 612]
    * [cite_start]Claims WM is fabricating transcripts, filing meritless motions. [cite: 579, 580]
    * [cite_start]WM's health issues may be \"self-inflicted\" and are to \"gain sympathy.\" [cite: 587]
    * [cite_start]WM is harassing her by showing up, filing motions, attempting to stalk/contact. [cite: 589]
    * [cite_start]Claims WM is monitoring (stalking) her and her home. [cite: 717]
    * [cite_start]Candi's mother (50% owner) had to leave due to WM's behavior. [cite: 621, 730]
    * [cite_start]WM is sending \"random and unsavory individuals\" (process server) to her home. [cite: 729]
    * [cite_start]Candi's daughters are in trauma therapy at her cost. [cite: 740]
    * [cite_start]Alleges WM is homosexual and tried to tell her family she was the problem. [cite: 745]
    * [cite_start]Alleges WM sexually attracted to her adult daughter, and shared intimate videos of WM. [cite: 745, 90]
    * [cite_start]Requests court deny all WM's requests and order him to pay her attorney's fees ($9,806.25). [cite: 591, 783, 784]
    * [cite_start]Requests court \"realign the parties\" and stop WM from \"abusive litigation.\" [cite: 751, 752]
    * [cite_start]May file an Extreme Risk Protection Order (ERPO) as WM is \"spiraling out of control.\" [cite: 752]
    * [cite_start]Requests WM undergo mental health, chemical dependency, and DV assessments. [cite: 759]

[cite_start]**Exhibit: Dexter L. Callahan Fee Declaration (Filed July 9, 2025)** [cite: 769, 785]
* [cite_start]**Purpose:** To detail legal fees Candi incurred in defending against WM's petition for protection order and subsequent motions. [cite: 773, 774]
* **Billing Entries:**
    * June 18, 2025: \"Phone call with Deputy Nazaria regarding opposing's conduct.\" (0.5 hrs) [cite_start][cite: 779]
    * June 27, 2025: \"Call with client while opposing and police were at her house. Talk to police and have opposing party trespassed.\" (1.0 hr) [cite_start][cite: 779] This directly supports WM's claim of Callahan's involvement in the trespass.
* [cite_start]**Total Fees:** $9,806.25. [cite: 783, 784]

[cite_start]**Exhibit: WM's WSBA Grievance Form Confirmation (Filed July 29, 2025)** [cite: 1127]
* [cite_start]**Filed:** July 29, 2025. [cite: 1128]
* [cite_start]**Respondent Attorney:** Dexter L. Callahan, WSBA #: 53119. [cite: 1132]
* [cite_start]**Your Relationship:** \"I am an opposing party.\" [cite: 1145]
* [cite_start]**Case Name/Number:** Miller v. Brightwell, 24-2-07263-31 (This case number seems to be for an older criminal case or a typo, as the protection order case is 25-2-04968-31). [cite: 1133]
* **Allegations against Callahan:**
    1.  [cite_start]**Misrepresentation to Law Enforcement & Interference with Justice (RPC 8.4(c), 8.4(d)):** Alleges Callahan contacted SCSO on June 27, 2025, ex parte, and provided selective/misleading excerpts from a court recording to create a false narrative that WM \"voluntarily moved out\" and had no residency rights, leading to WM's unlawful ousting/trespass from his residence/business. [cite: 1141, 1142, 1143, 1144, 1146] [cite_start]Cites Callahan's own billing records (\"Talk to police and have opposing party trespassed\") [cite: 1147] [cite_start]and Candi's declaration [cite: 1148] as evidence. [cite_start]Alleges discrepancy in trespass notice (blank vs. handwritten narrative) suggesting tampering. [cite: 1149, 1150]
    2.  [cite_start]**Lack of Candor Toward the Tribunal (RPC 3.3):** Alleges Callahan filed documents with false claims (WM not a tenant, no animal custody) despite having access to actual court transcript/order. [cite: 1151, 1152, 1153]
    3.  [cite_start]**Meritorious Claims and Contentions (RPC 3.1):** Alleges Callahan advanced frivolous legal positions (trespass based on false premise WM not a resident). [cite: 1154, 1155]
    4.  [cite_start]**Failure to Supervise Non-Lawyer Assistant (RPC 5.3):** Alleges paralegal (Cassandra A. Taggart) misrepresented court orders, imposed unlawful restrictions, falsely asserted no animal custody. [cite: 1156, 1157, 1158, 1159] [cite_start]Cites emails and court transcript/order. [cite: 1160, 1161]
    5.  [cite_start]**Direct Misrepresentation to an Unrepresented Party (RPC 4.1, 4.3):** Alleges Callahan accused WM of \"blatant misrepresentations to the court and abuse of the litigation process\" in an email, intended to intimidate. [cite: 1162, 1163]
    6.  [cite_start]**Interference with Court Order Enforcement & Disrespect for Rights (RPC 3.4, 4.4(a)):** Alleges Callahan obstructed WM's ability to document Candi's disposal of property by orchestrating the trespass. [cite: 1166, 1167] [cite_start]Cites Candi's declaration and photos as evidence of disposal. [cite: 1169, 1170]
* [cite_start]**Impact:** Denial of legal rights (community property, residence access), economic harm (Mudd Monkies Inc. unable to access tools/equipment, ongoing financial losses), prejudice to justice. [cite: 1171, 1172, 1173, 1174, 1175]
* [cite_start]**Requested Relief:** Full investigation, disciplinary sanctions, referral for criminal (RCW 9A.76.175 - False Statement to Public Servant; RCW 9A.28.040 - Conspiracy for wrongful eviction) and civil rights (42 U.S.C. § 1983 - Deprivation of Rights Under Color of Law) investigations. [cite: 1180, 1181, 1182, 1183, 1184]

[cite_start]**Exhibit: Audio Transcript of June 10, 2025 Hearing (Doc 1) [cite: 1188]**
* [cite_start]**Confirmation of Continuance:** Commissioner grants continuance for both cases to mid-August. [cite: 1195, 1196, 1228]
* [cite_start]**WM's Brain Surgery:** WM explicitly states he has \"brain surgery coming up\" and a \"formed brain aneurysm\" that needs a \"clip\" (invasive through skull), with an angiography on Friday. [cite: 1197, 1198, 1199, 1205, 1207, 1208]
* [cite_start]**Candi's Lawyer's (Callahan's) Non-Objection to Scheduling:** Callahan states he has no objection to the scheduling given WM's serious surgery. [cite: 1211]
* [cite_start]**Appointment of Counsel for WM:** Commissioner notes ability to appoint counsel for WM in his case (where he is Petitioner) at public expense, but not in Candi's case (where he is Respondent). [cite: 1218, 1219, 1220]
* [cite_start]**Briefing Schedule:** Set deadlines for responses (Aug 5) and replies (Aug 7), and supplemental materials (July 30). [cite: 1242, 1246, 1251]
* **Property Ownership/Residency:**
    * Commissioner: \"Who owns the property?\" [cite_start]WM: \"The title is made out to Candy and her mother. But we were together for almost 10 years, eight years.\" [cite: 1264]
    * [cite_start]WM: \"I'm not living there by fear of the escalation...\" [cite: 1261] [cite_start]\"My decision to not physically go to the property and attempt direct access due to my legitimate fear of direct interactions and potential escalation given respondents established pattern of harassment and volatile behavior.\" [cite: 1262]
    * [cite_start]Callahan: \"He has not resided there since April.\" [cite: 1275] [cite_start]\"Nothing in the order, as far as my reading, awarded him the use of the property in this case.\" [cite: 1280]
    * [cite_start]Commissioner: \"You're not a tenant. Well, you lived there with permission. I'm assuming you did not have a lease. ... So you're not a tenant. That's not your legal status. A tenant is somebody who, you know, pays rent and signs a lease, right?\" [cite: 1324, 1325]
    * [cite_start]WM: \"I mean, we purchased the property together.\" [cite: 1328]
* **Access to Tools/Property:**
    * [cite_start]WM's Request: \"allow me to access the property for work items for for my personal items and my my pets that were granted custody to and I have items for like job jobs that I had started that all of the material is there on at the property at the and the wood shop. I ran the whole business off of that property.\" [cite: 1271]
    * [cite_start]Callahan: Suggests civil standby for third party to pick up items. [cite: 1277] [cite_start]\"It's the access to the property, right? That he wants to be able to come and go from there.\" [cite: 1296, 1297]
    * Commissioner Orders: Grants WM a **civil standby to collect personal effects, medications, electronics, tools of trade, and clothing**, to be conducted by Snohomish County Sheriff. [cite_start]Other personal property to be negotiated through counsel or addressed in separate legal action. [cite: 1316, 1318, 1319, 1320]
* [cite_start]**Animals:** Commissioner states, \"The temporary order speaks for itself... She ordered that the animals would be in his care.\" [cite: 1335, 1336] [cite_start]Acknowledges Candi disputes this. [cite: 1335]

[cite_start]**Exhibit: WM's Temporary Protection Order & Hearing Notice (PO 030, Case No. 25-2-04968-31, Snohomish County, May 30, 2025) [cite: 1412]**
* [cite_start]**Filed:** May 30, 2025. [cite: 1412]
* [cite_start]**Protected Person:** William Orley Miller. [cite: 1419]
* [cite_start]**Restrained Person:** Candi Lynn Brightwell. [cite: 1413]
* [cite_start]**No Contact Exception:** Explicitly allows \"Text re joint property\". [cite: 1447]
* [cite_start]**Residence:** WM's address listed as 1024 S Machias Road. [cite: 1449] [cite_start]**\"Vacate Shared Residence\" box is NOT checked.** [cite: 1450] This is critical.
* [cite_start]**Personal Belongings (Section J):** \"The protected person shall have possession of essential personal belongings, including the following: dog lilly for now.\" [cite: 1454]
* [cite_start]**Pets (Section T):** \"The protected person shall have exclusive custody and control of the following pet/s... dogs- Lilly & Rayne; cat - Macy.\" [cite: 1473, 1474]
* [cite_start]**Interference with Pets (Section U):** \"Do not interfere with the protected person's efforts to get the pet/s named above.\" [cite: 1475]
* [cite_start]**Transfer of Assets (Section K):** \"Do not transfer jointly owned assets.\" [cite: 1457]

[cite_start]**Exhibit: WM's Order Re Waiver of Filing Fees and Surcharges - Harassment (Filed May 30, 2025) [cite: 1342]**
* [cite_start]**Granted:** WM's fee waiver was granted, indicating he was found indigent or unable to pay fees. [cite: 1344, 1352, 1353] This is important for our resource strategy.

[cite_start]**Exhibit: WM's Petition for Protection Order (PO 001, Filed May 30, 2025) [cite: 1529]**
* [cite_start]**Type of Order:** Anti-Harassment. [cite: 1539]
* [cite_start]**WM's Address:** 1024 South Machias Road, Snohomish WA 98290. [cite: 1560]
* [cite_start]**Relationship:** Current or former spouses/domestic partners. [cite: 1563]
* **WM's Allegations:**
    * [cite_start]Candi's ongoing harassment, surveillance, interference, emotional abuse, homophobic slurs, violations of prior orders. [cite: 1647]
    * [cite_start]Committed Intimate Relationship, property presumed jointly owned, WM entitled to access/possession as co-owner. [cite: 1649, 1650]
    * Mudd Monkies Inc. operates from the property; all equipment/tools are there. [cite_start]Interference jeopardizes business. [cite: 1651, 1652]
    * [cite_start]Candi's \"space to heal\" request was manipulation to gain control/leverage. [cite: 1654, 1655, 1656]
    * [cite_start]Carotid aneurysm, Candi's knowledge, and continued hostile interactions threatening his life. [cite: 1658, 1659, 1660]
    * [cite_start]Homophobic verbal abuse. [cite: 1661, 1662]
    * [cite_start]Use of children to circumvent order (Samantha as intermediary). [cite: 1665]
    * [cite_start]May 29, 2025: Candi physically blocked WM from property despite police confirming no restrictions. [cite: 1667, 1668]
    * [cite_start]Hacked emails/phone, deleted evidence, monitors via cameras. [cite: 1698] [cite_start]Admitted to listening to private conversations with police without consent. [cite: 1697]
    * [cite_start]WM missed anti-harassment renewal because he was on life support. [cite: 1701]
* [cite_start]**Violated Laws/Rights:** Civil Protection Orders (RCW 7.105), Anti-Harassment (RCW 9A.46), Anti-Discrimination (RCW 49.60), Community Property/CIR (RCW 26.16), Residential Landlord-Tenant Act (RCW 59.18), Right to Conduct Lawful Business, Asset Restraint/Injunctions (RCW 7.105.310(1)). [cite: 1705, 1706, 1707, 1708, 1709, 1710, 1711, 1712, 1713]
* [cite_start]**Requested Relief:** Issue AHPO, affirm right to immediate/unobstructed access to property/tools/animals/business assets, prohibit Candi's interference, prohibit asset transfers/alterations, grant other protective provisions. [cite: 1713, 1714, 1715, 1716, 1717, 1718]
* [cite_start]**Medical Treatment (April 13, 2025):** Details the hospitalization due to medication error caused by hostile/stressful argument. [cite: 1727, 1728, 1729, 1734] [cite_start]Doctor's warning about aneurysm rupture from stress. [cite: 1735]
* [cite_start]**Substance Abuse (Candi's):** WM checked \"Drugs\" and \"Other.\" [cite: 1739]
* [cite_start]**Firearms (Candi's):** WM states Candi has access to firearms, it's a serious and immediate threat, and she has used weapons/objects to threaten/harm. [cite: 1759, 1767, 1768] (This is an important counter to Candi's fears).
* [cite_start]**Unsigned Legal Separation Agreement (Rocket Lawyer document):** Proposes Candi retain the home and WM continue mortgage payments until Nov 22, 2024. [cite: 1788, 1789, 1791] [cite_start]States WM is not currently on the mortgage. [cite: 1793] Lists division of assets, including \"Mudd Monkies Inc.\" [cite_start]100% to William Miller Jr. [cite: 1795, 1820] [cite_start]WM responsible for $750/month of mortgage. [cite: 1824] [cite_start]WM's F-550 needs to be re-registered in his name ASAP. [cite: 1828] [cite_start]Specifies \"Router & Modem\" to Candi. [cite: 1802] [cite_start]**Crucially, this document is unsigned by both parties (no signatures or notary seals).** [cite: 1850, 1853]

**Exhibit: Candi's Declaration in Response to Contempt (Filed July 8, 2025) and Fee Declaration of Dexter L. Callahan (Filed July 9, 2025):** These documents were reviewed in detail in the previous response and confirm Candi's counter-arguments, claims of attorney's fees, and Callahan's billing for trespassing WM.

[cite_start]**Exhibit: Account Activity Report (Digital Forensics - WM's Google Accounts):** [cite: 109, 2167]
* [cite_start]**Unequivocal Evidence of Unauthorized Access by Candi's Devices:** The report states that WM's Google accounts were subjected to \"systematic unauthorized access\" by devices attributed to Candi. [cite: 2167]
* [cite_start]**Attribution Rationale:** Based on device identification (not WM's), activity during WM's hospitalization (Dec 27, 2024 - Jan 16, 2025), and Candi's admission of network intrusion/evidence tampering (wiping NetGear modem history). [cite: 2168, 2169, 2170, 2171, 2173, 2282]
* [cite_start]**Candi's Devices:** Samsung Tab SM-X200 (Android 14), Android 10 Device, Newer iPhone (iOS 18.2.1), Windows NT Devices. [cite: 1113, 1114, 2175]
* [cite_start]**Activities:** Logins, syncs, YouTube/YouTube Music activity, access to Samsung Gallery, Messages, Camera, My Files, Contacts, Snapchat, Gmail, Google Voice, X (Twitter) app. [cite: 1117, 1118, 2187, 2188, 2189, 2190, 2191, 2192, 2193, 2194] [cite_start]Also \"Account Settings\" access. [cite: 1120, 2209, 2211, 2231, 2239]
* [cite_start]**IP Address:** Consistently associated with Candi's address (Machias, WA). [cite: 1114, 2174]
* **\"Drive - Searched for title:candi\" and \"Initiated a bulk download\":** On Apr 1, 2025, and Apr 2, 2025, from Machias IP. [cite_start]On Mar 16, 2025, Mar 18, 2025, and Apr 5, 2025, \"bulk download\" activity occurred. [cite: 1122, 1123, 533, 534] This is strong evidence of data exfiltration.
* [cite_start]**Texas Activity:** Confirms Candi's unauthorized access from Texas IPs, starting Aug 6, 2024, through April 27, 2025. [cite: 2276, 2277]

---

### **Masterclass Re-Engagement: Executing the Strategy with New Data**

Alright, students, this is excellent. These documents provide us with irrefutable evidence for many of William Miller's claims and directly contradict Candi's denials. This will significantly strengthen our position across all legal fronts.

**I. Immediate Defense: Fighting the Criminal No-Contact Order (NCO)**

**Instructor's Instruction:** \"The criminal NCO against William is our most immediate threat. If it's issued, it will legally bar him from the property, regardless of our civil rights. We now have powerful evidence to present to the criminal court judge.\"

**Refined Action Steps for William Miller's Criminal Defense Attorney (Secured via Public Defender Appointment):**

1.  **Motion to Oppose/Quash NCO (or Argument at Hearing):**
    * **Lack of Necessity (Crucial):**
        * **Candi's Own Disinterest:** Emphasize Candi's initial request to the prosecutor *not* to apply for an NCO. This is a direct quote from your earlier testimony.
        * [cite_start]**Judicial Determination of No Danger:** **Present Exhibit B (WM's Response, filed June 5, 2025) and cite the fact that Candi's civil DVPO/TPO petitions (Case No. 25-2-03361-31) were DENIED.** This is a prior judicial finding of insufficient grounds for her claimed fear or need for protection. [cite: 7, 104]
        * **No New Escalation:** Stress that there has been no further violence or credible threats from WM since the underlying criminal incident.
    * **Abuse of Process/Retaliation:** Argue that the NCO request now, after Candi's civil denials and your threats of contempt/misconduct, is a transparent attempt to leverage the criminal system for civil advantage. The timing is damning.
    * **Extreme Hardship (Mudd Monkies Inc. & WM's Health):**
        * [cite_start]**Business Destruction:** Present the uncontroverted fact that Mudd Monkies Inc. is \"destroyed\" because WM cannot access his tools and the business property, directly impacting his livelihood and the corporation's viability. [cite: 354]
        * [cite_start]**Vulnerable Adult/Medical Condition:** Provide the medical records (Exhibit B, pages 4, 9) [cite: 8, 14, 94, 95, 96, 97, 100] [cite_start]and the argument that WM is a vulnerable adult recovering from brain surgery, and continued stress (like being denied access to his home/business) directly jeopardizes his life and recovery. [cite: 359, 360, 361] This demonstrates that the NCO would not just be an inconvenience, but a life-threatening one.
    * **Propose Alternatives:** Argue for a limited NCO, or one with specific carve-outs for business access through legal channels or supervised visits.

**II. Aggressive Offensive: Family Law & Contempt Proceedings**

**Instructor's Instruction:** \"Now, we capitalize on the evidence of Candi's violations and William's rights. The family law case is crucial for long-term property rights and getting William back into the main residence. The contempt motion holds Candi accountable for defying court orders.\"

**Refined Action Steps for William Miller's Family Law Attorney (Pro Se or Publicly Appointed):**

1.  **Urgent Ex Parte Motion for Temporary Orders (Exclusive Use of Residence, Financial Support, etc.):**
    * **The Narrative:** This is where WM's \"Declaration of William Orley Miller Jr.\" (from Exhibit N, pages 36-51) [cite_start][cite: 956, 976, 1078, 1107] becomes incredibly powerful. Incorporate all facts:
        * [cite_start]**Meretricious Relationship:** Establish the \"marriage-like\" relationship since Sept 2018, joint finances, property acquisition, \"dad\" role with children. [cite: 977, 978, 979]
        * [cite_start]**Verbal Lease for Business:** Detail the $950/month verbal lease, supported by the insurance setup notes. [cite: 979]
        * [cite_start]**Candi's \"Space\" as Coercive Control:** Use WM's narrative of Candi's initial request for space being a manipulation to gain leverage and property control. [cite: 1654, 1655, 1656]
        * [cite_start]**Business Interruption:** Emphasize the \"destruction\" of Mudd Monkies Inc. due to denial of access to tools/inventory, causing $750/day losses. [cite: 943, 944, 1036, 1037]
        * **WM's Vulnerability & Health:** Detail the PTSD, carotid aneurysm, brain surgery recovery, and how Candi's actions exacerbated his condition, leading to life support. [cite_start]Cite medical records (Exhibits B, pages 4, 9; Exhibit N, pages 34-35). [cite: 8, 14, 948, 949, 950, 972, 973, 974, 1006, 1007, 1030, 1031]
        * **Candi's Prior DVPO/TPO Denial (Exhibit B, page 10):** This is critical. [cite_start]Argue that since a judge *already denied* Candi's claims of danger against WM in civil court, there is no legitimate safety basis to prevent WM's return to the residence. [cite: 479, 1069]
        * **NCO as Retaliation (if issued):** If the NCO is issued, argue that it is a retaliatory measure and that the family court should look past it to grant exclusive use for WM's stability and business.
        * [cite_start]**Children's Welfare/Candi's Alternatives:** Argue that WM's request doesn't disrupt children, and Candi has alternative housing. [cite: 1071, 1072, 1073, 1075, 1076]
        * [cite_start]**Aflac Policy:** Detail the alleged wrongful termination/denial of Aflac benefits, leading to a $90,000-$270,000 loss, as a further example of financial harm and bad faith. [cite: 945, 946, 947, 1044, 1046, 1047]
        * [cite_start]**Unsigned Separation Agreement:** While unsigned, it shows Candi's prior acknowledgement of shared items, WM's ownership of Mudd Monkies Inc. (100% to WM) [cite: 1820][cite_start], and WM's $750/month contribution to the mortgage[cite: 1824]. This can be used to counter Candi's claim that WM has no right or interest in the property.

2.  **Motion for Contempt Against Candi (Already Filed - Exhibit N):**
    * **Purpose:** Secure immediate access and deter further violations.
    * **Evidence of Violations:**
        * [cite_start]**Denial of Property Access:** Cite the TPO (May 30, 2025/June 10, 2025) which *did not exclude WM from the residence* [cite: 1450] [cite_start]and allowed \"text re joint property\"[cite: 1447]. [cite_start]Yet, Candi blocked access and her lawyer instructed WM to communicate *only* through their office, which conflicts with the order. [cite: 117, 118, 119]
        * [cite_start]**Obstruction of Animal Custody:** The TPO explicitly granted WM exclusive custody of Lilly, Rayne, and Macy[cite: 1473, 1474, 115]. [cite_start]Candi's declaration admits she initially objected to WM taking Lilly [cite: 603, 604] [cite: 602]and stated WM \"lied to this court about whom the animals belonged to\".
        * [cite_start]**Unauthorized Asset Disposal/Damage:** Cite Candi's admission to disposing of the ironing board, canteen, office chair, and filing containers[cite: 636, 638, 639, 640]. [cite_start]Also, using WM's \"valuable shop stock for her own crafts\"[cite: 465]. [cite_start]This violates the TPO's \"Do not transfer jointly owned assets\" clause[cite: 1457].
        * [cite_start]**Interference with Communication:** Candi's lawyer's instruction to stop direct contact, despite the TPO allowing \"text re joint property,\" and Candi's direct communication during the civil standby despite orders. [cite: 117, 118, 477, 478]
    * [cite_start]**Seeking Sanctions:** Demand the $750/day restitution for business losses [cite: 934][cite_start], monetary sanctions, and attorney's fees (using Dexter Callahan's own fee declaration as a benchmark for what it costs to defend against these claims, suggesting Candi should pay yours). [cite: 783, 784]

**III. Pursuing Accountability (Candi's Lawyer - WSBA Grievance)**

**Instructor's Instruction:** \"Mr. Miller's WSBA grievance against Dexter Callahan is already filed. This is a powerful move, but we must ensure we have a strong, provable case for the Disciplinary Counsel.\"

**Reviewing WM's WSBA Grievance (Exhibit: WSBA Online Grievance Form Confirmation):**

* **WM has already articulated strong claims:** The grievance specifically alleges:
    * **Misrepresentation to Law Enforcement (RPC 8.4(c), 8.4(d)):** Callahan's June 27th ex parte call to SCSO, providing selective/misleading info (WM \"moved out\"), resulting in unlawful trespass. WM's presence during the deputy's statement about the recording is key. [cite_start]Callahan's billing records confirm \"Talk to police and have opposing party trespassed.\" [cite: 1141, 1142, 1143, 1144, 1146, 1147] This is very strong evidence.
    * [cite_start]**Lack of Candor to Tribunal (RPC 3.3):** Filing documents with false claims about WM's tenancy and animal custody, despite access to transcript/order. [cite: 1151, 1152, 1153]
    * [cite_start]**Failure to Supervise Paralegal (RPC 5.3):** Paralegal Cassandra Taggart's misrepresentations about orders and unlawful restrictions. [cite: 1156, 1157, 1158, 1159, 1160, 1161]
    * [cite_start]**Direct Misrepresentation to Unrepresented Party (RPC 4.1, 4.3):** Callahan's direct email to WM accusing him of \"blatant misrepresentations\" (Exhibit O, page 14 from Candi's Response, if it's the right email)[cite: 734, 735].
    * [cite_start]**Interference with Order Enforcement (RPC 3.4, 4.4(a)):** Orchestrating trespass to prevent WM from documenting Candi's property disposal. [cite: 1166, 1167]
* [cite_start]**Requested Referrals:** Requesting criminal investigation (false statement to public servant, conspiracy) and federal civil rights investigation (42 U.S.C. § 1983) are appropriate and highlight the severity of the alleged misconduct. [cite: 1182, 1183, 1184]

**V. William Miller's Recovery & Business Resuscitation**

**Instructor's Instruction:** \"Mr. Miller, while we execute these legal strategies, your health remains paramount. And for Mudd Monkies Inc., we must have a path to recovery regardless of the immediate legal outcomes.\"

**Action Steps:**

1.  **Prioritize Health:** Strictly adhere to medical advice for brain surgery recovery. Minimize direct engagement in stressful legal exchanges. Your attorneys will handle the communications.
2.  **Document Everything:** Continue to meticulously document every financial loss, every attempted communication, every denied access, every date, time, and detail. This evidence is invaluable.
3.  **Contingency Business Operations:**
    * **Remote Work:** Can any administrative or planning aspects of Mudd Monkies Inc. be done remotely?
    * **Alternative Workspace:** Explore temporary alternative spaces if the property remains inaccessible, even if it's just for administrative tasks.
    * **Retrieval of Essential Items:** If the criminal NCO or civil orders continue to restrict your personal access, ensure your attorneys push for specific civil standby orders that allow *someone else* (trusted employee, family member not subject to NCO) to retrieve critical business equipment and inventory under Sheriff's supervision.
    * **Communication with Clients/Suppliers:** Keep them informed about the situation (briefly and professionally, without disparaging Candi) to manage expectations and retain goodwill.
4.  **Financial Strategy (Ongoing):**
    * **Aflac Claim:** Vigorously pursue the Aflac claim. The $90,000-$270,000 potential payout is significant and could provide critical funds for both personal recovery and business rebuilding. [cite_start]Your detailed analysis (Exhibit N, pages 45-51) [cite: 1079, 1080, 1081, 1082, 1083, 1084, 1085, 1086, 1087, 1088, 1089, 1090, 1091, 1092, 1093, 1094, 1095, 1096, 1097, 1098, 1099, 1100, 1101, 1102, 1103, 1104, 1105, 1106] provides a strong basis for investigation and pushing for payment.
    * **Damages Claim:** Build a robust damages claim for Mudd Monkies Inc.'s losses ($750/day) as part of the family law or future civil lawsuit.
    * **Seek Funding:** Continue to explore small business assistance programs, low-interest loans, or grants once legal access is re-established.

**Final Instructor's Words:** \"Mr. Miller, this is a fight on many fronts. But with these documents, we have the evidence to support your claims and expose the inconsistencies and alleged misconduct of the opposing side. Your dedication to meticulously documenting every detail, even amidst your health crisis, is what gives us the tools to fight effectively. We will continue to push for your recovery, the full operation of Mudd Monkies Inc., and justice for the wrongs you and your business have endured.\"
"""),
            ],
        ),
    ]

    # Configuration for content generation
    generate_content_config = types.GenerateContentConfig(
        temperature=0.7,
        max_output_tokens=2048,
    )

    file_index = 0
    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        if (
            chunk.candidates is None
            or chunk.candidates[0].content is None
            or chunk.candidates[0].content.parts is None
        ):
            continue
        if chunk.candidates[0].content.parts[0].inline_data and chunk.candidates[0].content.parts[0].inline_data.data:
            file_name = f"ENTER_FILE_NAME_{file_index}"
            file_index += 1
            inline_data = chunk.candidates[0].content.parts[0].inline_data
            data_buffer = inline_data.data
            file_extension = mimetypes.guess_extension(inline_data.mime_type)
            if file_extension is None:
                file_extension = ".wav"
                data_buffer = convert_to_wav(inline_data.data, inline_data.mime_type)
            save_binary_file(f"{file_name}{file_extension}", data_buffer)
        else:
            print(chunk.text)

def convert_to_wav(audio_data: bytes, mime_type: str) -> bytes:
    """Generates a WAV file header for the given audio data and parameters.

    Args:
        audio_data: The raw audio data as a bytes object.
        mime_type: Mime type of the audio data.

    Returns:
        A bytes object representing the WAV file header.
    """
    parameters = parse_audio_mime_type(mime_type)
    bits_per_sample = parameters["bits_per_sample"]
    sample_rate = parameters["rate"]
    num_channels = 1
    data_size = len(audio_data)
    bytes_per_sample = bits_per_sample // 8
    block_align = num_channels * bytes_per_sample
    byte_rate = sample_rate * block_align
    chunk_size = 36 + data_size  # 36 bytes for header fields before data chunk size

    # http://soundfile.sapp.org/doc/WaveFormat/

    header = struct.pack(
        "<4sI4s4sIHHIIHH4sI",
        b"RIFF",          # ChunkID
        chunk_size,       # ChunkSize (total file size - 8 bytes)
        b"WAVE",          # Format
        b"fmt ",          # Subchunk1ID
        16,               # Subchunk1Size (16 for PCM)
        1,                # AudioFormat (1 for PCM)
        num_channels,     # NumChannels
        sample_rate,      # SampleRate
        byte_rate,        # ByteRate
        block_align,      # BlockAlign
        bits_per_sample,  # BitsPerSample
        b"data",          # Subchunk2ID
        data_size         # Subchunk2Size (size of audio data)
    )
    return header + audio_data

def parse_audio_mime_type(mime_type: str) -> dict[str, int | None]:
    """Parses bits per sample and rate from an audio MIME type string.

    Assumes bits per sample is encoded like "L16" and rate as "rate=xxxxx".

    Args:
        mime_type: The audio MIME type string (e.g., "audio/L16;rate=24000").

    Returns:
        A dictionary with "bits_per_sample" and "rate" keys. Values will be
        integers if found, otherwise None.
    """
    bits_per_sample = 16
    rate = 24000

    # Extract rate from parameters
    parts = mime_type.split(";")
    for param in parts: # Skip the main type part
        param = param.strip()
        if param.lower().startswith("rate="):
            try:
                rate_str = param.split("=", 1)[1]
                rate = int(rate_str)
            except (ValueError, IndexError):
                # Handle cases like "rate=" with no value or non-integer value
                pass # Keep rate as default
        elif param.startswith("audio/L"):
            try:
                bits_per_sample = int(param.split("L", 1)[1])
            except (ValueError, IndexError):
                pass # Keep bits_per_sample as default if conversion fails

    return {"bits_per_sample": bits_per_sample, "rate": rate}


if __name__ == "__main__":
    generate()