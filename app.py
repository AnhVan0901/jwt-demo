from flask import Flask, request, jsonify
import jwt
import datetime

app = Flask(__name__)

# ❌ Secret yếu (cố tình)
SECRET_KEY = "secret"

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"message": "JSON required"}), 400

    if data.get("username") == "user" and data.get("password") == "123456":
        payload = {
            "user": "user",
            "role": "user",
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
        return jsonify({"token": token})

    return jsonify({"message": "Login failed"}), 401



SECRET_KEY = "STRONG_SECRET_2025!@#"

@app.route("/protected", methods=["GET"])
def protected():
    token = request.headers.get("Authorization")
    if not token:
        return jsonify({"message": "Token missing"}), 401

    try:
        decoded = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=["HS256"]  # ✅ bắt buộc thuật toán
        )
        return jsonify({"message": "Secure access granted", "data": decoded})

    except jwt.ExpiredSignatureError:
        return jsonify({"message": "Token expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"message": "Invalid token"}), 401


if __name__ == "__main__":
    app.run(debug=True)