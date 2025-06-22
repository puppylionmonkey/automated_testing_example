import requests

# 測試 GET：取得假用戶列表
BASE_URL = "https://jsonplaceholder.typicode.com"

def create_post_api(title: str, body: str, user_id: int = 1):
    payload = {
        "title": title,
        "body": body,
        "userId": user_id
    }
    response = requests.post(f"{BASE_URL}/posts", json=payload)
    return response.json()


response = requests.get("https://jsonplaceholder.typicode.com/users")
print("GET 狀態碼：", response.status_code)
print("用戶列表：", response.json()[:2])  # 顯示前兩筆

# 測試 POST：新增假貼文
payload = {
    "title": "測試標題",
    "body": "這是測試內容",
    "userId": 1
}
post_response = requests.post("https://jsonplaceholder.typicode.com/posts", json=payload)
print("POST 狀態碼：", post_response.status_code)
print("新增結果：", post_response.json())
