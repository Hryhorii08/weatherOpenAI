from flask import Flask, request, jsonify
import requests
import time
import os

app = Flask(__name__)

# Конфигурация токенов
TELEGRAM_BOT_TOKEN = os.getenv("7788946008:AAGULYh-GIkpr-GA3ZA70ERdCAT6BcGNW-g")
CHAT_ID = os.getenv("-1002307069728")

# Функция получения данных о погоде
def get_weather_data(city):
    api_url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid=YOUR_WEATHER_API_KEY&units=metric&lang=ru"
    response = requests.get(api_url)
    
    if response.status_code != 200:
        return {"error": "Не удалось получить данные о погоде."}
    
    data = response.json()
    
    weather_info = {
        "city": data["name"],
        "temperature": f"{data['main']['temp']}°C",
        "humidity": f"{data['main']['humidity']}%",
        "wind_speed": f"{data['wind']['speed']} km/h",
        "timestamp": int(time.time())  # Уникальный временной метка
    }
    
    return weather_info

# Функция отправки сообщения в Telegram
def send_telegram_message(message):
    telegram_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    requests.post(telegram_url, json=payload)

# API-эндпоинт обработки запроса
@app.route("/weather", methods=["POST"])
def weather_endpoint():
    data = request.get_json()
    city = data.get("city")
    
    if not city:
        return jsonify({"error": "Город не указан"}), 400

    # Запрашиваем данные о погоде
    weather_info = get_weather_data(city)

    # Если данные получены, отправляем в Telegram и OpenAI
    if "error" not in weather_info:
        message = (
            f"*Данные из OpenAI*\n"
            f"🌍 Погода в {weather_info['city']}:\n"
            f"🌡 Температура: {weather_info['temperature']}\n"
            f"💧 Влажность: {weather_info['humidity']}\n"
            f"💨 Ветер: {weather_info['wind_speed']}"
        )
        send_telegram_message(message)

    return jsonify(weather_info)  # Возвращаем данные в OpenAI

# Запуск сервера
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
