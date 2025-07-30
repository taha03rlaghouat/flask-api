from flask import Flask, request, jsonify
import spacy
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet

# تحميل ملفات WordNet إذا لم تكن موجودة
try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet')
    nltk.download('omw-1.4')

nlp = spacy.load("en_core_web_sm")
lemmatizer = WordNetLemmatizer()
app = Flask(__name__)

# تحويل spaCy POS إلى WordNet POS
def get_wordnet_pos(spacy_tag):
    if spacy_tag.startswith("J"):
        return wordnet.ADJ
    elif spacy_tag.startswith("V"):
        return wordnet.VERB
    elif spacy_tag.startswith("N"):
        return wordnet.NOUN
    elif spacy_tag.startswith("R"):
        return wordnet.ADV
    else:
        return wordnet.NOUN  # افتراضيًا noun

@app.route("/")
def home():
    return "✅ Flask NLP API is live!"

@app.route('/analyze', methods=['POST'])
def analyze_text():
    data = request.get_json()
    text = data.get("text", "")
  

    # معالجة النصوص الطويلة
    if not text or len(text.strip()) == 0:
        return jsonify({"error": "No text provided"}), 400
    if len(text) > 100000:
        return jsonify({"error": "Text too long (limit: 100,000 characters)"}), 413

    doc = nlp(text)

    result = []
    for token in doc:
        wn_pos = get_wordnet_pos(token.tag_)
        lemma_nltk = lemmatizer.lemmatize(token.text, wn_pos)
        result.append({
            "text": token.text,
            "lemma_spacy": token.lemma_,
             "lemma_nltk": lemma_nltk,
            "pos": token.pos_,
            "tag": token.tag_,
            "dep": token.dep_,
            "head": token.head.text
        })

    return jsonify({
       "input_snippet": text[:200] + "..." if len(text) > 200 else text,
"full_input_length": len(text),

        "tokens": result
    })


if __name__ == "__main__":
    app.run()
