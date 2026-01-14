from flask import Flask, request, jsonify
from flask_cors import CORS
from nlp_core import process_query

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "Enterprise Agentic Assistant Backend Running"

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(force=True, silent=True)

    if not data or "message" not in data:
        return jsonify({"answer": "Invalid request"}), 400

    try:
        result = process_query(data["message"])
        return jsonify(result)
    except Exception as e:
        return jsonify({"answer": "Backend error", "error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)
