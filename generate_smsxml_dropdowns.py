
import xml.etree.ElementTree as ET
import os
import glob
import webbrowser
from textblob import TextBlob
import whisper

# Scan Downloads for all SMS XML files and video files
xml_files = glob.glob(os.path.join(os.getcwd(), "sms-*.xml"))
video_files = glob.glob(os.path.join(os.getcwd(), "*.mp4")) + glob.glob(os.path.join(os.getcwd(), "*.avi")) + glob.glob(os.path.join(os.getcwd(), "*.mov"))

def is_coercive_control(text):
    # Conceptual analysis for coercive control patterns
    text_lower = text.lower()
    
    # Patterns for different types of coercive control
    patterns = {
        'threats_violence': ['kill', 'hurt', 'threat', 'f***', 'bitch', 'disgusting', 'pain', 'walk away', 'ghetto', 'start s***'],
        'emotional_manipulation': ['manipulate', 'control', 'fix yourself', 'time machine', 'disgusting', 'inside and out', 'fix everything'],
        'isolation': ['isolate', 'alone', 'no one', 'cut off', 'separate'],
        'gaslighting': ['crazy', 'fantasy', 'lie', 'not real', 'imagining'],
        'financial_control': ['money', 'pay', 'debt', 'control finances'],
        'surveillance': ['watch', 'track', 'follow', 'spy'],
        'repetitive_abuse': ['stupid', 'idiot', 'worthless', 'hate you']
    }
    
    flagged_types = []
    for category, keywords in patterns.items():
        if any(kw in text_lower for kw in keywords):
            flagged_types.append(category)
    
    # Additional conceptual checks
    if len(text.split()) > 50:  # Long rants often indicate emotional dumping
        flagged_types.append('emotional_dumping')
    if 'you' in text_lower and ('always' in text_lower or 'never' in text_lower):  # Blame shifting
        flagged_types.append('blame_shifting')
    if any(word in text_lower for word in ['i hate', 'you disgust', 'you make me']):  # Direct insults
        flagged_types.append('direct_insult')
    
    return flagged_types if flagged_types else None

def extract_sms_details(xml_path, max_count=100):
    messages = []
    count = 0
    for event, elem in ET.iterparse(xml_path, events=("end",)):
        if elem.tag == "sms":
            body = elem.attrib.get("body", "(No body)")
            sender = elem.attrib.get("address", "(No sender)")
            date = elem.attrib.get("readable_date", "(No date)")
            blob = TextBlob(body)
            sentiment = blob.sentiment
            polarity = sentiment.polarity  # -1 to 1
            subjectivity = sentiment.subjectivity  # 0 to 1
            sentiment_label = 'positive' if polarity > 0.1 else 'negative' if polarity < -0.1 else 'neutral'
            messages.append({
                'date': date,
                'sender': sender,
                'body': body,
                'flagged_types': is_coercive_control(body),
                'sentiment': sentiment_label,
                'polarity': polarity,
                'subjectivity': subjectivity
            })
            count += 1
            if count >= max_count:
                break
        elem.clear()
    return messages

def transcribe_video(video_path):
    try:
        model = whisper.load_model("base")
        result = model.transcribe(video_path)
        return result["text"]
    except Exception as e:
        return f"Transcription failed: {str(e)}"

html = """
<!DOCTYPE html>
<html>
<head>
    <title>SMSXML Dropdowns with Coercive Control Analysis</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        .dropdown { margin-bottom: 30px; }
        .flagged { background-color: #ffcccc; }
        .normal { background-color: #ccffcc; }
    </style>
</head>
<body>
    <h1>SMSXML Dropdowns with Coercive Control Analysis</h1>
"""

if not xml_files and not video_files:
    html += "<p>No SMS XML or video files found in Downloads folder.</p>"
else:
    # Process XML files
    for xml_file in xml_files:
        messages = extract_sms_details(xml_file)
        file_name = os.path.basename(xml_file)
        html += f'<div class="dropdown"><h3>{file_name} (SMS)</h3><div style="max-height:400px; overflow-y:scroll; border:1px solid #ccc; padding:10px;">'
        for msg in messages:
            if msg['flagged_types']:
                types_str = ', '.join(msg['flagged_types'])
                html += f'<p style="background-color:#ffcccc;"><strong>FLAGGED: {types_str}</strong> [Sentiment: {msg["sentiment"]}] {msg["date"]} | {msg["sender"]}: {msg["body"]}</p>'
            else:
                html += f'<p style="background-color:#ccffcc;">[Sentiment: {msg["sentiment"]}] {msg["date"]} | {msg["sender"]}: {msg["body"]}</p>'
        html += '</div></div>'
    
    # Process video files
    for video_file in video_files:
        transcript = transcribe_video(video_file)
        file_name = os.path.basename(video_file)
        flagged_types = is_coercive_control(transcript)
        blob = TextBlob(transcript)
        sentiment = blob.sentiment
        sentiment_label = 'positive' if sentiment.polarity > 0.1 else 'negative' if sentiment.polarity < -0.1 else 'neutral'
        html += f'<div class="dropdown"><h3>{file_name} (Video Transcript)</h3><div style="max-height:400px; overflow-y:scroll; border:1px solid #ccc; padding:10px;">'
        if flagged_types:
            html += f'<p style="background-color:#ffcccc;"><strong>FLAGGED: {", ".join(flagged_types)}</strong> [Sentiment: {sentiment_label}] {transcript}</p>'
        else:
            html += f'<p style="background-color:#ccffcc;">[Sentiment: {sentiment_label}] {transcript}</p>'
        html += '</div></div>'

html += """
</body>
</html>
"""

# Save HTML file
output_path = os.path.join(os.getcwd(), "smsxml_dropdowns.html")
with open(output_path, "w", encoding="utf-8") as f:
    f.write(html)

print(f"HTML file created: {output_path}")
webbrowser.open(f"file://{output_path}")
