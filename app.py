from flask import Flask, request, jsonify
import jwt
import datetime
import os
from functools import wraps
from flask import render_template


app = Flask(__name__)

# ======================
# ❌ Secret yếu (demo attack)
# ======================
WEAK_SECRET = "secret"

# ======================
# ✅ Secret mạnh (Cloud / Secure)
# Lấy từ environment variable
# ======================
STRONG_SECRET = os.environ.get(
    "JWT_SECRET",
    "DEV_FALLBACK_SECRET_DO_NOT_USE_IN_PROD"
)

# ======================
# LOGIN – tạo JWT (CỐ TÌNH YẾU)
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

        # ❌ Dùng secret yếu để demo bị forge
        token = jwt.encode(payload, WEAK_SECRET, algorithm="HS256")
        return jsonify({"token": token})

    return jsonify({"message": "Login failed"}), 401


# ======================
# ❌ VULNERABLE JWT CHECK
# Không verify chữ ký
# ======================
def vulnerable_jwt_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            return jsonify({"message": "Token missing"}), 401

        try:
            decoded = jwt.decode(
                token,
                options={"verify_signature": False}
            )
            request.user = decoded
        except Exception as e:
            return jsonify({"error": str(e)}), 401

        return f(*args, **kwargs)
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
# ✅ API ĐÃ FIX (VERIFY ĐẦY ĐỦ)
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


# ======================
# HEALTH CHECK (Render)
# ======================
@app.route("/healthz")
def healthz():
    return "OK", 200


@app.route("/")
def home():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
