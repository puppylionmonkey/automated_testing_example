import requests

# 測試 GET：取得假用戶列表
BASE_URL = "https://jsonplaceholder.typicode.com"


def create_user_api(name: str, username: str, email: str):
    payload = {
        "name": name,
        "username": username,
        "email": email
    }
    response = requests.post(f"{BASE_URL}/users", json=payload)
    return response.json()


def create_post_api(title: str, body: str, user_id: int = 1):
    payload = {
        "title": title,
        "body": body,
        "userId": user_id
    }
    response = requests.post(f"{BASE_URL}/posts", json=payload)
    return response.json()


def get_users_api():
    response = requests.get(f"{BASE_URL}/users")
    assert response.status_code == 200, "GET /users 失敗"
    return response.json()
