from flask import Flask, request, jsonify
import jwt
import datetime

app = Flask(__name__)

# ❌ SECRET KEY YẾU (cố tình)
SECRET_KEY = "secret"

@app.route("/login", methods=["POST"])
def login():
    data = request.json

    # Giả lập user
    if data["username"] == "user" and data["password"] == "123456":
        payload = {
            "user": data["username"],
            "role": "user",
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=10)
        }

        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
        return jsonify({"token": token})

    return jsonify({"message": "Login failed"}), 401


@app.route("/protected", methods=["GET"])
def protected():
    token = request.headers.get("Authorization")

    if not token:
        return jsonify({"message": "Token missing"}), 401

    try:
        # ❌ KHÔNG KIỂM SOÁT ALGORITHM
        decoded = jwt.decode(token, SECRET_KEY, options={"verify_signature": False})
        return jsonify({
            "message": "Access granted",
            "data": decoded
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 401


if __name__ == "__main__":
    app.run(debug=True)
