# tests/conftest.py
import pytest
import requests
import allure


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


# Настройка Allure environment properties
@pytest.fixture(scope="session", autouse=True)
def allure_environment(request):
    """Добавляет информацию об окружении в Allure отчёт"""
    import os
    environment_path = os.path.join(request.config.rootdir, "allure-results", "environment.properties")
    os.makedirs(os.path.dirname(environment_path), exist_ok=True)

    with open(environment_path, "w") as f:
        f.write(f"Base_URL=https://postman-echo.com\n")
        f.write(f"Python_Version={os.getenv('PYTHON_VERSION', '3.x')}\n")
        f.write(f"Test_Environment=Production\n")
