import requests
import mysql.connector

# === CONFIG ===
API_KEY = "Api_key from openweather_app"  # Replace with your real API key

DB_CONFIG = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': 'your_mysql_password',  # Replace with your MySQL password
    'database': 'weather_app'
}

# === Connect to MySQL ===
def connect_db():
    try:
        return mysql.connector.connect(**DB_CONFIG)
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        exit()

# === Store weather info in DB ===
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
    print("Weather info saved to database.")

# === Get current weather ===
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
            print(f"\nCity not found. Error: {data.get('message', 'Unknown error')}\n")
            return

        city = data['name']
        country = data['sys']['country']
        temp = data['main']['temp']
        humidity = data['main']['humidity']
        desc = data['weather'][0]['description']

        print(f"\nWeather in {city}, {country}")
        print(f"Condition : {desc.capitalize()}")
        print(f"Temperature: {temp}°C")
        print(f"Humidity   : {humidity}%")

        store_weather_log(city, country, temp, humidity, desc)

    except requests.RequestException as e:
        print(f"\nNetwork error: {e}\n")

# === MAIN LOOP ===
print("Weather Checker — Type a city name or 'exit' to quit.")

while True:
    city_input = input("\nEnter a city name: ").strip()
    if city_input.lower() == 'exit':
        print("Exiting Weather App.")
        break
    get_current_weather(city_input)
