from flask import Flask, jsonify, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import re

app = Flask(__name__)

history = []

# ------------------ RATE LIMITING ------------------

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["100 per second"]
)

#if os.getenv("DISABLE_RATE_LIMIT"):
#    limiter.enabled = False

@app.errorhandler(429)
def ratelimit_handler(e):
    return jsonify({"error": "Too many requests"}), 429


# ------------------ HELPERS ------------------

def parse_json():
    """Safely parse JSON"""
    try:
        data = request.get_json(force=True)
        if not isinstance(data, dict):
            return None, ("Invalid JSON format", 400)
        return data, None
    except Exception:
        return None, ("Malformed JSON", 400)


def sanitize_number(value):
    """Sanitize and validate numeric input"""
    if isinstance(value, (int, float)):
        return value

    if isinstance(value, str):
        # Detect suspicious patterns
        if re.search(r"[;\'\"--]|<script>", value, re.IGNORECASE):
            raise ValueError("Potential injection detected")

        try:
            return float(value)
        except ValueError:
            raise ValueError("Invalid numeric value")

    raise ValueError("Unsupported type")


def validate_input(data):
    """Validate required fields and sanitize values"""
    if "a" not in data or "b" not in data:
        return None, "Missing required fields"

    try:
        a = sanitize_number(data["a"])
        b = sanitize_number(data["b"])
    except ValueError as e:
        return None, str(e)

    # Reject empty values explicitly
    if a == "" or b == "":
        return None, "Empty values not allowed"

    return (a, b), None


def safe_response(result, operation, a, b):
    """Store history safely"""
    history.append({
        "operation": operation,
        "a": a,
        "b": b,
        "result": result
    })
    return jsonify({"result": result})


# ------------------ ROUTES ------------------

@app.route("/")
def home():
    return "Welcome to the Secure Flask App!"


@app.route("/health")
def health():
    return jsonify({"status": "ok"})


@app.route("/add", methods=["POST"])
@limiter.limit("100 per second")
def add():
    data, error = parse_json()
    if error:
        return jsonify({"error": error[0]}), error[1]

    values, validation_error = validate_input(data)
    if validation_error:
        return jsonify({"error": validation_error}), 400

    a, b = values
    return safe_response(a + b, "add", a, b)


@app.route("/subtract", methods=["POST"])
@limiter.limit("100 per second")
def subtract():
    data, error = parse_json()
    if error:
        return jsonify({"error": error[0]}), error[1]

    values, validation_error = validate_input(data)
    if validation_error:
        return jsonify({"error": validation_error}), 400

    a, b = values
    return safe_response(a - b, "subtract", a, b)


@app.route("/multiply", methods=["POST"])
@limiter.limit("100 per second")
def multiply():
    data, error = parse_json()
    if error:
        return jsonify({"error": error[0]}), error[1]

    values, validation_error = validate_input(data)
    if validation_error:
        return jsonify({"error": validation_error}), 400

    a, b = values
    return safe_response(a * b, "multiply", a, b)


@app.route("/divide", methods=["POST"])
@limiter.limit("100 per second")
def divide():
    data, error = parse_json()
    if error:
        return jsonify({"error": error[0]}), error[1]

    values, validation_error = validate_input(data)
    if validation_error:
        return jsonify({"error": validation_error}), 400

    a, b = values

    if b == 0:
        return jsonify({"error": "Division by zero"}), 400

    return safe_response(a / b, "divide", a, b)


@app.route("/history", methods=["GET"])
@limiter.limit("100 per second")
def get_history():
    return jsonify(history)


# ------------------ SECURITY HEADERS ------------------

@app.after_request
def add_security_headers(response):
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    return response


# ------------------ MAIN ------------------

if __name__ == "__main__":
    #app.run(debug=True)
    app.run(host="0.0.0.0", port=5000, debug=False, use_reloader=False)
