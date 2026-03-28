import random
from datetime import datetime


def fetch_weather_data(city):
    # simulacija API odgovora
    return {
        "city": city,
        "temp": round(random.uniform(10, 30), 1),
        "condition": random.choice(["sunny", "rainy", "cloudy", "partly cloudy"]),
        "humidity": random.randint(40, 90)
    }


def fetch_forecast(city, days=3):
    forecast = []
    for i in range(days):
        forecast.append({
            "day": i + 1,
            "temp": round(random.uniform(10, 30), 1),
            "condition": random.choice(["sunny", "rainy", "cloudy", "partly cloudy"])
        })
    return forecast


def get_current_hour():
    return datetime.now().hour