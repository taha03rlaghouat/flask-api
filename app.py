from flask import Flask, request, jsonify
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
import os

# تحميل قاموس WordNet إذا لم يكن محمّلًا
try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet')
    nltk.download('omw-1.4')  # دعم اللغات الأخرى

# إعداد الواجهة
app = Flask(__name__)
lemmatizer = WordNetLemmatizer()

@app.route("/")
def home():
    return "✅ Flask API with NLTK lemmatization is live!"

@app.route('/analyze', methods=['POST'])
def analyze_text():
    data = request.get_json()
    text = data.get("text", "")
    tokens = text.split()  # يمكنك استخدام spaCy إذا أردت تحليلًا أدق

    result = []
    for token in tokens:
        lemma = lemmatizer.lemmatize(token)
        result.append({
            "text": token,
            "lemma": lemma
        })

    return jsonify({
        "input": text,
        "tokens": result
    })

if __name__ == "__main__":
    app.run()
