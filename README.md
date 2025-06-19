# 🌦️ CityCast App

CityCast is a voice-assisted weather application built with Python that:
- Provides real-time weather information for any city in the world
- Suggests clothing based on weather
- Stores weather data in a MySQL database
- Supports both **text** and **voice** input
- Uses AI to answer follow-up weather questions
- Detects your location automatically

---

## Features

✅ **Real-time Weather** — Get current temperature, humidity, and conditions  
✅ **Voice Interaction** — Ask for weather by speaking into your mic  
✅ **AI Chatbot Integration** — Gemini-powered assistant answers weather questions  
✅ **Follow-up Questions** — Continue asking about the same city  
✅ **Clothing Tips** — Suggests what to wear based on weather  
✅ **Auto Location Detection** — Get weather based on IP or location  
✅ **MySQL Database Logging** — Saves every searched city's weather data

---

## Technologies Used

- Python 3.x  
- [OpenWeatherMap API](https://openweathermap.org/)  
- [Google Gemini AI](https://ai.google.dev/)  
- MySQL  
- SpeechRecognition  
- Pyttsx3 (Text-to-speech)  
- Geocoder (IP-based location)  
- PyCountry (Full country names)  

---

## Setup Instructions

### 1. Get API Keys
- **OpenWeatherMap API Key:** [Get here](https://home.openweathermap.org/users/sign_up)
- **Gemini API Key:** [Get here](https://ai.google.dev/)

### 2. Create MySQL Database
```sql
CREATE DATABASE weather_app;
USE weather_app;

CREATE TABLE city_weather_log (
    id INT AUTO_INCREMENT PRIMARY KEY,
    city_name VARCHAR(100),
    country VARCHAR(100),
    temperature FLOAT,
    humidity INT,
    weather_desc VARCHAR(255),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```
### 3. Install required dependencies
pip install requests mysql-connector-python speechrecognition pyttsx3 geocoder pycountry google-generativeai

###4. Configure the App
API_KEY = "your_openweather_api_key"
GEMINI_API_KEY = "your_gemini_api_key"

🧑‍💻 How to Use
Step 1: Run the App
In bash terminal:
python citycast.py

Step 2: Choose Input Type
1 → Type your inputs manually

2 → Use your microphone to speak

Step 3: Choose Task
Search a city → Get weather for any city

My location → Detect your location and fetch weather

Weather chatbot → Ask questions like “Is it raining in Delhi?”

Precise location weather → Use IP to get accurate current location weather

💬 Example Voice Commands
“Search city” → then say “Kolkata”

“Chatbot” → then ask “Will it rain in Mumbai tomorrow?”

“Precise location” → gets your current location via IP

📝 To Do / Ideas for Future
1.Export weather history to CSV
2.Add hourly forecasts
3.GUI version with Tkinter or Streamlit
4.Mobile-friendly version
5.Reminder notifications for rain/cold days

Created By-
Raima Deb
2nd-year Computer Science Student

