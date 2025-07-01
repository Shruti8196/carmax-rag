from flask import Flask, request, jsonify
from src.retriever import FAQRetriever
from src.generator import generate_answer
from src.memory import init_db
from flask_cors import CORS  # Optional: allows frontend devs to test cross-origin
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all domains (or restrict in prod)

init_db()
retriever = FAQRetriever()

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    query = data.get("query")
    session_id = data.get("session_id")

    if not query or not session_id:
        return jsonify({"error": "Missing 'query' or 'session_id'"}), 400

    faqs = retriever.retrieve(query)
    answer = generate_answer(query, faqs, session_id=session_id)

    return jsonify({
        "answer": answer,
        "session_id": session_id,
    })

@app.route("/healthz", methods=["GET"])
def health_check():
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port, debug=True)
