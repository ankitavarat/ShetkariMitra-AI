from pyexpat import model
import re
from urllib import response

import sounddevice as sd
from scipy.io.wavfile import write
import speech_recognition as sr
import numpy as np
from gtts import gTTS
import pygame as pygame
import requests
import sqlite3
import time
import cv2
from groq import Groq
from config import api_key, groq_key, marketing_key
groq_client = Groq(api_key=groq_key)


pygame.mixer.init()


# ---------------- SPEAK ----------------
def speak(text):

    language = detect_language(text)

    if language == "marathi":

        lang_code = "mr"

    else:

        lang_code = "en"

    filename = f"voice_{int(time.time()*1000)}.mp3"   

    tts = gTTS(
        text=text,
        lang=lang_code
    )

    filename = "voice.mp3"

    tts.save(filename)


    pygame.mixer.music.load(filename)

    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    pygame.mixer.music.unload()


# ---------------- STOP SPEAKING ----------------
def stop_speaking():

    pygame.mixer.music.stop()    

# ----------------LANGUAGE DETECTION -----------------
def detect_language(text):

    marathi_words = [
        "pani", "kami", "khate", "pik",
        "rog", "havaman", "sheti",
        "beej", "thandi", "garam",
        "kapus", "tomato","pana","dag",
        "paus","kanda","bhat","us","gahu",
        "pane","pivli","lagvad","yojana","shetkari"
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

    headers = {
        "api-key": marketing_key
    }

    url = "https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070"

    params = {
        "api-key": marketing_key,
        "format": "json",
        "limit": 5,
        "filters[state.keyword]": "Maharashtra",
        "filters[commodity]": crop.title()
    }

    try:
        session = requests.Session()
        session.headers.update(headers)
        response = session.get(url, params=params, timeout=60)
        print(response.status_code)
        data = response.json()
        
        if not data.get("records"):
            if language == "marathi":
                return "❌ या पिकाचा भाव सापडला नाही."
            return "❌ Price not found for this crop."

        results = []
        for item in data["records"]:
            commodity = item.get("commodity", "")
            market = item.get("market", "")
            min_price = item.get("min_price", "")
            max_price = item.get("max_price", "")
            modal_price = item.get("modal_price", "")
            date = item.get("arrival_date", "")

            if language == "marathi":
                results.append(
                    f"🌾 पीक : {commodity}\n"
                    f"📍 बाजार : {market}\n"
                    f"📅 तारीख : {date}\n"
                    f"💰 किमान : ₹{min_price} | कमाल : ₹{max_price} | सरासरी : ₹{modal_price}"
                )
            else:
                results.append(
                    f"🌾 Crop : {commodity}\n"
                    f"📍 Market : {market}\n"
                    f"📅 Date : {date}\n"
                    f"💰 Min : ₹{min_price} | Max : ₹{max_price} | Modal : ₹{modal_price}"
                )

        return "\n\n".join(results)

    except Exception as e:
        print(e)
        if language == "marathi":
            return "❌ बाजारभाव माहिती उपलब्ध नाही."
        return "❌ Market price not available."


# ---------------- VOICE INPUT ----------------
def get_voice_input():

    fs = 44100

    seconds = 5

    recording = sd.rec(
        int(seconds * fs),
        samplerate=fs,
        channels=1
    )

    sd.wait()

    recording = np.int16(recording * 32767)

    write("output.wav", fs, recording)

    r = sr.Recognizer()

    with sr.AudioFile("output.wav") as source:

        audio = r.record(source)

    try:

        text = r.recognize_google(audio)

        return text.lower()

    except:

        return ""
    

# ---------------- DETECT CROP ----------------
def detect_crop(question):

    crops = [
        "tomato",
        "onion",
        "cotton",
        "wheat",
        "rice",
        "sugarcane",
        "kanda"
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

    for row in data:

        keywords = row[0].split(",")

        answer_en = row[1]

        answer_mr = row[2]

        for k in keywords:

            k = k.strip().lower()

            if k in question:

                if language == "marathi":

                    return answer_mr.replace(";", "\n")

                else:

                    return answer_en.replace(";", "\n")

    return None 

# ---------------- DISEASE DETECTION ----------------
def detect_disease(filepath, language):

    img = cv2.imread(filepath)

    if img is None:

        if language == "marathi":

            return "❌ फोटो वाचता आला नाही."

        else:

            return "❌ Unable to read image."

    # Resize image
    img = cv2.resize(img, (300, 300))

    # Convert to HSV
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # ---------------- YELLOW DETECTION ----------------
    lower_yellow = (20, 100, 100)

    upper_yellow = (35, 255, 255)

    yellow_mask = cv2.inRange(
        hsv,
        lower_yellow,
        upper_yellow
    )

    yellow_pixels = cv2.countNonZero(yellow_mask)

    print("Yellow Pixels:", yellow_pixels)

    # ---------------- BLACK DETECTION ----------------

    lower_black = (0, 0, 0)

    upper_black = (180, 255, 50)

    black_mask = cv2.inRange(

        hsv,

        lower_black,

        upper_black
    )

    black_pixels = cv2.countNonZero(

        black_mask
    )

    print(
        "Black Pixels:",
        black_pixels
    )

    # ---------------- DISEASE RESULTS ----------------

    results = []


    # ---------------- YELLOW DISEASE ----------------

    if yellow_pixels > 3000:

        if yellow_pixels > 5000:

            confidence_en = "High"
            confidence_mr = "जास्त"

        else:

            confidence_en = "Medium"
            confidence_mr = "मध्यम"


        if language == "marathi":

            results.append(

                "🌿 पान पिवळे पडण्याची समस्या आढळली.\n"

                f"📊 खात्री : {confidence_mr}\n"

                "✅ उपाय : संतुलित खत वापरा."
            )

        else:

            results.append(

                "🌿 Yellow Leaf Problem Detected.\n"

                f"📊 Confidence : {confidence_en}\n"

                "✅ Suggestion : Use balanced fertilizer."
            )


    # ---------------- BLACK SPOTS ----------------

    if black_pixels > 3000:

        if black_pixels > 5000:

            confidence_en = "High"
            confidence_mr = "जास्त"

        else:

            confidence_en = "Medium"
            confidence_mr = "मध्यम"


        if language == "marathi":

            results.append(

                "⚫ पानावर काळे डाग आढळले.\n"

                f"📊 खात्री : {confidence_mr}\n"

                "✅ उपाय : बुरशीनाशक फवारणी करा."
            )

        else:

            results.append(

                "⚫ Black Spot Disease Detected.\n"

                f"📊 Confidence : {confidence_en}\n"

                "✅ Suggestion : Apply fungicide spray."
            )


    # ---------------- FINAL RESULT ----------------

    if results:

        return "\n\n".join(results)

    else:

        if language == "marathi":

            return (

                "रोग ओळखता आला नाही.\n"
                "कृपया स्पष्ट पानाचा फोटो अपलोड करा."
            )

        else:

            return (

                "Disease not detected.\n"
                "Please upload a clear leaf image."
            )
# ---------------- MAIN CHATBOT ----------------
def chatbot_response(question):

    question = str(question)

    language = detect_language(question)

    question = question.strip().lower()

    detected_crop = detect_crop(question)

    print("Detected Crop:", detected_crop)

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

     city = "Pune"

     for word in words:

        if word not in [
            "aaj",
            "paus",
            "padnar",
            "aahe",
            "ka",
            "udya",
            "tomorrow",
            "rain",
            "madhe",
            "gahu"
        ]:

            city = word
            break

     print("Detected City:", city)

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

        city = "Pune"

        for word in words:

            if word not in [

                "weather",
                "havaman",
                "हवामान",

                "tomato",
                "टोमॅटो",

                "onion",
                "कांदा",
                "kanda",

                "cotton",
                "कापूस",
                "kapus"

            ]:

                city = word

                break

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

    conn.commit()

    conn.close()

    for attempt in range(5):
      try:
        prompt = f"""
        You are an expert agricultural assistant for Indian farmers, 
        especially Maharashtra farmers.

        Rules:
        - Answer in {"Marathi" if language == "marathi" else "English"} only
        - Give practical, specific farming advice
        - Mention exact quantities when possible (like "10 kg per acre")
        - Keep answer under 100 words
        - Use simple language farmers can understand
        - Add relevant emojis for clarity

        Question: {question}
        """
      
        response = groq_client.chat.completions.create(
          model="llama-3.3-70b-versatile",
          messages=[
            {
              "role": "system",
              "content": """You are an expert farming assistant for Maharashtra farmers. Always give practical, specific advice with exact quantities. Never give vague answers.
              STRICT RULES:
              - Plain text only
              - NO HTML tags
              - NO markdown
              - NO links or URLs
              - NO asterisks or symbols
              - Simple emojis only
              - Maximum 4 lines
              - Practical advice only"""
            
            },
            {
              "role": "user",
              "content": prompt
           }
          ],
          temperature=0.7,
          max_tokens=200,
          timeout=10
        )
        raw = response.choices[0].message.content
        print("Groq Raw Answer:", raw)

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
            print(f"Rate limit — waiting 5 sec... attempt {attempt+1}")
            time.sleep(10)
       else:      
        print("Groq Error:",e)
        break
    if language == "marathi":
        return "कृपया अधिक माहिती द्या."
    else:
        return "Please provide more information."