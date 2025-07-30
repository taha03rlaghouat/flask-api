from flask import Flask, request, jsonify
import spacy

nlp = spacy.load("en_core_web_sm")

app = Flask(__name__)
@app.route("/")
def home():
    return "✅ Flask API is live on Render!"

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
