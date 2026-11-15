import os
import json
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Read API key
API_KEY = os.getenv("API_KEY")

print("API Key:", API_KEY)


# 1. Call API with custom header
print("\n--- API Headers ---")

try:
    response = requests.get(
        "https://httpbin.org/headers",
        headers={"X-API-Key": API_KEY},
        timeout=5
    )

    response.raise_for_status()

    data = response.json()
    received_key = data.get("headers", {}).get("X-Api-Key")

    print("Key received by server:", received_key)

except requests.exceptions.Timeout:
    print("Request timed out. Please try again.")

except requests.exceptions.ConnectionError:
    print("Connection failed. Check your internet.")

except requests.exceptions.HTTPError as e:
    print("HTTP Error:", e)


# 2. Test timeout using delay endpoint
print("\n--- Timeout Test ---")

try:
    response = requests.get(
        "https://httpbin.org/delay/10",
        timeout=3
    )

    response.raise_for_status()
    print(response.json())

except requests.exceptions.Timeout:
    print("Friendly message: Server took too long. Please try again later.")

except requests.exceptions.ConnectionError:
    print("Connection failed. Check your internet.")


# 3. Handle HTTP 500 error
print("\n--- HTTP Error Test ---")

try:
    response = requests.get(
        "https://httpbin.org/status/500",
        timeout=5
    )

    response.raise_for_status()

except requests.exceptions.HTTPError as e:
    print("HTTP Error caught:", e)

except requests.exceptions.Timeout:
    print("Request timed out.")

except requests.exceptions.ConnectionError:
    print("Connection failed.")


# 4. Parse nested JSON response
print("\n--- Nested JSON ---")

try:
    response = requests.get(
        "https://httpbin.org/json",
        timeout=5
    )

    response.raise_for_status()

    data = response.json()

    # Access nested JSON using get()
    slideshow = data.get("slideshow", {})
    title = slideshow.get("title")
    author = slideshow.get("author")

    result = {
        "title": title,
        "author": author
    }

    print("Parsed result:", result)

    # Save result into result.json
    with open("result.json", "w") as file:
        json.dump(result, file, indent=4)

    print("JSON saved successfully!")

except requests.exceptions.Timeout:
    print("Request timed out.")

except requests.exceptions.ConnectionError:
    print("Connection failed.")

except requests.exceptions.HTTPError as e:
    print("HTTP Error:", e)