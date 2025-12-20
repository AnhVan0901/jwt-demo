from flask import Flask, request, jsonify
import jwt
import datetime
from functools import wraps

app = Flask(__name__)

# ======================
# ❌ Secret yếu (demo)
# ======================
WEAK_SECRET = "secret"

# ======================
# ✅ Secret mạnh (fix)
# ======================
STRONG_SECRET = "STRONG_SECRET_2025!@#"

# ======================
# LOGIN – tạo JWT
# ======================
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

        token = jwt.encode(payload, WEAK_SECRET, algorithm="HS256")
        return jsonify({"token": token})

    return jsonify({"message": "Login failed"}), 401


# ======================
# ❌ VULNERABLE JWT CHECK
# ======================
def vulnerable_jwt_required(f):
    @wraps(f)
    def wrapper():
        token = request.headers.get("Authorization")
        if not token:
            return jsonify({"message": "Token missing"}), 401

        try:
            # ❌ KHÔNG verify chữ ký
            decoded = jwt.decode(token, options={"verify_signature": False})
            request.user = decoded
        except Exception as e:
            return jsonify({"error": str(e)}), 401

        return f()
    return wrapper


# ======================
# 🔴 API CÓ LỖ HỔNG
# ======================
@app.route("/vuln/admin", methods=["GET"])
@vulnerable_jwt_required
def vuln_admin():
    if request.user.get("role") != "admin":
        return jsonify({"message": "Access denied"}), 403

    return jsonify({
        "message": "VULNERABLE admin access granted",
        "data": request.user
    })


# ======================
# ✅ API ĐÃ FIX
# ======================
@app.route("/secure/admin", methods=["GET"])
def secure_admin():
    token = request.headers.get("Authorization")
    if not token:
        return jsonify({"message": "Token missing"}), 401

    try:
        decoded = jwt.decode(
            token,
            STRONG_SECRET,
            algorithms=["HS256"]
        )

        if decoded.get("role") != "admin":
            return jsonify({"message": "Access denied"}), 403

        return jsonify({
            "message": "SECURE admin access granted",
            "data": decoded
        })

    except jwt.ExpiredSignatureError:
        return jsonify({"message": "Token expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"message": "Invalid token"}), 401


@app.route("/")
def home():
    return "JWT Security Demo API"


if __name__ == "__main__":
    app.run(debug=True)
