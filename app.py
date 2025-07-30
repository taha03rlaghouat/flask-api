from flask import Flask, request, jsonify
import spacy
from nltk.stem import PorterStemmer
import nltk

# تأكد من تحميل بيانات nltk الضرورية
nltk.download('punkt')

# تحميل نموذج spaCy
nlp = spacy.load("en_core_web_sm")
stemmer = PorterStemmer()

app = Flask(__name__)

@app.route("/")
def home():
    return "✅ Flask API with stemming is live!"

@app.route('/analyze', methods=['POST'])
def analyze_text():
    data = request.get_json()
    text = data.get("text", "")
    doc = nlp(text)

    result = []
    for token in doc:
        result.append({
            "text": token.text,
            "lemma": token.lemma_,
            "stem": stemmer.stem(token.text),
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
