from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# 🔑 Данные для Telegram
TELEGRAM_BOT_TOKEN = "7788946008:AAGULYh-GIkpr-GA3ZA70ERdCAT6BcGNW-g"
CHAT_ID = "-1002307069728"

# 🌍 Функция получения погоды
def get_weather_data(city):
    geocode_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&format=json"
    geocode_response = requests.get(geocode_url)
    geocode_data = geocode_response.json()

    if "results" in geocode_data:
        lat = geocode_data["results"][0]["latitude"]
        lon = geocode_data["results"][0]["longitude"]
    else:
        return {"error": "Город не найден"}

    weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m&timezone=auto"
    response = requests.get(weather_url)
    data = response.json()

    if "hourly" not in data:
        return {"error": "Не удалось получить данные о погоде"}

    temperature = data["hourly"]["temperature_2m"][0]
    humidity = data["hourly"]["relative_humidity_2m"][0]
    wind_speed = data["hourly"]["wind_speed_10m"][0]

    return {
        "city": city,
        "temperature": f"{temperature}°C",
        "humidity": f"{humidity}%",
        "wind_speed": f"{wind_speed} km/h"
    }

# 📡 Функция отправки в Telegram
def send_telegram_message(message):
    telegram_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }
    requests.post(telegram_url, json=payload)

# 🚀 API для обработки запроса
@app.route("/weather", methods=["POST"])
def weather_endpoint():
    data = request.get_json()
    city = data.get("city")

    if not city:
        return jsonify({"error": "Город не указан"}), 400

    weather_info = get_weather_data(city)

    if "error" not in weather_info:
        message = (
            f"Данные из OpenAI\n"
            f"🌍 Погода в {weather_info['city']}:\n"
            f"🌡 Температура: {weather_info['temperature']}\n"
            f"💧 Влажность: {weather_info['humidity']}\n"
            f"💨 Ветер: {weather_info['wind_speed']}"
        )
        send_telegram_message(message)

    return jsonify(weather_info)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
