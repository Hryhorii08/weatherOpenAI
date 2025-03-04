from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# 🌑 Данные для Telegram
TELEGRAM_BOT_TOKEN = "7788946008:AAGULYh-GIkpr-GA3ZA70ERdCAT6BcGNW-g"
CHAT_ID = "-1002307069728"

def get_weather_data(city):
    # Заглушка: здесь должен быть запрос к API погоды
    return {
        "city": city,
        "temperature": "6.4°C",
        "humidity": "67%",
        "wind_speed": "2.9 km/h"
    }

@app.route("/weather", methods=["POST"])
def weather_endpoint():
    data = request.get_json()
    city = data.get("city")

    if not city:
        return "Город не указан", 400

    weather_info = get_weather_data(city)

    if "error" not in weather_info:
        message = f"Данные из OpenAI\n🌍 Погода в {weather_info['city']}:\n🌡 Температура: {weather_info['temperature']}\n💧 Влажность: {weather_info['humidity']}\n💨 Ветер: {weather_info['wind_speed']}"
        send_telegram_message(message)

    return f"{weather_info['city']}: {weather_info['temperature']}, {weather_info['humidity']}, {weather_info['wind_speed']}"

def send_telegram_message(message):
    telegram_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }
    requests.post(telegram_url, json=payload)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
