import unittest
from unittest.mock import Mock, patch
import weather_service


class TestWeatherService(unittest.TestCase):

    @patch("weather_service.api_client.fetch_weather_data")
    def test_get_weather_success(self, mock_fetch):
        mock_fetch.return_value = {
            "city": "Banja Luka",
            "temp": 25,
            "condition": "sunny",
            "humidity": 50
        }

        result = weather_service.get_weather("Banja Luka")

        self.assertEqual(result["city"], "Banja Luka")
        self.assertEqual(result["condition"], "sunny")

    @patch("weather_service.api_client.fetch_weather_data")
    def test_get_weather_api_error(self, mock_fetch):
        mock_fetch.side_effect = Exception("API error")

        result = weather_service.get_weather("Banja Luka")

        self.assertEqual(result, {"error": "api_error"})

    @patch("weather_service.api_client.fetch_weather_data")
    def test_get_weather_timeout(self, mock_fetch):
        mock_fetch.side_effect = TimeoutError()

        result = weather_service.get_weather("Banja Luka")

        self.assertEqual(result, {"error": "timeout"})

    @patch("weather_service.api_client.fetch_forecast")
    def test_get_forecast_with_patch(self, mock_fetch):
        mock_fetch.return_value = [
            {"day": 1, "temp": 20, "condition": "sunny"}
        ]

        result = weather_service.get_forecast("Banja Luka", 1)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["condition"], "sunny")

    @patch("weather_service.api_client.get_current_hour")
    def test_greeting_morning(self, mock_hour):
        mock_hour.return_value = 8

        result = weather_service.get_greeting_based_on_time()

        self.assertEqual(result, "Good morning")

    @patch("weather_service.api_client.get_current_hour")
    def test_greeting_afternoon(self, mock_hour):
        mock_hour.return_value = 15

        result = weather_service.get_greeting_based_on_time()

        self.assertEqual(result, "Good afternoon")


if __name__ == "__main__":
    unittest.main()