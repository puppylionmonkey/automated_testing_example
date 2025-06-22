import pytest

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
