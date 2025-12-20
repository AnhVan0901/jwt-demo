import jwt
import time

WEAK_SECRET = "secret"

payload = {
    "user": "user",
    "role": "admin",
    "exp": int(time.time()) + 1800
}

token = jwt.encode(payload, WEAK_SECRET, algorithm="HS256")
print(token)
