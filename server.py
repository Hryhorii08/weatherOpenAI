import requests
import datetime
from flask import Flask, request, jsonify

app = Flask(__name__)

# 🔑 Данные для Telegram
TELEGRAM_BOT_TOKEN = "7788946008:AAGULYh-GIkpr-GA3ZA70ERdCAT6BcGNW-g"
CHAT_ID = "-1002307069728"

# 🌍 Функция для получения погоды (каждый раз делает новый запрос)
def fetch_weather(city):
    geocode_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&format=json"
    geocode_response = requests.get(geocode_url)
    geocode_data = geocode_response.json()

    if "results" not in geocode_data:
        return {"error": "Город не найден"}

    lat = geocode_data["results"][0]["latitude"]
    lon = geocode_data["results"][0]["longitude"]

    weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m&timezone=auto"
    weather_response = requests.get(weather_url)
    weather_data = weather_response.json()

    if "hourly" not in weather_data:
        return {"error": "Не удалось получить данные о погоде"}

    temp = round(weather_data["hourly"]["temperature_2m"][0])
    humidity = weather_data["hourly"]["relative_humidity_2m"][0]
    wind_speed = round(weather_data["hourly"]["wind_speed_10m"][0])

    # Добавляем время запроса
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return {
        "city": city,
        "temperature": f"{temp}°C",
        "humidity": f"{humidity}%",
        "wind_speed": f"{wind_speed} km/h",
        "timestamp": timestamp
    }

# 📡 Функция отправки сообщения в Telegram
def send_telegram_message(message):
    telegram_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }
    requests.post(telegram_url, json=payload)

# 🚀 API для получения погоды
@app.route('/weather', methods=['POST'])
def weather():
    data = request.get_json()
    city = data.get("city", "")

    if not city:
        return jsonify({"error": "City is required"}), 400

    weather_data = fetch_weather(city)

    if "error" not in weather_data:
        message = (
            f"Данные из OpenAI\n"
            f"🌍 Погода в {weather_data['city']}:\n"
            f"🌡 Температура: {weather_data['temperature']}\n"
            f"💧 Влажность: {weather_data['humidity']}\n"
            f"💨 Ветер: {weather_data['wind_speed']}\n"
            f"⏱ Время запроса: {weather_data['timestamp']}"
        )
        send_telegram_message(message)

    return weather_data["city"] + " | " + weather_data["temperature"] + " | " + weather_data["humidity"] + " | " + weather_data["wind_speed"] + " | " + weather_data["timestamp"]

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
