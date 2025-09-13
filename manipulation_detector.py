import spacy
from textblob import TextBlob

nlp = spacy.load("en_core_web_sm")
text = "Paste your evidence text here..."

doc = nlp(text)
for sent in doc.sents:
    polarity = TextBlob(sent.text).sentiment.polarity
    print(f"{sent.text} - Polarity: {polarity}")

# Add pattern matchers for coercive control, stonewalling detection, etc. as needed
