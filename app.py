from flask import Flask, request, jsonify
import spacy
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet

# تحميل النماذج إن لم تكن موجودة
try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet')
    nltk.download('omw-1.4')

nlp = spacy.load("en_core_web_sm")
lemmatizer = WordNetLemmatizer()
app = Flask(__name__)

# دالة لتحويل POS من spaCy إلى WordNet
def get_wordnet_pos(spacy_pos):
    if spacy_pos.startswith('V'):
        return wordnet.VERB
    elif spacy_pos.startswith('N'):
        return wordnet.NOUN
    elif spacy_pos.startswith('J'):
        return wordnet.ADJ
    elif spacy_pos.startswith('R'):
        return wordnet.ADV
    else:
        return wordnet.NOUN  # افتراضيًا noun

@app.route("/")
def home():
    return "✅ Flask API using spaCy + NLTK is live!"

@app.route('/analyze', methods=['POST'])
def analyze_text():
    data = request.get_json()
    text = data.get("text", "")
    doc = nlp(text)

    result = []
    for token in doc:
        wn_pos = get_wordnet_pos(token.tag_)  # استخدم tag_ وليس pos_
        lemma = lemmatizer.lemmatize(token.text, wn_pos)

        result.append({
            "text": token.text,
            "lemma_spacy": token.lemma_,
            "lemma_nltk": lemma,
            "pos": token.pos_,
            "tag": token.tag_,
            "dep": token.dep_,
            "head": token.head.text
        })

    return jsonify({
        "input": text,
        "tokens": result
    })

if __name__ == "__main__":
    app.run()
