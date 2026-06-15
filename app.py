"""
app.py — Flask bridge server
Connects smart_farmer_ui.html with your existing backend.py

Install:  pip install flask flask-cors
Run:      python app.py
Then open: smart_farmer_ui.html in Chrome
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import tempfile
from config import  marketing_key


from backend import (
    chatbot_response,
    get_weather,
    detect_disease,
    detect_language,
)

app = Flask(__name__)
CORS(app)  # Allows HTML file to call this server


# ─── CHAT ENDPOINT ───────────────────────────────────
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    question = data.get("question", "").strip()

    if not question:
        return jsonify({"answer": "Please enter a question."})

    answer = chatbot_response(question)
    return jsonify({"answer": answer})


# ─── WEATHER ENDPOINT ────────────────────────────────
@app.route("/weather", methods=["GET"])
def weather():
    city = request.args.get("city", "Pune")
    language = request.args.get("lang", "english")

    data = get_weather(city, language)

    if data is None:
        return jsonify({"error": "City not found"}), 404

    return jsonify(data)


# ─── DISEASE DETECTION ENDPOINT ──────────────────────
@app.route("/detect", methods=["POST"])
def detect():
    if "image" not in request.files:
        return jsonify({"result": "No image uploaded."}), 400

    file = request.files["image"]

    # Save temporarily
    suffix = os.path.splitext(file.filename)[1] or ".jpg"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        file.save(tmp.name)
        tmp_path = tmp.name

    # Detect language from Accept-Language header (optional)
    language = request.args.get("lang", "english")

    result = detect_disease(tmp_path, language)

    # Cleanup temp file
    try:
        os.unlink(tmp_path)
    except Exception:
        pass

    return jsonify({"result": result})



@app.route("/market-key", methods=["GET"])
def market_key():
    return jsonify({"key": marketing_key})

# ─── RUN ─────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 50)
    print("🌾 Smart Farmer Assistant Server")
    print("   Running at: http://localhost:5000")
    print("   Open smart_farmer_ui.html in Chrome")
    print("=" * 50)
    app.run(debug=True, port=5000)
