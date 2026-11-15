import os
import requests
import hmac
import hashlib

from dotenv import load_dotenv
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


# 1. Load environment variables
load_dotenv()

API_KEY = os.getenv("API_KEY")
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET")

if not API_KEY or not WEBHOOK_SECRET:
    raise ValueError("Missing API_KEY or WEBHOOK_SECRET in .env")


# 2. Create requests Session with Retry
retry_strategy = Retry(
    total=3,
    backoff_factor=1,
    status_forcelist=[500, 502, 503, 504]
)

adapter = HTTPAdapter(max_retries=retry_strategy)

session = requests.Session()

session.mount("https://", adapter)
session.mount("http://", adapter)


# 3. GET users API
url = "https://jsonplaceholder.typicode.com/users"

response = session.get(url, timeout=10)

response.raise_for_status()

users = response.json()


# 4. Print first 5 users
print("First 5 Users:")

for user in users[:5]:
    print(
        "ID:", user.get("id", "Not Available"),
        "| Name:", user.get("name", "Not Available"),
        "| Email:", user.get("email", "Not Available")
    )


# 5. Print first user's nested information
if users:
    first_user = users[0]

    address = first_user.get("address") or {}
    geo = address.get("geo") or {}
    company = first_user.get("company") or {}

    print("\nFirst User Details:")

    print("City:", address.get("city") or "Not Available")
    print("Latitude:", geo.get("lat") or "Not Available")
    print("Zip:", address.get("zipcode") or "Not Available")
    print("Company:", company.get("name") or "Not Available")


# 6. HMAC-SHA256 signature verification
def verify_signature(payload, signature, secret):

    expected_signature = hmac.new(
        secret.encode("utf-8"),
        payload,
        hashlib.sha256
    ).hexdigest()

    return hmac.compare_digest(
        expected_signature,
        signature
    )


# 7. Test signature verification
payload = b'{"event":"payment_success","amount":1000}'

secret = WEBHOOK_SECRET

# Generate valid signature
valid_signature = hmac.new(
    secret.encode("utf-8"),
    payload,
    hashlib.sha256
).hexdigest()

# Tampered signature
tampered_signature = valid_signature[:-1] + (
    "0" if valid_signature[-1] != "0" else "1"
)

# Wrong secret
wrong_secret = "wrong_secret"

wrong_secret_signature = hmac.new(
    wrong_secret.encode("utf-8"),
    payload,
    hashlib.sha256
).hexdigest()


print("\nSignature Verification:")

print(
    "Valid Signature:",
    verify_signature(payload, valid_signature, secret)
)

print(
    "Tampered Signature:",
    verify_signature(payload, tampered_signature, secret)
)

print(
    "Wrong Secret:",
    verify_signature(payload, wrong_secret_signature, secret)
)
