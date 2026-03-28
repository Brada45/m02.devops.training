import unittest
import requests

BASE_URL = "http://127.0.0.1:5000"


class TestSecurity(unittest.TestCase):

    def test_missing_field_a(self):
        response = requests.post(f"{BASE_URL}/calculate", json={"b": 5})
        self.assertEqual(response.status_code, 400)

    def test_missing_field_b(self):
        response = requests.post(f"{BASE_URL}/calculate", json={"a": 5})
        self.assertEqual(response.status_code, 400)

    def test_invalid_data_type(self):
        response = requests.post(f"{BASE_URL}/calculate", json={"a": "abc", "b": 5})
        self.assertIn(response.status_code, [400, 422])  # zavisi od implementacije

    def test_empty_string_value(self):
        response = requests.post(f"{BASE_URL}/calculate", json={"a": "", "b": 5})
        self.assertEqual(response.status_code, 400)

    def test_very_large_number(self):
        large_number = 10**100  # veoma veliki broj
        response = requests.post(
            f"{BASE_URL}/calculate",
            json={"a": large_number, "b": large_number}
        )
        # bitno: ne smije crash (500)
        self.assertNotEqual(response.status_code, 500)

    def test_malformed_json(self):
        # šaljemo nevalidan JSON string
        response = requests.post(
            f"{BASE_URL}/calculate",
            data='{"a": 5, "b":}',  # neispravan JSON
            headers={"Content-Type": "application/json"}
        )
        self.assertEqual(response.status_code, 400)

    def test_division_by_zero_returns_safe_error(self):
        response = requests.post(
            f"{BASE_URL}/calculate",
            json={"a": 10, "b": 0, "operation": "divide"}
        )
        # ne smije biti 500
        self.assertNotEqual(response.status_code, 500)
        # očekujemo kontrolisanu grešku
        self.assertIn(response.status_code, [400, 422])


if __name__ == "__main__":
    unittest.main()