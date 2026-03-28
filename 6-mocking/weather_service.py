import api_client


def get_weather(city):
    try:
        return api_client.fetch_weather_data(city)
    except TimeoutError:
        return {"error": "timeout"}
    except Exception:
        return {"error": "api_error"}


def get_forecast(city, days=3):
    return api_client.fetch_forecast(city, days)


def is_good_weather(conditions):
    return conditions.lower() in ["sunny", "partly cloudy"]


def get_greeting_based_on_time():
    hour = api_client.get_current_hour()

    if 5 <= hour < 12:
        return "Good morning"
    elif 12 <= hour < 18:
        return "Good afternoon"
    else:
        return "Good evening"