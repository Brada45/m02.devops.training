import unittest
import requests

BASE_URL = "http://127.0.0.1:5000"


class TestSecurity(unittest.TestCase):

    def test_missing_field_a(self):
        response = requests.post(f"{BASE_URL}/add", json={"b": 5})
        self.assertEqual(response.status_code, 400)

    def test_missing_field_b(self):
        response = requests.post(f"{BASE_URL}/add", json={"a": 5})
        self.assertEqual(response.status_code, 400)

    def test_invalid_data_type(self):
        response = requests.post(f"{BASE_URL}/add", json={"a": "abc", "b": 5})
        self.assertEqual(response.status_code, 400)

    def test_empty_string_value(self):
        response = requests.post(f"{BASE_URL}/add", json={"a": "", "b": 5})
        self.assertEqual(response.status_code, 400)

    def test_very_large_number(self):
        large_number = 10**100
        response = requests.post(
            f"{BASE_URL}/add",
            json={"a": large_number, "b": large_number}
        )
        self.assertNotEqual(response.status_code, 500)

    def test_malformed_json(self):
        response = requests.post(
            f"{BASE_URL}/add",
            data='{"a": 5, "b":}',
            headers={"Content-Type": "application/json"}
        )
        self.assertEqual(response.status_code, 400)

    def test_division_by_zero_returns_safe_error(self):
        response = requests.post(
            f"{BASE_URL}/divide",
            json={"a": 10, "b": 0}
        )
        self.assertEqual(response.status_code, 400)


if __name__ == "__main__":
    unittest.main()