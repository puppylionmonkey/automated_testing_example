import pytest

from functions.api_functions import create_post_api


@pytest.fixture
def params():
    return {}


def test_create_post_api():
    result = create_post_api("測試標題", "這是測試內容")
    assert result["title"] == "測試標題"
    assert result["body"] == "這是測試內容"
