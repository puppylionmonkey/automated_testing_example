import pytest
import concurrent.futures
from functions.api_functions import *


@pytest.fixture
def params():
    return {}


def test_create_post_api():
    result = create_post_api("測試標題", "這是測試內容")
    assert result["title"] == "測試標題"
    assert result["body"] == "這是測試內容"


def test_create_user():
    result = create_user_api("測試用戶", "tester", "tester@example.com")  # 不會真的存進去
    assert result["name"] == "測試用戶"
    assert result["username"] == "tester"
    assert result["email"] == "tester@example.com"
    assert result["id"] == 11

    result = get_users_api()
    assert result[-1]["name"] == "Clementina DuBuque"
    assert result[-1]["username"] == "Moriah.Stanton"
    assert result[-1]["email"] == "Rey.Padberg@karina.biz"
    assert result[-1]["id"] == 10


def test_create_post_api_stress_testing():
    total_requests = 200  # 發送總次數，可依需求調高
    max_workers = 5  # 同時併發的執行緒數量

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_index = {
            executor.submit(
                create_post_api,
                f"title-{i}",
                f"body-{i}",
                1
            ): i for i in range(total_requests)
        }

        for future in concurrent.futures.as_completed(future_to_index):
            i = future_to_index[future]
            result = future.result(timeout=10)
            # print(result)
            assert result["title"] == f"title-{i}"
            assert result["body"] == f"body-{i}"
            assert result["userId"] == 1
            assert isinstance(result.get("id"), int)
