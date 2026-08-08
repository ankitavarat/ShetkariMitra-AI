from pyexpat import model
import re
from urllib import response

# import sounddevice as sd
# from scipy.io.wavfile import write
# import speech_recognition as sr
import numpy as np
# from gtts import gTTS
# import pygame as pygame
import requests
import sqlite3
import time
import cv2
import logging 
from groq import Groq
from config import api_key, groq_key, marketing_key
groq_client = Groq(api_key=groq_key)

logging.basicConfig(
    filename="shetkarimitra.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# pygame.mixer.init()


# ---------------- SPEAK ----------------
# def speak(text):

# language = detect_language(text)

#     if language == "marathi":

#         lang_code = "mr"

#     else:

#         lang_code = "en"

#     filename = f"voice_{int(time.time()*1000)}.mp3"   

#     tts = gTTS(
#         text=text,
#         lang=lang_code
#     )

#     filename = "voice.mp3"

#     tts.save(filename)


#     pygame.mixer.music.load(filename)

#     pygame.mixer.music.play()

#     while pygame.mixer.music.get_busy():
#         pygame.time.Clock().tick(10)

#     pygame.mixer.music.unload()


# # ---------------- STOP SPEAKING ----------------
# def stop_speaking():

#     pygame.mixer.music.stop()    

# ----------------LANGUAGE DETECTION -----------------
def detect_language(text):

    marathi_words = [
        "pani", "kami", "khate", "pik",
        "rog", "havaman", "sheti",
        "beej", "thandi", "garam",
        "kapus", "tomato","pana","dag",
        "paus","kanda","bhat","us","gahu",
        "pane","pivli","lagvad","yojana","shetkari"
        ,"karle","jeevamrut","fawarni","pivlya","kharif",
        'namaste'
    ]

    # Marathi Lipi
    for ch in text:

        if 'अ' <= ch <= 'ह':
            return "marathi"

    # Roman Marathi
    words = text.lower().split()

    for word in words:

        if word in marathi_words:
            return "marathi"

    return "english"
    
    
# ---------------- WEATHER ----------------
def get_weather(city, language):

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    try:

        response = requests.get(url, timeout=5)

        logging.info(f"Weather API called for city: {city}")

        data = response.json()

        if data["cod"] != 200:

            return None

        temp = data["main"]["temp"]

        humidity = data["main"]["humidity"]

        weather = data["weather"][0]["description"]

        return {

            "temp": temp,

            "humidity": humidity,

            "weather": weather,

            "city": city

        }

    except Exception as e:
          logging.error(f"Weather API Error: {e}")

          return None
    

def get_weather_by_coords(lat, lon, language):

    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"

    try:
        response = requests.get(url, timeout=10)
        data = response.json()

        if data.get("cod") != 200:
            return None

        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        weather = data["weather"][0]["description"]
        city = data["name"]

        # Reverse geocoding — exact location name
        # Nominatim — exact village/town name
        try:
          geo_url = f"https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={lon}&format=json&zoom=14"
          geo_res = requests.get(geo_url, timeout=5, headers={"User-Agent": "ShetkariMitraAI/1.0"})
          geo_data = geo_res.json()
          address = geo_data.get("address", {})
    
          print("Address data:", address)  # debug ke liye
    
          city = (
             address.get("village") or
             address.get("hamlet") or      # ← chhote gaon ke liye
             address.get("town") or
             address.get("municipality") or # ← taluka level
             address.get("county") or       # ← district level
             address.get("suburb") or
             address.get("city") or
             city
           )
        except:
           pass
        return {
            "temp": temp,
            "humidity": humidity,
            "weather": weather,
            "city": city
        }

    except:
        return None    
    

def get_forecast(city):

    url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric"

    try:

        response = requests.get(url, timeout=5)

        data = response.json()

        if data["cod"] != "200":

            return None

        return data

    except:

        return None    


def get_market_price(crop, language):

    logging.info("Entered get_market_price()")

    url = f"https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070?api-key={marketing_key}&format=json&limit=5&filters%5Bstate.keyword%5D=Maharashtra&filters%5Bcommodity%5D={crop}"

    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/137.0 Safari/537.36"
   }

    # Marathi → English crop mapping
    crop_map = {
        "kanda": "Onion",
        "kapus": "Cotton",
        "batata": "Potato",
        "tomato": "Tomato",
        "wheat": "Wheat",
        "rice": "Rice",
        "sugarcane": "Sugarcane"
    }

    crop_name = crop_map.get(crop.lower(), crop.title())


    try:
        logging.info(f"Crop Requested: {crop_name}")

        response = requests.get(
            url,
            headers=headers,
            timeout=15
        )

        logging.info(f"Market API Status: {response.status_code}")

        data = response.json()

        if response.status_code != 200:
            return "❌ Market API Error"

        if not data.get("records"):
            if language == "marathi":
                return f"❌ {crop_name} चा भाव सापडला नाही."
            return f"❌ Price not found for {crop_name}."

        results = []

        for item in data["records"]:

            commodity = item.get("commodity", "")
            market = item.get("market", "")
            date = item.get("arrival_date", "")

            min_price = item.get("min_price", "")
            max_price = item.get("max_price", "")
            modal_price = item.get("modal_price", "")

            if language == "marathi":

                results.append(
                    f"🌾 पीक : {commodity}\n"
                    f"📍 बाजार : {market}\n"
                    f"📅 तारीख : {date}\n"
                    f"🗺 जिल्हा : {item.get('district', '')}\n"
                    f"💰 किमान : ₹{min_price}|💰 कमाल : ₹{max_price}|💰 सरासरी : ₹{modal_price}"
                    
                )

            else:

                results.append(
                    f"🌾 Crop : {commodity}\n"
                    f"📍 Market : {market}\n"
                    f"📅 Date : {date}\n"
                    f"🗺 District : {item.get('district', '')}\n"
                    f"💰 Min : ₹{min_price}|💰 Max : ₹{max_price}|💰 Modal : ₹{modal_price}"
                    
                )

        return "\n\n".join(results)

    except Exception as e:

        logging.error(f"Market API Error: {e}")

        if language == "marathi":
            return "❌ बाजारभाव माहिती उपलब्ध नाही."

        return "❌ Market price not available."
# ---------------- VOICE INPUT ----------------
# def get_voice_input():

#     fs = 44100

#     seconds = 5

#     recording = sd.rec(
#         int(seconds * fs),
#         samplerate=fs,
#         channels=1
#     )

#     sd.wait()

#     recording = np.int16(recording * 32767)

#     write("output.wav", fs, recording)

#     r = sr.Recognizer()

#     with sr.AudioFile("output.wav") as source:

#         audio = r.record(source)

#     try:

#         text = r.recognize_google(audio)

#         return text.lower()

#     except:

#         return ""
    

# ---------------- DETECT CROP ----------------
def detect_crop(question):

    crops = [
        "tomato",
        "onion",
        "cotton",
        "wheat",
        "rice",
        "sugarcane",
        "kanda",
        "kapus",
        "batata",
        "gahu",
        "potato"
    ]

    for crop in crops:

        if crop in question:
            return crop

    return None


# ---------------- DETECT INTENT ----------------
def detect_intent(question):

    if (
        "pani" in question
        or "पाणी" in question
        or "irrigation" in question
    ):

        return "water"

    elif (
        "favarni" in question
        or "फवारणी" in question
        or "spray" in question
    ):

        return "spray"

    elif (
        "lagvad" in question
        or "लागवड" in question
        or "lagvadi" in question
        or "plant" in question
        or "planting" in question
    ):

        return "plant"
    
    elif (
    "aaj " in question
    or "आज " in question
    or "rain today" in question
    ):
      return "today_rain"
    
    elif (
    "udya" in question
    or "उद्या" in question
    or "tomorrow" in question
    or "tomorrow weather" in question
    ):
      return "tomorrow_weather"
    
    elif (
    "market" in question
    or "bhav" in question
    or "rate" in question
    or "mandi" in question
    or "price" in question
  ):
      return "market_price"

    return None


# ---------------- WATER ADVICE ----------------
def water_advice(temp, detected_crop, language):

    if temp >= 30:

        if language == "marathi":

            return (
                "आज तापमान जास्त आहे ☀️\n"
                f"{detected_crop} पिकाला हलके पाणी द्या."
            )

        else:

            return (
                f"Temperature is high ☀️\n"
                f"Give light irrigation to {detected_crop} crop."
            )

    else:

        if language == "marathi":

            return "सध्या तात्काळ पाणी देण्याची गरज नाही."

        else:

            return "No immediate irrigation needed."


# ---------------- PLANTING ADVICE ----------------
def planting_advice(weather, temp, detected_crop, language):

    if "rain" in weather.lower():

        if language == "marathi":

            return (
                f"{detected_crop} लागवडीसाठी पावसाळी हवामान आहे 🌧\n"
                "जमिनीत पाणी साचणार नाही याची काळजी घ्या."
            )

        else:

            return (
                f"Rainy weather for {detected_crop} planting 🌧\n"
                "Avoid waterlogging in the field."
            )

    elif temp >= 30:

        if language == "marathi":

            return (
                f"{detected_crop} लागवडीसाठी गरम हवामान आहे ☀️\n"
                "हलके पाणी द्या."
            )

        else:

            return (
                f"Hot weather for {detected_crop} planting ☀️\n"
                "Give light irrigation."
            )

    else:

        if language == "marathi":

            return (
                f"{detected_crop} लागवडीसाठी हवामान योग्य आहे 🌱"
            )

        else:

            return (
                f"Weather is suitable for {detected_crop} planting 🌱"
            )
        

def get_today_rain(city, language):

    weather_data = get_weather(city, language)

    if weather_data is None:

        if language == "marathi":
            return "हवामान माहिती उपलब्ध नाही."
        else:
            return "Weather information not available."

    weather = weather_data["weather"].lower()

    if (
        "rain" in weather
        or "drizzle" in weather
        or "thunderstorm" in weather
    ):

        if language == "marathi":
            return f"🌧 हो, {city} मध्ये आज पावसाची शक्यता आहे."
        else:
            return f"🌧 Yes, {city} rain is expected today."

    else:

        if language == "marathi":
            return f"☀️ नाही, {city} मध्ये आज पावसाची शक्यता नाही."
        else:
            return f"☀️ No, {city} rain is not expected today."        
        


def get_tomorrow_rain(city, language):

    forecast = get_forecast(city)

    if forecast is None:

        if language == "marathi":
            return "हवामान माहिती उपलब्ध नाही."

        else:
            return "Weather information not available."

    tomorrow_weather = (
        forecast["list"][8]["weather"][0]["main"]
    )

    tomorrow_temp = (
    forecast["list"][8]["main"]["temp"]
   )

    tomorrow_humidity = (
    forecast["list"][8]["main"]["humidity"]
)

    if tomorrow_weather.lower() in [
        "rain",
        "drizzle",
        "thunderstorm"
    ]:

        if language == "marathi":

         return (
           f"🌧{city}मध्ये उद्या पावसाची शक्यता आहे.\n\n"

           f"🌡 अंदाजित तापमान : {tomorrow_temp:.1f}°C\n"

           f"💧 आर्द्रता : {tomorrow_humidity}%\n"

           f"☁ हवामान : {tomorrow_weather}\n\n"

           "🌾 फवारणी टाळा.\n"

           "⚠️ शेतात पाणी साचणार नाही याची काळजी घ्या.\n"

           "💧 अतिरिक्त सिंचनाची गरज नसू शकते."
        )

        else:

         return (
           f"🌧 Rain is expected tomorrow in {city}.\n\n"

           f"🌡 Expected Temperature : {tomorrow_temp:.1f}°C\n"

           f"💧 Humidity : {tomorrow_humidity}%\n"

           f"☁ Weather Condition : {tomorrow_weather}\n\n"

           "🌾 Avoid spraying pesticides.\n"

           "⚠️ Ensure proper drainage in the field.\n"

           "💧 Additional irrigation may not be required."
       )



    else:

        if language == "marathi":

         return (
          f"☀️{city}मध्ये उद्या पावसाची शक्यता कमी आहे.\n\n"

          f"🌡 अंदाजित तापमान : {tomorrow_temp:.1f}°C\n"

          f"💧 आर्द्रता : {tomorrow_humidity}%\n"

          f"☁ हवामान : {tomorrow_weather}\n\n"

          "🌾 शेतातील नियोजित कामे करू शकता.\n"

          "💧 आवश्यक असल्यास सिंचन करा."
       )

        else:

         return (
            f"☀️ Rain is not expected tomorrow in {city}.\n\n"

            f"🌡 Expected Temperature : {tomorrow_temp:.1f}°C\n"

            f"💧 Humidity : {tomorrow_humidity}%\n"

            f"☁ Weather Condition : {tomorrow_weather}\n\n"

            "🌾 You can continue planned farming activities.\n"

            "💧 Irrigate crops if required."
        )       


# ---------------- DATABASE RESPONSE ----------------
def get_database_response(question, language):

    conn = sqlite3.connect("chatbot.db")

    cursor = conn.cursor()

    cursor.execute(
        "SELECT keyword,answer_en,answer_mr FROM qa"
    )

    data = cursor.fetchall()

    conn.close()

    question = question.lower()

    best_match = None
    best_length = 0

    for row in data:

        keywords = row[0].split(",")

        answer_en = row[1]

        answer_mr = row[2]

        for k in keywords:

            k = k.strip().lower()

            if k in question:

                if len(k) > best_length:
                    best_length = len(k)

                    best_match = (answer_en, answer_mr)

    if best_match:
                                

        if language == "marathi":

            return best_match[1].replace(";", "\n")

        else:

            return best_match[0].replace(";", "\n")

    return None 

# ---------------- DISEASE DETECTION ----------------
def detect_disease(filepath, language):

    img = cv2.imread(filepath)

    if img is None:
        if language == "marathi":
            return "❌ फोटो वाचता आला नाही."
        else:
            return "❌ Unable to read image."

    # Resize
    img = cv2.resize(img, (300, 300))
    total_pixels = 300 * 300

    # HSV convert
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # ── GREEN (Healthy) ──
    green_mask = cv2.inRange(hsv, (36, 50, 50), (86, 255, 255))
    green_pixels = cv2.countNonZero(green_mask)

    # ── YELLOW ──
    yellow_mask = cv2.inRange(hsv, (20, 100, 100), (35, 255, 255))
    yellow_pixels = cv2.countNonZero(yellow_mask)

    # ── BLACK SPOTS ──
    black_mask = cv2.inRange(hsv, (0, 0, 0), (180, 255, 50))
    black_pixels = cv2.countNonZero(black_mask)

    # ── BROWN (Rust/Blight) ──
    brown_mask = cv2.inRange(hsv, (10, 100, 20), (20, 255, 200))
    brown_pixels = cv2.countNonZero(brown_mask)

    # ── WHITE SPOTS (Powdery Mildew) ──
    white_mask = cv2.inRange(hsv, (0, 0, 200), (180, 30, 255))
    white_pixels = cv2.countNonZero(white_mask)

    logging.info(
    f"Disease Detection -> Green:{green_pixels}, Yellow:{yellow_pixels}, "
    f"Black:{black_pixels}, Brown:{brown_pixels}, White:{white_pixels}"
    )

    # ── SEVERITY CALCULATOR ──
    def severity(pixels):
        pct = (pixels / total_pixels) * 100
        if pct > 20:
            return ("High", "जास्त", "🔴")
        elif pct > 10:
            return ("Medium", "मध्यम", "🟡")
        else:
            return ("Low", "कमी", "🟢")

    results = []

    # ── HEALTHY CHECK ──
    green_pct = (green_pixels / total_pixels) * 100
    disease_pixels = yellow_pixels + black_pixels + brown_pixels + white_pixels
    disease_pct = (disease_pixels / total_pixels) * 100

    if green_pct > 40 and disease_pct < 5:
        if language == "marathi":
            return (
                "✅ पान निरोगी दिसत आहे!\n"
                f"🌿 हिरवेपणा : {green_pct:.1f}%\n"
                "💚 कोणताही रोग आढळला नाही.\n"
                "🌱 पिकाची चांगली काळजी घेत आहात!"
            )
        else:
            return (
                "✅ Leaf appears Healthy!\n"
                f"🌿 Greenness : {green_pct:.1f}%\n"
                "💚 No disease detected.\n"
                "🌱 Keep up the good crop care!"
            )

    # ── YELLOW DISEASE ──
    if yellow_pixels > 2000:
        sev_en, sev_mr, icon = severity(yellow_pixels)
        if language == "marathi":
            results.append(
                f"🌿 पान पिवळे पडण्याची समस्या आढळली.\n"
                f"📊 तीव्रता : {icon} {sev_mr} ({(yellow_pixels/total_pixels*100):.1f}%)\n"
                "🔍 कारण : नायट्रोजनची कमतरता किंवा बुरशी\n"
                "✅ उपाय : DAP खत द्या, पाण्याचे नियोजन करा."
            )
        else:
            results.append(
                f"🌿 Yellow Leaf Disease Detected.\n"
                f"📊 Severity : {icon} {sev_en} ({(yellow_pixels/total_pixels*100):.1f}%)\n"
                "🔍 Cause : Nitrogen deficiency or fungal infection\n"
                "✅ Remedy : Apply DAP fertilizer, manage irrigation."
            )

    # ── BLACK SPOTS ──
    if black_pixels > 2000:
        sev_en, sev_mr, icon = severity(black_pixels)
        if language == "marathi":
            results.append(
                f"⚫ पानावर काळे डाग आढळले.\n"
                f"📊 तीव्रता : {icon} {sev_mr} ({(black_pixels/total_pixels*100):.1f}%)\n"
                "🔍 कारण : बुरशीजन्य रोग (Fungal)\n"
                "✅ उपाय : मॅन्कोझेब बुरशीनाशक फवारणी करा."
            )
        else:
            results.append(
                f"⚫ Black Spot Disease Detected.\n"
                f"📊 Severity : {icon} {sev_en} ({(black_pixels/total_pixels*100):.1f}%)\n"
                "🔍 Cause : Fungal infection\n"
                "✅ Remedy : Spray Mancozeb fungicide immediately."
            )

    # ── BROWN / RUST / BLIGHT ──
    if brown_pixels > 2000:
        sev_en, sev_mr, icon = severity(brown_pixels)
        if language == "marathi":
            results.append(
                f"🟤 तांबेरा / करपा रोग आढळला.\n"
                f"📊 तीव्रता : {icon} {sev_mr} ({(brown_pixels/total_pixels*100):.1f}%)\n"
                "🔍 कारण : Rust किंवा Blight बुरशी\n"
                "✅ उपाय : Propiconazole फवारणी करा, ओलावा कमी करा."
            )
        else:
            results.append(
                f"🟤 Rust / Blight Disease Detected.\n"
                f"📊 Severity : {icon} {sev_en} ({(brown_pixels/total_pixels*100):.1f}%)\n"
                "🔍 Cause : Rust or Blight fungus\n"
                "✅ Remedy : Spray Propiconazole, reduce moisture."
            )

    # ── WHITE / POWDERY MILDEW ──
    if white_pixels > 3000:
        sev_en, sev_mr, icon = severity(white_pixels)
        if language == "marathi":
            results.append(
                f"⬜ भुरी रोग (Powdery Mildew) आढळला.\n"
                f"📊 तीव्रता : {icon} {sev_mr} ({(white_pixels/total_pixels*100):.1f}%)\n"
                "🔍 कारण : कोरड्या हवामानात बुरशी\n"
                "✅ उपाय : Sulphur dust किंवा Karathane फवारणी करा."
            )
        else:
            results.append(
                f"⬜ Powdery Mildew Detected.\n"
                f"📊 Severity : {icon} {sev_en} ({(white_pixels/total_pixels*100):.1f}%)\n"
                "🔍 Cause : Fungus in dry weather\n"
                "✅ Remedy : Apply Sulphur dust or Karathane spray."
            )

    # ── FINAL RESULT ──
    if results:
        header = "🔬 रोग विश्लेषण अहवाल\n\n" if language == "marathi" else "🔬 Disease Analysis Report\n\n"
        return header + "\n\n".join(results)
    else:
        if language == "marathi":
            return (
                "⚠️ रोग स्पष्टपणे ओळखता आला नाही.\n"
                "📷 कृपया पानाचा स्पष्ट, जवळचा फोटो अपलोड करा.\n"
                "💡 फोटो नैसर्गिक प्रकाशात काढा."
            )
        else:
            return (
                "⚠️ Disease not clearly detected.\n"
                "📷 Please upload a clear, close-up leaf photo.\n"
                "💡 Take photo in natural light for better results."
            )

CITY_MAP = {
    "जामखेड": "Jamkhed",
    "पुणे": "Pune",
    "अहमदनगर": "Ahmednagar",
    "नगर": "Ahmednagar",
    "मुंबई": "Mumbai",
    "नाशिक": "Nashik",
    "औरंगाबाद": "Aurangabad",
    "कोल्हापूर": "Kolhapur",
    "सोलापूर": "Solapur",
}

def extract_city_from_question(question):
    skip_words = [
        "weather", "havaman", "हवामान", "आजचे", "आजचं",
        "उद्या", "उद्याचे", "पाऊस", "पडणार", "आहे", "का",
        "मध्ये", "सांगा", "काय", "कसा", "कसे", "aaj",
        "udya", "paus", "padnar", "aahe", "ka", "madhe",
        "sanga", "today", "tomorrow", "rain", "weather",
        "forecast", "batao", "bata", "kya", "hai", "hoga",
        "padnar", "sandha", "kiti", "kitiv"
    ]
    words = question.split()
    for word in words:
        clean_word = word.strip("?.,!।")
        if clean_word.lower() in skip_words:
            continue
        if any('\u0900' <= c <= '\u097F' for c in clean_word):
            if clean_word in CITY_MAP:
                return CITY_MAP[clean_word]
            if clean_word in ["हवामान","पाऊस","उद्या","आजचे","मध्ये","आहे","का","सांगा","पडणार"]:
                continue
            try:
                from indic_transliteration import sanscript
                roman = sanscript.transliterate(
                    clean_word,
                    sanscript.DEVANAGARI,
                    sanscript.ITRANS
                )
                roman = roman.replace('aa','a').replace('ii','i')
                return roman.capitalize()
            except:
                return clean_word
        else:
            if len(clean_word) > 2:
                return clean_word.capitalize()
    return "Pune"
# ---------------- MAIN CHATBOT ----------------
def chatbot_response(question):

    question = str(question)

    logging.info(f"User Question: {question}")

    language = detect_language(question)

    logging.info(f"Language: {language}")

    question = question.strip().lower()

    detected_crop = detect_crop(question)

    logging.info(f"Detected Crop: {detected_crop}")

    # Greeting
    if (
        "hello" in question
        or "namaste" in question
        or "नमस्कार" in question
    ):

        if language == "marathi":

            return "नमस्कार शेतकरी मित्र 🌾"

        else:

            return "Hello Farmer Friend 🌾"
        
    intent = detect_intent(question)

    if intent == "market_price":

      crop = detect_crop(question)

      if crop:

        if crop == "kanda":
            crop = "onion"

        if crop == "kapus":
            crop = "cotton"

        return get_market_price(
            crop,
            language
        )

      if language == "marathi":
         return "कृपया पिकाचे नाव सांगा."

      return "Please specify crop name."

    if intent in ["today_rain", "tomorrow_weather"]:

     words = question.split()

     city = extract_city_from_question(question)
     print("Question :", question)
     print("Detected City :", city)   
        
     if intent == "today_rain":

        return get_today_rain(
            city,
            language
        )

     if intent == "tomorrow_weather":

        return get_tomorrow_rain(
            city,
            language
        )

    # ---------------- WEATHER ----------------
    if (
        "weather" in question
        or "havaman" in question
        or "हवामान" in question
    ):

        words = question.split()

        city = extract_city_from_question(question)
        print("Question :", question)
        print("Detected City :", city)

        weather_data = get_weather(city, language)

        if weather_data is None:

            if language == "marathi":

                return "हवामान माहिती मिळाली नाही."

            else:

                return "Weather information not found."

        temp = weather_data["temp"]

        humidity = weather_data["humidity"]

        weather = weather_data["weather"]

        # Intent Detection
        intent = detect_intent(question)

        # Water Advice
        if (
            detected_crop is not None
            and intent == "water"
        ):

            return water_advice(
                temp,
                detected_crop,
                language
            )

        # Planting Advice
        if (
            detected_crop is not None
            and intent == "plant"
        ):

            return planting_advice(
                weather,
                temp,
                detected_crop,
                language
            )

        # Crop Weather
        if detected_crop is not None:

            # Rainy Weather
            if "rain" in weather.lower():

                if language == "marathi":

                    if detected_crop == "tomato":

                        return (
                            "आज टोमॅटो लागवड टाळा 🌧\n"
                            "बुरशीचा धोका वाढू शकतो."
                        )

                    elif detected_crop == "kanda":

                        return (
                            "कांदा पिकात पाणी साचू देऊ नका 🌧"
                        )

                else:

                    if detected_crop == "tomato":

                        return (
                            "Avoid tomato planting today 🌧\n"
                            "Fungal disease risk may increase."
                        )

                    elif detected_crop == "onion":

                        return (
                            "Do not allow water logging in onion crop 🌧"
                        )

            # Hot Weather
            elif temp >= 30:

                if language == "marathi":

                    return (
                        "उष्ण हवामान आहे ☀️\n"
                        "नियमित पाणी द्या."
                    )

                else:

                    return (
                        "Hot weather detected ☀️\n"
                        "Give water regularly."
                    )

            # Good Weather
            else:

                if language == "marathi":

                    return (
                        f"{detected_crop} लागवडीसाठी हवामान योग्य आहे 🌱"
                    )

                else:

                    return (
                        f"Weather is suitable for {detected_crop} cultivation 🌱"
                    )

        # Normal Weather
        else:

            if language == "marathi":

                return (
                    f"🌤 {city} हवामान\n"
                    f"🌡 तापमान : {temp}°C\n"
                    f"💧 आर्द्रता : {humidity}%\n"
                    f"☁ हवामान : {weather}"
                )

            else:

                return (
                    f"🌤 {city.upper()} WEATHER\n"
                    f"🌡 Temperature : {temp}°C\n"
                    f"💧 Humidity : {humidity}%\n"
                    f"☁ Condition : {weather}"
                )

    # ---------------- DATABASE RESPONSE ----------------
    response = get_database_response(
        question,
        language
    )

    if response:

        return response

    # ---------------- SAVE UNKNOWN QUESTION ----------------
    conn = sqlite3.connect("chatbot.db")

    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM unknown_questions WHERE question=?",
        (question,)
    )

    existing = cursor.fetchone()

    if existing is None:

        cursor.execute(
            "INSERT INTO unknown_questions(question) VALUES(?)",
            (question,)
        )
        logging.info(f"New Unknown Question: {question}")

    conn.commit()

    conn.close()

    for attempt in range(5):
      try:
        prompt = f"""
        You are ShetkariMitra AI — an expert agricultural assistant 
        specifically for Maharashtra farmers.

        User's question: {question}

        LANGUAGE RULE (MOST IMPORTANT):
        - If question has Marathi words even in Roman script 
        (kanda, paus, sheti, lagvad, pani, gahu, bhat) 
        → Answer FULLY in Marathi Devanagari script
        - Current detected language: {"Marathi — use Devanagari script only" if language == "marathi" else "English"}

        ANSWER FORMAT:
        - Give answer in bullet points
        - Each point starts with emoji
        - Maximum 5 points
        - Each point = 1 practical sentence
        - Add quantities (10 kg/acre, 7 days interval)

        QUALITY:
        - Answer like experienced Maharashtra agronomist
        - Specific to Maharashtra climate and crops
        - Real actionable advice only
        - No filler words

        Question: {question}
        """
      
        response = groq_client.chat.completions.create(
          model="llama-3.3-70b-versatile",
          messages=[
            {
              "role": "system",
              "content": """You are ShetkariMitra AI — Maharashtra's smartest farming assistant.

            You have deep knowledge of:
            - Kharif & Rabi crops of Maharashtra 
            (Onion, Tomato, Cotton, Wheat, Sugarcane, Rice)
            - Organic farming (Jeevamrut, Dashparni Ark, Vermicompost)
            - Pest & disease management
            - Irrigation scheduling
            - Soil health & fertilizers
            - Maharashtra government schemes

            CRITICAL RULES:
            1. Roman Marathi questions (kanda, paus, sheti, lagvad) 
            = Answer in Marathi Devanagari script ALWAYS
            2. Always use bullet points with emojis (•)
            3. Give specific quantities and timings
            4. Sound like trusted expert friend
            5. Plain text only — no markdown, no HTML
            6. Maximum 5 points
            7. Each point practical and specific"""
            
            },
            {
              "role": "user",
              "content": prompt
           }
          ],
          temperature=0.7,
          max_tokens=350,
          timeout=10
        )

        logging.info("Groq Response Generated")
        raw = response.choices[0].message.content
        print("Groq Raw Answer:", raw)
        logging.info("Groq response received successfully")

        clean = re.sub(r'\*\*(.+?)\*\*', r'\1', raw)
        clean = re.sub(r'\*(.+?)\*', r'\1', clean)
        clean = re.sub(r'#{1,6}\s', '', clean)
        clean = re.sub(r'\[(.+?)\]\(.+?\)', r'\1', clean)
        clean = re.sub(r'`(.+?)`', r'\1', clean)
        clean = re.sub(r'<[^>]+>', '', clean)
        clean = clean.strip()

        return clean
      
      except Exception as e:
       
       if '429' in str(e):
            logging.warning(f"Rate limit — waiting 5 sec... attempt {attempt+1}")
            time.sleep(10)
       else:      
        logging.error(f"Groq Error: {e}")
        break
    if language == "marathi":
        return "कृपया अधिक माहिती द्या."
    else:
        return "Please provide more information."
