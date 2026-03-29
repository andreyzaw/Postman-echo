# tests/conftest.py
import pytest
import requests


# sample user
@pytest.fixture
def sample_user():
    return {"username": "admin", "email": "andreyzaw@gmail.com"}


# URL for GET requests
@pytest.fixture
def get_url():
    return "https://postman-echo.com/get"


# URL for POST requests
@pytest.fixture
def post_url():
    return "https://postman-echo.com/post"
