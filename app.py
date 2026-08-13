"""
app.py — Flask bridge server with Session-based Chat Grouping
Connects smart_farmer_ui.html with backend.py and Supabase Database.
"""

from datetime import timedelta
import os
import tempfile
import uuid

from backend import (
    chatbot_response,
    detect_disease,
    get_weather,
    get_weather_by_coords,
)
from flask import Flask, jsonify, request, send_from_directory, session
from flask_cors import CORS
import psycopg2

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "shetkari_secret_key_123")
CORS(app, supports_credentials=True)
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(days=30)

DATABASE_URL = os.environ.get("DATABASE_URL")


def get_db_connection():
  return psycopg2.connect(
      DATABASE_URL,
      sslmode="require",
      connect_timeout=10,
      options="-c prepare_threshold=0",
  )

def init_db():
  try:
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                mobile VARCHAR(15) UNIQUE NOT NULL,
                district VARCHAR(100),
                password VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)

    # 🔹 session_id चा कॉलम ऑटो जोडला जाईल
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS chat_history (
                id SERIAL PRIMARY KEY,
                mobile VARCHAR(15) NOT NULL,
                session_id VARCHAR(100) NOT NULL,
                question TEXT NOT NULL,
                answer TEXT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)

    conn.commit()
    cursor.close()
    conn.close()
    print("✅ Tables initialized!")
  except Exception as e:
    print("❌ DB Error:", e)


init_db()


@app.route("/")
def index():
  return send_from_directory(".", "smart_farmer_ui.html")


# -------------------- CHAT --------------------


@app.route("/chat", methods=["POST"])
def chat():
  data = request.get_json() or {}
  question = data.get("question", "").strip()

  if not question:
    return jsonify({"answer": "Please enter a question."}), 400

  answer = chatbot_response(question)

  # 🔹 जर सेशन नसेल, तर नवीन बनवा
  if "current_chat_session" not in session:
    session["current_chat_session"] = str(uuid.uuid4())

  chat_session_id = session["current_chat_session"]

  user_mobile = session.get("user_mobile")
  if user_mobile:
    try:
      conn = get_db_connection()
      cursor = conn.cursor()
      cursor.execute(
          """
                INSERT INTO chat_history (mobile, session_id, question, answer)
                VALUES (%s, %s, %s, %s)
            """,
          (user_mobile, chat_session_id, question, answer),
      )
      conn.commit()
      cursor.close()
      conn.close()
    except Exception as e:
      print("History Save Error:", e)

  return jsonify({"answer": answer})


# 🔹 1. नवीन पेज / New Chat सुरू करण्यासाठी नवीन राऊट (याने प्रत्येक नवीन पेजला नवीन पॉईंट बनेल)
@app.route("/new-session", methods=["POST"])
def new_session():
  session["current_chat_session"] = str(uuid.uuid4())
  return jsonify(
      {"status": "success", "session_id": session["current_chat_session"]}
  )


# -------------------- HISTORY --------------------


@app.route("/history", methods=["GET"])
def history():
  user_mobile = session.get("user_mobile")
  if not user_mobile:
    return jsonify({"message": "कृपया आधी लॉगिन करा.", "history": []}), 401

  try:
    conn = get_db_connection()
    cursor = conn.cursor()

    # 🔹 प्रत्येक session_id चा एकच इतिहास पॉईंट बनवणे
    cursor.execute(
        """
            SELECT 
                session_id,
                (ARRAY_AGG(question ORDER BY id ASC))[1] as first_question,
                MIN(timestamp) as session_time,
                COUNT(id) as total_count
            FROM chat_history
            WHERE mobile = %s
            GROUP BY session_id
            ORDER BY session_time DESC;
        """,
        (user_mobile,),
    )

    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    history_list = []
    for row in rows:
      first_q = row[1]
      short_title = first_q[:28] + "..." if len(first_q) > 28 else first_q

      history_list.append({
          "session_id": str(row[0]),
          "title": short_title,
          "time": str(row[2]),
          "count": row[3],
      })

    return jsonify({"history": history_list}), 200
  except Exception as e:
    print("History Fetch Error:", e)
    return jsonify({"message": "History एरर", "history": []}), 500


# 🔹 2. विशिष्ट Session चे सर्व मेसेजेस मिळवणे
@app.route("/get-session-chat/<session_id>", methods=["GET"])
def get_session_chat(session_id):
  user_mobile = session.get("user_mobile")
  if not user_mobile:
    return jsonify({"message": "Unauthorized"}), 401

  try:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
            SELECT question, answer, timestamp 
            FROM chat_history 
            WHERE mobile = %s AND session_id = %s 
            ORDER BY id ASC;
        """,
        (user_mobile, session_id),
    )
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    messages = []
    for row in rows:
      messages.append(
          {"question": row[0], "answer": row[1], "time": str(row[2])}
      )

    return jsonify({"messages": messages}), 200
  except Exception as e:
    print("Fetch session error:", e)
    return jsonify({"message": "Error fetching chat"}), 500

# -------------------- AUTH & OTHER ROUTES --------------------


@app.route("/login", methods=["POST"])
def login():
  data = request.get_json() or {}
  mobile = data.get("mobile", "").strip()
  password = data.get("password", "").strip()

  conn = get_db_connection()
  cursor = conn.cursor()
  cursor.execute(
      "SELECT name, password FROM users WHERE mobile = %s;", (mobile,)
  )
  user = cursor.fetchone()
  cursor.close()
  conn.close()

  if not user or user[1] != password:
    return jsonify({"message": "मोबाईल नंबर किंवा पासवर्ड चुकीचा आहे."}), 401

  session.permanent = True
  session["user_name"] = user[0]
  session["user_mobile"] = mobile
  # लॉगिन होताच नवीन सेशन सुरू होईल
  session["current_chat_session"] = str(uuid.uuid4())

  return jsonify({"message": f"स्वागत आहे, {user[0]}!", "user_name": user[0]}), 200


@app.route("/logout", methods=["GET"])
def logout():
  session.clear()
  return jsonify({"message": "लॉगआउट यशस्वी झाले."}), 200


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
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (name, mobile, district, password) VALUES (%s, %s,"
        " %s, %s)",
        (name, mobile, district, password),
    )
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "नोंदणी यशस्वी झाली! आता लॉगिन करा."}), 200
  except Exception as e:
    return jsonify({"message": "डेटाबेस त्रुटी आली."}), 500


@app.route("/check-auth", methods=["GET"])
def check_auth():
  user_name = session.get("user_name")
  if user_name:
    return jsonify({"logged_in": True, "user_name": user_name}), 200
  return jsonify({"logged_in": False}), 200


@app.route("/weather", methods=["GET"])
def weather():
  city = request.args.get("city", "Ahmednagar")
  language = request.args.get("lang", "english")
  data = get_weather(city, language)
  return jsonify(data) if data else (jsonify({"error": "City not found"}), 404)


@app.route("/weather-coords", methods=["GET"])
def weather_coords():
  lat = request.args.get("lat")
  lon = request.args.get("lon")
  if not lat or not lon:
    return jsonify({"error": "Latitude and longitude required"}), 400
  data = get_weather_by_coords(lat, lon, "english")
  return jsonify(data) if data else (jsonify({"error": "Weather not found"}), 404)


@app.route("/detect", methods=["POST"])
def detect():
  if "image" not in request.files:
    return jsonify({"result": "No image uploaded."}), 400
  file = request.files["image"]
  suffix = os.path.splitext(file.filename)[1] or ".jpg"
  with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
    file.save(tmp.name)
    tmp_path = tmp.name
  result = detect_disease(tmp_path, request.args.get("lang", "english"))
  try:
    os.unlink(tmp_path)
  except Exception:
    pass
  return jsonify({"result": result})


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


if __name__ == "__main__":
  port = int(os.getenv("PORT", 5000))
  app.run(host="0.0.0.0", port=port, debug=False, threaded=True)
