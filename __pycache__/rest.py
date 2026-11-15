import requests

BASE_URL = "https://jsonplaceholder.typicode.com"


# Function to explain HTTP status codes
def explain_status(code):
    messages = {
        200: "OK - Request successful",
        201: "Created - Resource created successfully",
        400: "Bad Request",
        401: "Unauthorized",
        404: "Not found",
        500: "Internal Server Error"
    }

    return messages.get(code, "Unknown status code")


# 1. GET - First 5 users
response = requests.get(f"{BASE_URL}/users")

users = response.json()

for user in users[:5]:
    print(f"{user['id']} - {user['name']} - {user['email']}")


# 2. POST - Create a new post
new_post = {
    "title": "Python Learning",
    "body": "Learning REST API using requests",
    "userId": 1
}

response = requests.post(
    f"{BASE_URL}/posts",
    json=new_post
)

created_post = response.json()

print(f"POST: {response.status_code}, id: {created_post['id']}")


# 3. PUT - Update entire post
put_data = {
    "id": 1,
    "title": "Updated Title",
    "body": "Updated Body",
    "userId": 1
}

put_response = requests.put(
    f"{BASE_URL}/posts/1",
    json=put_data
)


# 4. PATCH - Update part of post
patch_data = {
    "title": "Patched Title"
}

patch_response = requests.patch(
    f"{BASE_URL}/posts/1",
    json=patch_data
)


# 5. DELETE - Delete post
delete_response = requests.delete(
    f"{BASE_URL}/posts/1"
)

print(
    f"PUT: {put_response.status_code} | "
    f"PATCH: {patch_response.status_code} | "
    f"DELETE: {delete_response.status_code}"
)


# 6. GET - Non-existing post
response = requests.get(f"{BASE_URL}/posts/9999")

print(
    f"GET /posts/9999 -> "
    f"{response.status_code} {explain_status(response.status_code).split(' - ')[0]}"
)
