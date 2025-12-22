from flask import Flask, request, jsonify, render_template
import jwt
import datetime
import os
from functools import wraps

app = Flask(__name__)

# ======================
# CHỈ 1 SECRET DUY NHẤT
# ======================
JWT_SECRET = os.environ.get(
    "JWT_SECRET",
    "secret"  # mặc định yếu để demo local
)

# ======================
# LOGIN – tạo JWT bằng SECRET YẾU
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

        # ❌ Cố tình ký bằng secret yếu
        token = jwt.encode(payload, JWT_SECRET, algorithm="HS256")
        return jsonify({"token": token})

    return jsonify({"message": "Login failed"}), 401


# ======================
# JWT CHECK YẾU
# ======================
def weak_jwt_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            return jsonify({"message": "Token missing"}), 401

        try:
            decoded = jwt.decode(
                token,
                JWT_SECRET,           
                algorithms=["HS256"]
            )
            request.user = decoded
        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"message": "Invalid token"}), 401

        return f(*args, **kwargs)
    return wrapper


# ======================
# API CÓ LỖ HỔNG
# ======================
@app.route("/vuln/admin", methods=["GET"])
@weak_jwt_required
def vuln_admin():
    if request.user.get("role") != "admin":
        return jsonify({"message": "Access denied"}), 403

    return jsonify({
        "message": "VULNERABLE admin access granted",
        "data": request.user
    })


# ======================
# API ĐÃ FIX
# ======================
@app.route("/secure/admin", methods=["GET"])
def secure_admin():
    token = request.headers.get("Authorization")
    if not token:
        return jsonify({"message": "Token missing"}), 401

    try:
        decoded = jwt.decode(
            token,
            JWT_SECRET,
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
# HEALTH CHECK
# ======================
@app.route("/healthz")
def healthz():
    return "OK", 200

# ======================
# TRANG CHỦ
# ======================
@app.route("/")
def home():
    return render_template("index.html")

# ======================
# RUN APP
# ======================
if __name__ == "__main__":
    app.run(debug=True)
