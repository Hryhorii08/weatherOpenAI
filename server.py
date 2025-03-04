from flask import Flask, request, jsonify
import requests
import datetime

app = Flask(__name__)

# Твой Telegram-бот
TELEGRAM_BOT_TOKEN = "7788946008:AAGULYh-GIkpr-GA3ZA70ERdCAT6BcGNW-g"
CHAT_ID = "-1002307069728"

# Функция получения погоды (оставляем как у тебя)
def get_weather_data(city):
    weather_info = {
        "city": city,
        "temperature": "6.4°C",
        "humidity": "67%",
        "wind_speed": "2.9 km/h",
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Добавляем время запроса
    }
    return weather_info

# Функция отправки сообщения в Telegram
def send_telegram_message(message):
    telegram_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }
    requests.post(telegram_url, json=payload)

# API-эндпоинт
@app.route("/weather", methods=["POST"])
def weather_endpoint():
    data = request.get_json()
    city = data.get("city")

    if not city:
        return "Ошибка: Город не указан.", 400

    weather_info = get_weather_data(city)

    message = (
        f"Данные из OpenAI\n"
        f"🌍 Погода в {weather_info['city']}:\n"
        f"🌡 Температура: {weather_info['temperature']}\n"
        f"💧 Влажность: {weather_info['humidity']}\n"
        f"💨 Ветер: {weather_info['wind_speed']}\n"
        f"⏱ Время запроса: {weather_info['timestamp']}"
    )

    send_telegram_message(message)

    return message  # Возвращаем текстовый ответ в OpenAI

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
