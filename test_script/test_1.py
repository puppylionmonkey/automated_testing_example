import pytest
from functions.web_user_functions import WebUser

user = WebUser()


@pytest.fixture
def params():
    return {}


def test_google_search():
    user.driver.get('https://www.google.com')
