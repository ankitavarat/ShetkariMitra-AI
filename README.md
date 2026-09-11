# 🌾 ShetkariMitra AI

### AI-Powered Bilingual Farm Assistant for Maharashtra Farmers

**ShetkariMitra AI** is a farmer-focused AI-powered Progressive Web App (PWA) designed to make practical agricultural information easier to access, understand, and use.

The platform brings together **AI farming assistance, Marathi + English interaction, voice input/output, weather information, rain guidance, agricultural market prices, crop guidance, organic farming support, water advice, and crop disease detection** in one farmer-friendly application.

The project started as an idea to build a useful agricultural assistant and has gradually evolved into a more complete **AgriTech product prototype with authentication, persistent user data, cloud database integration, PWA support, and real-world agricultural APIs.**

---

## 🎯 The Problem

Farmers often need information from multiple places for everyday decisions:

* 🌦️ Weather and rainfall conditions
* 💰 Agricultural market/mandi prices
* 🌱 Crop-related guidance
* 🦠 Crop disease identification
* 💧 Water-management advice
* 🌿 Organic farming information
* 🗣️ Easy access to information in a familiar language

For many users, especially in rural areas, information that is technically available online is not always presented in a simple, practical, farmer-friendly way.

**ShetkariMitra AI aims to bring these everyday agricultural needs together in a single accessible platform.**

---

## 💚 The Story Behind ShetkariMitra AI

ShetkariMitra AI started with a personal observation.

My father is a farmer, and growing up, I have seen the everyday challenges that farmers face while making decisions about weather, crops, water, market prices and crop-related problems.

I realized that farmers often need different types of information at different times, but accessing the right information in a simple and understandable way can still be difficult.

This made me think:

> **What if one simple platform could bring useful agricultural information together and allow farmers to ask questions naturally?**

That thought became the starting point of **ShetkariMitra AI**.

What began as a personal idea inspired by my father's farming experience gradually developed into a larger AgriTech project combining **AI, agricultural data, weather information, market prices, voice interaction, computer vision, authentication, PostgreSQL and PWA technology.**

The goal is simple:

> 🌾 **Build technology that understands the real problems farmers face and makes useful information easier to access.**

# 💡 Our Solution

ShetkariMitra AI provides a single digital assistant where a farmer can:

> **Ask → Understand → Check → Decide**

Instead of switching between different applications and websites, users can interact with one farming assistant for multiple everyday agricultural needs.

---

# 🚀 Key Features

## 🤖 AI Farming Assistant

An AI-powered conversational assistant designed for agriculture-related questions.

Farmers can ask questions about:

* 🌱 Crop cultivation
* 🌾 Farming practices
* 💧 Water management
* 🌿 Organic farming
* 🦠 Crop problems
* 🌦️ Weather-related farming decisions
* 🚜 General agricultural queries

The assistant is designed to provide **simple, practical and farmer-friendly responses** rather than highly technical explanations.

---

## 🌐 Marathi + English Support

ShetkariMitra AI supports interaction in:

* 🇮🇳 Marathi
* 🇬🇧 English

The goal is to make agricultural technology more accessible to farmers who may prefer communicating in their familiar language.

---

## 🎙️ Voice Input & Voice Output

ShetkariMitra AI supports **voice-based interaction** so users can communicate with the assistant without depending completely on typing.

### Voice Input

Users can speak their farming question instead of typing it.

### Voice Output

The assistant can read the response aloud, making information easier to consume while working in the field or when reading is inconvenient.

This creates a more natural interaction between the farmer and the application.

---

## 🌦️ Weather Information

The application provides weather-related information using weather services and location-based data.

Farmers can use weather information while planning activities such as:

* 🌱 Sowing
* 💧 Irrigation
* 🌾 Crop management
* 🌧️ Rain-sensitive activities
* 🚜 Field operations

The application also uses location information to provide more relevant weather context.

---

## 🌧️ Rain & Weather-Based Farming Guidance

Weather information is combined with agricultural guidance to help users understand how changing weather conditions may affect farming activities.

Examples include:

* Rain-related crop precautions
* Irrigation considerations
* Weather-sensitive farming activities
* Practical farming suggestions based on conditions

---

# 💰 Agricultural Market / Mandi Prices

One of the important features of ShetkariMitra AI is access to **agricultural market prices**.

The application integrates agricultural market data to help farmers check available mandi/market prices for crops.

### Supported crop examples include:

* 🧅 Onion / Kanda
* 🌾 Wheat / Gahu
* 🥔 Potato / Batata
* 🍅 Tomato
* 🌿 Cotton / Kapus

The feature is designed around agricultural market data from government sources such as **AGMARKNET/data.gov.in**.

> The availability and freshness of prices depend on the underlying government market-data source.

---

# 🌱 Crop Guidance

Farmers can ask the AI assistant for practical guidance related to crop cultivation and management.

Topics can include:

* Crop-growing practices
* Basic crop care
* Farming recommendations
* Weather-related precautions
* Water requirements
* General crop-management questions

The goal is to provide information in a format that is easier to understand and apply.

---

# 🌿 Organic Farming Support

ShetkariMitra AI also provides information related to organic and natural farming practices.

Users can ask about:

* Organic farming methods
* Natural farming practices
* Organic inputs
* Crop-care approaches
* Sustainable agricultural practices

---

# 💧 Water & Irrigation Guidance

Water management is an important part of farming.

The assistant can help users with questions related to:

* Irrigation
* Water requirements
* Water-saving practices
* Crop and weather considerations
* Practical water-management decisions

---

# 🦠 Crop Disease Detection

ShetkariMitra AI includes a crop-image analysis feature using **OpenCV-based image processing**.

The application analyzes visual characteristics of a crop/leaf image to provide an initial indication of possible crop-health issues.

The current implementation uses image-processing techniques rather than claiming a fully trained deep-learning disease-classification model.

### Current approach

* 📷 Image input
* 🔍 OpenCV processing
* 🎨 Color/visual analysis
* 🧪 Basic crop-health indication
* 💡 Supporting guidance through the application

This feature is designed as an initial assistive tool and is not intended to replace professional agricultural diagnosis.

---

# 👤 User Registration & Login

ShetkariMitra AI includes user authentication.

Users can:

* 📝 Create an account
* 🔐 Log in
* 👤 Access their own application data
* 💬 Maintain their own conversation history

Authentication and database functionality are implemented using **Supabase and PostgreSQL**.

---

# 🗄️ Persistent Chat History

Unlike a temporary chatbot, ShetkariMitra AI maintains user-specific conversation history.

Users can:

* 💬 Continue previous conversations
* 📚 View previous chats
* 👤 Keep their conversations associated with their account
* 🗑️ Delete individual conversations

This makes the assistant more useful as a continuing farming-support tool.

---

# 🗑️ Individual Chat Deletion

Users can delete individual conversations from their chat history.

This provides better control over personal conversation data and keeps the history organized.

---

# 🔐 Supabase + PostgreSQL Backend

ShetkariMitra AI uses **Supabase with PostgreSQL** for its cloud-backed user and application data.

The backend architecture supports:

* 🔐 Authentication
* 👤 User accounts
* 🗄️ PostgreSQL database
* 💬 Persistent chat data
* 🗑️ Chat deletion
* 🔑 User-specific data handling

Supabase Auth is integrated with PostgreSQL and supports authenticated access to application data.

---

# 📱 Progressive Web App (PWA)

ShetkariMitra AI is designed as a **Progressive Web App**, allowing the application to provide an app-like experience through the web.

### PWA capabilities include:

* 📱 Mobile-friendly interface
* 🖥️ Responsive web experience
* 📲 Installable application experience
* ⚡ App-like navigation
* 🔄 PWA manifest
* 📦 Service-worker based functionality

A web app manifest is a core part of making a PWA installable, while service workers are commonly used to provide enhanced/offline experiences.

---

# 🧩 Technology Stack

| Layer                        | Technology                |
| ---------------------------- | ------------------------- |
| **Programming Language**     | Python                    |
| **Backend Framework**        | Flask                     |
| **Frontend**                 | HTML, CSS, JavaScript     |
| **AI Assistant**             | Groq LLM API              |
| **Database**                 | PostgreSQL                |
| **Backend Platform**         | Supabase                  |
| **Authentication**           | Supabase Auth             |
| **Computer Vision**          | OpenCV                    |
| **Weather Data**             | OpenWeatherMap            |
| **Location / Geocoding**     | Nominatim                 |
| **Agricultural Market Data** | data.gov.in / AGMARKNET   |
| **Application Type**         | Progressive Web App (PWA) |
| **Version Control**          | Git & GitHub              |
| **Deployment**               | Render                    |

---

# 🏗️ High-Level Architecture

```text
                         ┌──────────────────────┐
                         │      Farmer/User     │
                         └──────────┬───────────┘
                                    │
                    Text / Voice / Image / Location
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │   ShetkariMitra AI   │
                         │       Frontend       │
                         │    HTML/CSS/JS/PWA   │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │    Flask Backend     │
                         │      Python API      │
                         └──────────┬───────────┘
                                    │
             ┌──────────────────────┼──────────────────────┐
             │                      │                      │
             ▼                      ▼                      ▼
      ┌─────────────┐       ┌──────────────┐       ┌──────────────┐
      │ AI / Groq   │       │ Weather API  │       │ Market Data  │
      │ Assistant   │       │              │       │ AGMARKNET    │
      └─────────────┘       └──────────────┘       └──────────────┘
             │                      │                      │
             └──────────────────────┼──────────────────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │ Supabase + PostgreSQL│
                         │ Auth + User Data +   │
                         │ Persistent History   │
                         └──────────────────────┘
```

---

# 🔄 How the Application Works

### 1. User Registration / Login

The farmer creates an account and logs into the application.

### 2. User Interaction

The farmer can:

* Type a question
* Speak a question
* Ask about weather
* Check market prices
* Upload a crop image
* Ask for farming guidance

### 3. Backend Processing

The Flask backend processes the request and communicates with the required service.

### 4. Information Retrieval / AI Processing

Depending on the request, the application can use:

* AI model
* Weather service
* Agricultural market data
* Location services
* OpenCV image processing

### 5. Response

The result is presented in a simple farmer-friendly format.

### 6. Conversation Storage

Authenticated conversations can be stored in PostgreSQL and accessed later through the user's chat history.

---

# 📂 Project Structure

```text
ShetkariMitra-AI/
│
├── app.py
├── requirements.txt
├── README.md
│
├── templates/
│   └── ...
│
├── static/
│   ├── css/
│   ├── js/
│   ├── icons/
│   └── ...
│
├── screenshots/
│   ├── login.png
│   ├── register.png
│   ├── dashboard.png
│   ├── chat.png
│   ├── voice.png
│   ├── weather.png
│   ├── market-prices.png
│   ├── disease-detection.png
│   └── history.png
│
├── manifest.json
├── service-worker.js
│
└── ...
```

> The exact file structure may change as the project continues to evolve.

---

## 📸 Application Screenshots

### 🔐 Registration
![Registration](screenshot/register.jpg)

### 📝 Login
![Login](screenshot/login.jpg)

### 🏠 Main Dashboard
![Main Dashboard](screenshot/dashboard.jpg)

### 🤖 AI Chat
![AI Chat](screenshot/chat.jpg)

### 🤖 Menu
![Menu](screenshot/menu.jpg)

### 💬 Chat History
![Chat History](screenshot/history.jpg)

### 💬 Live Market
![Live Market](screenshot/livemarket.jpg)

### 🌦️ Weather Information
![Weather Information](screenshot/weather.jpg)

### 🦠 Crop Disease Detection
![Crop Disease Detection](screenshot/disease.jpg)

---

# 🌾 From Idea to Product

ShetkariMitra AI was developed incrementally rather than as a single college-demo implementation.

### Phase 1 — Initial Farming Assistant

The project began with the idea of creating an AI assistant that could answer agricultural questions.

### Phase 2 — Farmer-Focused Responses

The assistant was refined toward simpler, practical responses suitable for farmers.

### Phase 3 — Marathi + English

Bilingual interaction was introduced to make the system more accessible.

### Phase 4 — Weather Integration

Weather and location-based information were added to make the assistant more useful for real farming decisions.

### Phase 5 — Agricultural Guidance

Crop guidance, organic farming and water-management support were added.

### Phase 6 — Crop Disease Detection

OpenCV-based image processing was introduced to provide an initial crop-health/disease-support feature.

### Phase 7 — Agricultural Market Prices

Government agricultural market data was integrated so users could access available mandi/market price information.

### Phase 8 — Voice Interaction

Voice input and voice output were introduced to make interaction easier for users who may prefer speaking instead of typing.

### Phase 9 — User Authentication

Registration and login were added so the application could support individual users.

### Phase 10 — PostgreSQL & Persistent Data

The application moved toward cloud-backed persistent storage using Supabase and PostgreSQL.

### Phase 11 — Personal Chat History

User-specific conversations were added so previous interactions could be accessed later.

### Phase 12 — Individual Chat Deletion

Users were given control to delete individual conversations.

### Phase 13 — Progressive Web App

The application was developed as a PWA to provide a more app-like experience on mobile devices.

### Phase 14 — Deployment & Continuous Improvement

The application was deployed and continues to be improved based on testing, usability and real-world product requirements.

---

# 🎯 Product Vision

The long-term vision of ShetkariMitra AI is to become a **practical digital farming companion** rather than just a chatbot.

The goal is to bring multiple useful agricultural services into one accessible platform:

```text
                 🌾 SHETKARIMITRA AI
                         │
       ┌─────────────────┼─────────────────┐
       │                 │                 │
       ▼                 ▼                 ▼
   🤖 AI Help       🌦️ Weather        💰 Markets
       │                 │                 │
       ├─────────────────┼─────────────────┤
       │                 │                 │
       ▼                 ▼                 ▼
   🌱 Crops          🦠 Disease        💧 Water
       │                 │                 │
       └─────────────────┼─────────────────┘
                         │
                         ▼
                🎙️ Voice Interaction
                         │
                         ▼
                 👨‍🌾 Farmer-Friendly
                    Experience
```

---

# 🚀 Future Roadmap

The project is designed to grow beyond its current implementation.

### 🔬 AI & Agriculture

* Improved crop-disease detection
* Better crop-specific recommendations
* More structured agricultural knowledge
* More reliable farming decision support

### 🌦️ Smart Farming Information

* More detailed weather-based recommendations
* Regional agricultural alerts
* Better market-price discovery
* Additional crop and mandi coverage

### 🗣️ Accessibility

* Improved Marathi voice interaction
* Support for additional Indian languages
* Better voice-first workflows
* More accessible UI for rural users

### 📱 Product Development

* Improved PWA experience
* Better mobile performance
* Expanded farmer services
* More personalized user experience

### 🌾 Long-Term Vision

Build a scalable agricultural technology platform that combines:

**AI + Agricultural Data + Weather + Market Information + Voice + Computer Vision**

into one farmer-centered ecosystem.

---

# 🔒 Data & Security Approach

The application uses authenticated user accounts and cloud-backed PostgreSQL storage.

Key principles include:

* User authentication
* User-specific application data
* Persistent conversation storage
* Controlled access to database records
* Individual conversation deletion

Supabase provides authentication and PostgreSQL database capabilities, with Row Level Security available for fine-grained data access control.

---

# 🛠️ Development

## Clone the repository

```bash
git clone https://github.com/ankitavarat/ShetkariMitra-AI.git
cd ShetkariMitra-AI
```

## Create a virtual environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

## Install dependencies

```bash
pip install -r requirements.txt
```

## Configure environment variables

Create a `.env` file and add the required API keys and configuration values.

Example:

```env
GROQ_API_KEY=your_groq_api_key
OPENWEATHER_API_KEY=your_openweather_api_key

SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
```

> Never commit real API keys, passwords, database credentials, or other secrets to GitHub.

## Run the application

```bash
python app.py
```

Then open the local application in your browser.

---

# 🌐 External Services & APIs

ShetkariMitra AI uses external services to provide specialized functionality.

| Service                     | Purpose                              |
| --------------------------- | ------------------------------------ |
| **Groq**                    | AI-powered conversational responses  |
| **Supabase**                | Authentication and backend services  |
| **PostgreSQL**              | Persistent application/user data     |
| **OpenWeatherMap**          | Weather information                  |
| **Nominatim**               | Location / reverse-geocoding support |
| **data.gov.in / AGMARKNET** | Agricultural market data             |
| **OpenCV**                  | Crop-image processing                |

---

# ⚠️ Important Disclaimer

ShetkariMitra AI is an **assistive agricultural information platform**.

Information generated by the AI or external data services may not always be complete, current, or suitable for every farm situation.

Farmers should verify important decisions with:

* Qualified agricultural experts
* Local agricultural officers
* Krishi Vigyan Kendras
* Trusted agricultural institutions
* Official government sources

Crop-disease detection is intended as an initial assistive indication and should not be treated as a definitive professional diagnosis.

---

# 🌟 Why ShetkariMitra AI?

ShetkariMitra AI is not designed as just a basic chatbot.

The project combines multiple technologies into one practical agricultural product:

```text
              Python + Flask
                    │
                    ▼
              AI Assistant
                    │
       ┌────────────┼────────────┐
       ▼            ▼            ▼
   Weather       Market       Computer
    Data         Prices        Vision
       │            │            │
       └────────────┼────────────┘
                    ▼
             Voice Interaction
                    │
                    ▼
          Supabase + PostgreSQL
                    │
                    ▼
          Persistent User History
                    │
                    ▼
                  PWA
                    │
                    ▼
          👨‍🌾 Farmer-Centered
             Digital Platform
```

---

# 👩‍💻 Developer

### Ankita Varat

**B.E. Information Technology**

Maharashtra, India

ShetkariMitra AI is an **individual project** developed with the goal of exploring how AI, software engineering, agricultural data and accessible technology can be combined to solve real-world problems.

---

# 📌 Project Status

**Status:** 🚧 Active Development

ShetkariMitra AI is continuously being improved with new features, testing, UI improvements, agricultural services and product-level enhancements.

---

## ⭐ Support the Project

If you find **ShetkariMitra AI** interesting or useful:

⭐ Star the repository
🍴 Fork the project
💡 Share feedback
🐛 Report issues
🤝 Contribute ideas

---

## 🌾 Built with a simple idea

> **Technology should not make farming more complicated.
> It should make useful information easier to access.**

### 🌱 ShetkariMitra AI — Technology for Farmers.


---


⭐ If you find this project interesting, consider giving it a star on GitHub.
