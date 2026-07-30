"""
app.py — Flask bridge server
Connects UI with your existing backend.py + Auth System (Login/Register)

Install:  pip install flask flask-cors werkzeug
Run:      python app.py
"""

from flask import Flask, request, jsonify, render_template, session, redirect, url_for
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import os
import tempfile
import sqlite3

# Backend module imports (NO CHANGES NEEDED IN BACKEND.PY)
from backend import (
    chatbot_response,
    get_weather,
    detect_disease,
    detect_language,
    get_weather_by_coords
)

# ─── FLASK SETUP ─────────────────────────────────────
# template_folder='.' sets the current root folder for rendering HTML files directly
app = Flask(__name__, template_folder='.')
app.secret_key = "shetkari_mitra_secret_key_2026"  # Session encryption key
CORS(app)  # Allows HTML/Frontend requests

# ─── DATABASE CONNECTION HELPER ──────────────────────
def get_db_connection():
    conn = sqlite3.connect("chatbot.db")
    conn.row_factory = sqlite3.Row
    return conn


# ─── HOME ROUTE (Serves UI) ──────────────────────────
@app.route("/")
def home():
    # Renders index.html/smart_farmer_ui.html directly from root folder
    return render_template("index.html")


# ─── AUTHENTICATION ENDPOINTS (Login / Register / Logout) ───

@app.route("/register", methods=["POST"])
def register():
    data = request.get_json() if request.is_json else request.form

    name = data.get("name", "").strip()
    mobile = data.get("mobile", "").strip()
    district = data.get("district", "").strip()
    language = data.get("language", "marathi").strip()
    password = data.get("password", "").strip()

    if not name or not mobile or not password:
        return jsonify({"status": "error", "message": "सर्व माहिती भरणे अनिवार्य आहे!"}), 400

    hashed_password = generate_password_hash(password)

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO users (name, mobile, district, language, password)
            VALUES (?, ?, ?, ?, ?)
        """, (name, mobile, district, language, hashed_password))
        conn.commit()
        conn.close()
        
        return jsonify({"status": "success", "message": "रजिस्ट्रेशन यशस्वी झाले! आता लॉगिन करा."}), 201

    except sqlite3.IntegrityError:
        return jsonify({"status": "error", "message": "हा मोबाईल नंबर आधीच रजिस्टर आहे!"}), 400
    except Exception as e:
        return jsonify({"status": "error", "message": f"Error: {str(e)}"}), 500


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json() if request.is_json else request.form

    mobile = data.get("mobile", "").strip()
    password = data.get("password", "").strip()

    if not mobile or not password:
        return jsonify({"status": "error", "message": "मोबाईल नंबर आणि पासवर्ड टाका!"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE mobile = ?", (mobile,))
    user = cursor.fetchone()
    conn.close()

    if user and check_password_hash(user['password'], password):
        # Session in Flask
        session['user_id'] = user['id']
        session['user_name'] = user['name']
        session['user_mobile'] = user['mobile']
        session['user_district'] = user['district']

        return jsonify({
            "status": "success",
            "message": f"स्वागत आहे, {user['name']}!",
            "user": {
                "name": user['name'],
                "mobile": user['mobile'],
                "district": user['district']
            }
        }), 200
    else:
        return jsonify({"status": "error", "message": "मोबाईल नंबर किंवा पासवर्ड चुकीचा आहे!"}), 401


@app.route("/logout", methods=["GET"])
def logout():
    session.clear()
    return redirect(url_for("home"))


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
    city = request.args.get("city", "ahmednagar")
    language = request.args.get("lang", "english")

    data = get_weather(city, language)

    if data is None:
        return jsonify({"error": "City not found"}), 404

    return jsonify(data)


@app.route("/weather-coords", methods=["GET"])
def weather_coords():
    lat = request.args.get("lat")
    lon = request.args.get("lon")

    data = get_weather_by_coords(lat, lon, "english")

    if data is None:
        return jsonify({"error": "Weather not found"}), 404

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

    language = request.args.get("lang", "english")

    result = detect_disease(tmp_path, language)

    # Cleanup temp file
    try:
        os.unlink(tmp_path)
    except Exception:
        pass

    return jsonify({"result": result})


# ─── RUN ─────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 50)
    print("🌾 Smart Farmer Assistant Server with Auth")
    print("   Running at: http://localhost:5000")
    print("=" * 50)
    port = int(os.getenv("PORT", 5000))
    app.run(debug=False, host="0.0.0.0", port=port, threaded=True)
