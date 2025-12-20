# 🔐 JWT Security Demo – Flask API

Demo **tạo API đơn giản bằng Flask + PyJWT**, xác thực bằng JWT và **mô phỏng các lỗ hổng bảo mật JWT phổ biến**:
- Secret key yếu
- Không verify chữ ký JWT
- So sánh API **Vulnerable vs Secure**

---

## 🎯 Mục tiêu đề tài
- Hiểu cách JWT hoạt động trong REST API
- Xây dựng API có xác thực JWT
- Demo lỗ hổng JWT khi cấu hình sai
- So sánh cách làm **không an toàn** và **đúng chuẩn**

---

## 🧱 Công nghệ sử dụng
- Python 3.9+
- Flask
- PyJWT
- JWT (HS256)

---

## 📁 Project Structure

jwt-demo/
├── app.py
├── requirements.txt
├── README.md
├── templates/
│   └── index.html
├── static/
│   └── assets/
│       ├── css/
│       │   └── style.css
│       ├── js/
│       │   └── main.js
│       └── img/
│           └── logo.png

# JWT Demo – Flask + PyJWT

Demo API Flask sử dụng JWT để xác thực và mô phỏng lỗ hổng JWT không an toàn (secret yếu, không verify chữ ký).

## Yêu cầu
- Python 3.9+

## Cài đặt
git clone https://github.com/AnhVan0901/jwt-demo.git
cd jwt-demo
python -m venv venv

Windows:
venv\Scripts\activate

Linux / macOS:
source venv/bin/activate

pip install flask PyJWT

## Cấu hình JWT Secret (khuyến nghị)
Windows (PowerShell):
setx JWT_SECRET "THIS_IS_A_STRONG_SECRET_KEY_123456"

Linux / macOS:
export JWT_SECRET="THIS_IS_A_STRONG_SECRET_KEY_123456"

## Chạy ứng dụng
python app.py

Mở trình duyệt:
http://127.0.0.1:5000

## API chính
POST /login
Body:
{"username":"user","password":"123456"}

GET /vuln/admin
Header:
Authorization: <JWT_TOKEN>

GET /secure/admin
Header:
Authorization: <JWT_TOKEN>

## Lưu ý
Project chỉ dùng cho học tập & demo bảo mật, không dùng cho production.
