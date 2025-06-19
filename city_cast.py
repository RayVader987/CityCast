import requests
import mysql.connector
import speech_recognition as sr
import pyttsx3
import geocoder
import pycountry
import google.generativeai as genai
import re
from datetime import datetime, timedelta

# === CONFIGURATION ===
API_KEY = "your open_weather_app api here"  #Replace with your OpenWeatherApp API
GEMINI_API_KEY = "your gemini api here"  # Replace with your Gemini API key

DB_CONFIG = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': 'your MySQL password here',  #Replace with your MySQL password here
    'database': 'weather_app'
}

# === INIT TEXT-TO-SPEECH ENGINE ===
engine = pyttsx3.init()
def speak(text):
    print(text)
    engine.say(text)
    engine.runAndWait()

# === GET FULL COUNTRY NAME ===
def get_full_country_name(code):
    try:
        country = pycountry.countries.get(alpha_2=code.upper())
        return country.name if country else code
    except:
        return code

# === CONNECT TO MYSQL ===
def connect_db():
    try:
        return mysql.connector.connect(**DB_CONFIG)
    except mysql.connector.Error as err:
        speak(f"Database error: {err}")
        exit()

# === STORE WEATHER DATA IN DATABASE ===
def store_weather_log(city, country, temp, humidity, desc):
    conn = connect_db()
    cursor = conn.cursor()
    insert_query = """
        INSERT INTO city_weather_log (city_name, country, temperature, humidity, weather_desc)
        VALUES (%s, %s, %s, %s, %s)
    """
    values = (city, country, temp, humidity, desc)
    cursor.execute(insert_query, values)
    conn.commit()
    conn.close()
    speak("Weather info saved to database.")

# === CLOTHING SUGGESTIONS ===
def clothing_suggestion(desc, temp):
    desc = desc.lower()
    if 'rain' in desc:
        return "It might rain. Carry an umbrella!"
    elif 'clear' in desc or 'sun' in desc:
        return "It's sunny. Wear sunglasses and light clothes."
    elif 'snow' in desc:
        return "It's snowing. Wear heavy warm clothes."
    elif temp < 10:
        return "It's cold. Wear warm clothes."
    elif temp > 30:
        return "It's hot. Stay hydrated and wear light clothes."
    else:
        return "The weather is moderate. Dress comfortably."

# === FETCH CURRENT WEATHER ===
def get_current_weather(city_name):
    city_name = city_name.strip()
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': city_name,
        'appid': API_KEY,
        'units': 'metric'
    }

    try:
        res = requests.get(base_url, params=params)
        data = res.json()

        if res.status_code != 200 or str(data.get('cod')) != "200":
            speak(f"City not found. Error: {data.get('message', 'Unknown error')}")
            return

        city = data['name']
        country = get_full_country_name(data['sys']['country'])
        temp = data['main']['temp']
        humidity = data['main']['humidity']
        desc = data['weather'][0]['description']

        speak(f"\nWeather in {city}, {country}")
        speak(f"Condition : {desc.capitalize()}")
        speak(f"Temperature: {temp}°C")
        speak(f"Humidity   : {humidity}%")

        suggestion = clothing_suggestion(desc, temp)
        speak(f"Clothing Tip: {suggestion}")

        store_weather_log(city, country, temp, humidity, desc)

    except requests.RequestException as e:
        speak(f"Network error: {e}")

# === VOICE INPUT ===
def get_voice_input(prompt_text="Please say your input..."):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        speak(prompt_text)
        try:
            audio = r.listen(source, timeout=5)
            text = r.recognize_google(audio)
            speak(f"You said: {text}")
            return text
        except sr.UnknownValueError:
            speak("Sorry, I couldn't understand your voice.")
        except sr.RequestError:
            speak("Voice service not working.")
        except sr.WaitTimeoutError:
            speak("Listening timed out.")
    return None

# === AI WEATHER CHATBOT WITH FOLLOW-UP SUPPORT ===
last_city = None

def ai_chatbot(query):
    global last_city
    query_lower = query.lower()
    city_match = re.search(r'in ([a-zA-Z\s]+)', query_lower)

    if city_match:
        city_name = city_match.group(1).strip()
        last_city = city_name
    elif last_city:
        city_name = last_city
        speak(f"Using previous city: {city_name}")
    else:
        city_name = None

    if city_name:
        if "tomorrow" in query_lower:
            speak(f"Fetching tomorrow's forecast for {city_name}...")
            url = "http://api.openweathermap.org/data/2.5/forecast"
            params = {'q': city_name, 'appid': API_KEY, 'units': 'metric'}
            try:
                res = requests.get(url, params=params)
                data = res.json()
                if res.status_code != 200 or str(data.get('cod')) != "200":
                    speak(f"Couldn't find forecast data for {city_name}.")
                    return
                tomorrow = (datetime.utcnow() + timedelta(days=1)).date()
                forecasts = [item for item in data['list'] if datetime.utcfromtimestamp(item['dt']).date() == tomorrow]
                if not forecasts:
                    speak("No forecast available for tomorrow.")
                    return
                descs = [f['weather'][0]['description'] for f in forecasts]
                temps = [f['main']['temp'] for f in forecasts]
                avg_temp = round(sum(temps) / len(temps), 1)
                speak(f"Tomorrow in {city_name.capitalize()}, expect around {avg_temp}°C with conditions like: {', '.join(set(descs))}.")
            except Exception as e:
                speak(f"Error getting forecast: {e}")
            return

        elif "today" in query_lower or "now" in query_lower or "still" in query_lower or "rain" in query_lower:
            speak(f"Fetching current weather for {city_name}...")
            base_url = "http://api.openweathermap.org/data/2.5/weather"
            params = {'q': city_name, 'appid': API_KEY, 'units': 'metric'}
            try:
                res = requests.get(base_url, params=params)
                data = res.json()
                if res.status_code != 200 or str(data.get('cod')) != "200":
                    speak(f"Couldn't find weather data for {city_name}.")
                    return
                desc = data['weather'][0]['description']
                temp = data['main']['temp']
                is_rainy = "rain" in desc.lower()
                if "rain" in query_lower:
                    if is_rainy:
                        speak(f"Yes, it's currently raining in {city_name.capitalize()}.")
                    else:
                        speak(f"No, it's not raining in {city_name.capitalize()} right now. It's {desc}.")
                else:
                    speak(f"The weather in {city_name.capitalize()} is currently {desc} with {temp}°C temperature.")
            except Exception as e:
                speak(f"Error fetching weather: {e}")
            return

    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = f"You are a weather assistant. Answer the question: {query}"
    try:
        response = model.generate_content(prompt)
        speak(response.text)
    except Exception as e:
        speak(f"AI Error: {e}")

# === GET USER LOCATION ===
def get_user_location():
    g = geocoder.ip('me')
    if g.ok:
        return g.city
    return None

# === MAIN LOOP ===
while True:
    speak("\nChoose input type:\n1. Type Input\n2. Voice Input\nEnter your choice (1 or 2) or type 'exit' to quit:")
    input_type = input("Your choice: ").strip().lower()

    if input_type == 'exit':
        speak("Exiting City Cast App")
        break

    if input_type not in ['1', '2']:
        speak("Invalid option. Try again.")
        continue

    if input_type == '1':
        speak("\nWhat do you want to do?\nA. Search a city\nB. My location\nC. Weather chatbot\nD. Precise location weather\nEnter A, B, C, or D:")
        task_choice = input("Your choice: ").strip().lower()
    else:
        speak("Say: search city, my location, chatbot, or precise location")
        task_voice = get_voice_input("Speak your input now...")
        if task_voice is None:
            continue
        task_voice = task_voice.lower()
        if "search" in task_voice:
            task_choice = 'a'
        elif "my location" in task_voice:
            task_choice = 'b'
        elif "chat" in task_voice or "question" in task_voice:
            task_choice = 'c'
        elif "precise" in task_voice or "exact" in task_voice:
            task_choice = 'd'
        else:
            speak("Could not understand your choice. Please try again.")
            continue

    if task_choice == 'a':
        if input_type == '1':
            city = input("Enter city name: ").strip()
        else:
            city = get_voice_input("Say the city name.")
        if city:
            get_current_weather(city)

    elif task_choice == 'b':
        city = get_user_location()
        if city:
            speak(f"Detected location: {city}")
            get_current_weather(city)
        else:
            speak("Unable to detect your location.")

    elif task_choice == 'c':
        if input_type == '1':
            query = input("Enter your weather question: ").strip()
        else:
            query = get_voice_input("Ask your weather question.")
        if query:
            ai_chatbot(query)

    elif task_choice == 'd':
        g = geocoder.ip('me')
        if g.ok and g.city:
            speak(f"Your precise location is: {g.city}, {g.country}")
            get_current_weather(g.city)
        else:
            speak("Could not determine your precise location.")
    else:
        speak("Invalid option. Try again.")
