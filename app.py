"""
app.py — Flask bridge server
Connects smart_farmer_ui.html with your existing backend.py

Install:
    pip install flask flask-cors

Run:
    python app.py
"""

from flask import Flask, request, jsonify, send_from_directory, session
from flask_cors import CORS
import os
import tempfile
import sqlite3
from datetime import timedelta


from backend import (
    chatbot_response,
    get_weather,
    detect_disease,
    get_weather_by_coords,
)

app = Flask(__name__)
app.secret_key = "shetkari_secret_key_123" # Session के लिए आवश्यक
CORS(app, supports_credentials=True)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=30)


@app.route("/")
def index():
    return send_from_directory(".", "smart_farmer_ui.html")


# -------------------- CHAT --------------------

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()

    if not data:
        return jsonify({"answer": "Invalid request."}), 400

    question = data.get("question", "").strip()

    if not question:
        return jsonify({"answer": "Please enter a question."}), 400

    answer = chatbot_response(question)

    # अगर किसान लॉगिन है, तो चैट 'chatbot.db' में सेव होगी
    user_mobile = session.get("user_mobile")
    if user_mobile:
        try:
            conn = sqlite3.connect("chatbot.db")
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO chat_history (mobile, question, answer) VALUES (?, ?, ?)",
                (user_mobile, question, answer)
            )
            conn.commit()
            conn.close()
        except Exception as e:
            print("History Save Error:", e)

    return jsonify({"answer": answer})


# -------------------- WEATHER --------------------

@app.route("/weather", methods=["GET"])
def weather():
    city = request.args.get("city", "Ahmednagar")
    language = request.args.get("lang", "english")

    data = get_weather(city, language)

    if data is None:
        return jsonify({"error": "City not found"}), 404

    return jsonify(data)


@app.route("/weather-coords", methods=["GET"])
def weather_coords():
    lat = request.args.get("lat")
    lon = request.args.get("lon")

    if not lat or not lon:
        return jsonify({"error": "Latitude and longitude required"}), 400

    data = get_weather_by_coords(lat, lon, "english")

    if data is None:
        return jsonify({"error": "Weather not found"}), 404

    return jsonify(data)


# -------------------- DISEASE DETECTION --------------------

@app.route("/detect", methods=["POST"])
def detect():
    if "image" not in request.files:
        return jsonify({"result": "No image uploaded."}), 400

    file = request.files["image"]

    suffix = os.path.splitext(file.filename)[1] or ".jpg"

    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        file.save(tmp.name)
        tmp_path = tmp.name

    language = request.args.get("lang", "english")
    result = detect_disease(tmp_path, language)

    try:
        os.unlink(tmp_path)
    except Exception:
        pass

    return jsonify({"result": result})


# -------------------- AUTH & HISTORY (NEW ADDED) --------------------

@app.route("/register", methods=["POST"])
def register():
    data = request.get_json() or {}
    name = data.get("name", "").strip()
    mobile = data.get("mobile", "").strip()
    district = data.get("district", "").strip()
    password = data.get("password", "").strip()

    if not name or not mobile or not password:
        return jsonify({"message": "कृपया सर्व आवश्यक माहिती भरा."}), 400

    try:
        conn = sqlite3.connect("chatbot.db")
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (name, mobile, district, password) VALUES (?, ?, ?, ?)",
            (name, mobile, district, password)
        )
        conn.commit()
        conn.close()
        return jsonify({"message": "नोंदणी यशस्वी झाली! आता लॉगिन करा."}), 200
    except sqlite3.IntegrityError:
        return jsonify({"message": "हा मोबाईल नंबर आधीच नोंदणीकृत आहे."}), 400
    except Exception as e:
        return jsonify({"message": "डेटाबेस त्रुटी आली."}), 500


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    mobile = data.get("mobile", "").strip()
    password = data.get("password", "").strip()

    conn = sqlite3.connect("chatbot.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name, password FROM users WHERE mobile = ?", (mobile,))
    user = cursor.fetchone()
    conn.close()

    if not user or user[1] != password:
        return jsonify({"message": "मोबाईल नंबर किंवा पासवर्ड चुकीचा आहे."}), 401
        
    session.permanent = True
    session["user_name"] = user[0]
    session["user_mobile"] = mobile

    return jsonify({"message": f"स्वागत आहे, {user[0]}!", "user_name": user[0]}), 200


@app.route("/logout", methods=["GET"])
def logout():
    session.clear()
    return jsonify({"message": "लॉगआउट यशस्वी झाले."}), 200

@app.route("/check-auth", methods=["GET"])
def check_auth():
    user_name = session.get("user_name")
    if user_name:
        return jsonify({"logged_in": True, "user_name": user_name}), 200
    return jsonify({"logged_in": False}), 200


@app.route("/history", methods=["GET"])
def history():
    user_mobile = session.get("user_mobile")
    if not user_mobile:
        return jsonify({"message": "कृपया आधी लॉगिन करा.", "history": []}), 401

    conn = sqlite3.connect("chatbot.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, question, answer, timestamp FROM chat_history WHERE mobile = ? ORDER BY id ASC",
        (user_mobile,)
    )
    rows = cursor.fetchall()
    conn.close()

    history_list = []
    for row in rows:
        q_text = row[1]
        # सवाल का पहला छोटा हिस्सा (Short Name / Title)
        short_title = q_text[:25] + "..." if len(q_text) > 25 else q_text
        
        history_list.append({
            "id": row[0],
            "title": short_title,
            "question": row[1],
            "answer": row[2],
            "time": row[3]
        })

    return jsonify({"history": history_list}), 200


# -------------------- STATIC FILES --------------------

@app.route("/manifest.json")
def serve_manifest():
    return send_from_directory(".", "manifest.json")


@app.route("/service-worker.js")
def serve_sw():
    return send_from_directory(".", "service-worker.js")


@app.route("/icon-192.png")
def serve_icon192():
    return send_from_directory(".", "icon-192.png")


@app.route("/icon-512.png")
def serve_icon512():
    return send_from_directory(".", "icon-512.png")


# -------------------- RUN --------------------

if __name__ == "__main__":
    print("=" * 50)
    print("🌾 Smart Farmer Assistant Server")
    print("Running at: http://localhost:5000")
    print("=" * 50)

    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False, threaded=True)
