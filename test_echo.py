import pytest
import requests
import allure


# Test 1: request GET without parameters
@allure.feature("GET запросы")
@allure.story("Базовые GET запросы")
@allure.title("GET запрос без параметров")
@allure.description("""
    Тест проверяет выполнение GET запроса без передачи параметров.
    Ожидается:
    - Статус код 200
    - В ответе содержится URL запроса
""")
@allure.severity(allure.severity_level.NORMAL)
def test_get_without_parameters(get_url):
    with allure.step("Выполнение GET запроса без параметров"):
        response = requests.get(get_url)

    with allure.step("Проверка статус кода"):
        assert response.status_code == 200

    with allure.step("Получение и проверка данных ответа"):
        response_data = response.json()
        allure.attach(str(response_data), "Response Data", allure.attachment_type.JSON)

    with allure.step("Проверка URL в ответе"):
        assert response_data['url'] == get_url


# Test 2: request GET with url post
@allure.feature("GET запросы")
@allure.story("Негативные сценарии")
@allure.title("GET запрос к эндпоинту POST (негативный сценарий)")
@allure.description("""
    Тест проверяет GET запрос к URL, предназначенному для POST запросов.
    Ожидается:
    - Статус код 404 (ресурс не найден)
""")
@allure.severity(allure.severity_level.MINOR)
def test_get_request_with_url_post(post_url):
    with allure.step(f"Выполнение GET запроса к {post_url}"):
        response = requests.get(post_url)

    with allure.step("Проверка статус кода 404"):
        assert response.status_code == 404

    allure.attach(f"Status Code: {response.status_code}", "Response Info", allure.attachment_type.TEXT)


# Test 3: request POST with JSON data
@allure.feature("POST запросы")
@allure.story("Отправка данных в JSON формате")
@allure.title("POST запрос с JSON данными")
@allure.description("""
    Тест проверяет отправку POST запроса с JSON данными.
    Ожидается:
    - Статус код 200
    - В ответе возвращаются переданные JSON данные
    - Content-Type заголовок установлен в application/json
""")
@allure.severity(allure.severity_level.CRITICAL)
def test_post_json_data(post_url, sample_user):
    with allure.step("Подготовка тестовых данных"):
        allure.attach(str(sample_user), "Request JSON Data", allure.attachment_type.JSON)

    with allure.step("Выполнение POST запроса с JSON данными"):
        response = requests.post(post_url, json=sample_user)

    with allure.step("Проверка статус кода"):
        assert response.status_code == 200

    with allure.step("Получение и проверка данных ответа"):
        response_data = response.json()
        allure.attach(str(response_data), "Response Data", allure.attachment_type.JSON)

    with allure.step("Проверка соответствия JSON данных"):
        assert response_data['json'] == sample_user
        assert response_data['data'] is not None
        assert response_data['headers']['content-type'] == 'application/json'


# Test 4: request POST with form-data
@allure.feature("POST запросы")
@allure.story("Отправка form-data")
@allure.title("POST запрос с form-data")
@allure.description("""
    Тест проверяет отправку POST запроса с form-data (x-www-form-urlencoded).
    Ожидается:
    - Статус код 200
    - В ответе возвращаются переданные form данные
""")
@allure.severity(allure.severity_level.NORMAL)
def test_post_form_data(post_url):
    form_data = {
        'username': 'testuser',
        'password': 'secret123',
        'remember': 'true'
    }

    with allure.step("Подготовка form-data"):
        allure.attach(str(form_data), "Form Data", allure.attachment_type.TEXT)

    with allure.step("Выполнение POST запроса с form-data"):
        response = requests.post(post_url, data=form_data)

    with allure.step("Проверка статус кода"):
        assert response.status_code == 200

    with allure.step("Получение и проверка данных ответа"):
        response_data = response.json()
        allure.attach(str(response_data), "Response Data", allure.attachment_type.JSON)

    with allure.step("Проверка form данных в ответе"):
        assert response_data['form'] == form_data
        assert 'username' in response_data['form']
        assert response_data['form']['password'] == 'secret123'


# Test 5: request POST with file
@allure.feature("POST запросы")
@allure.story("Загрузка файлов")
@allure.title("POST запрос с загрузкой файла")
@allure.description("""
    Тест проверяет отправку POST запроса с файлом.
    Ожидается:
    - Статус код 200
    - Файл успешно загружен и присутствует в ответе
    - Content-Type содержит multipart/form-data
""")
@allure.severity(allure.severity_level.NORMAL)
def test_post_with_file(post_url):
    test_file_content = "Hello, this is a test file!"
    files = {
        'file': ('test.txt', test_file_content, 'text/plain')
    }
    data = {
        'description': 'Test file upload'
    }

    with allure.step("Подготовка файла для загрузки"):
        allure.attach(test_file_content, "File Content", allure.attachment_type.TEXT)

    with allure.step("Выполнение POST запроса с файлом"):
        response = requests.post(post_url, files=files, data=data)

    with allure.step("Проверка статус кода"):
        assert response.status_code == 200

    with allure.step("Получение и проверка данных ответа"):
        response_data = response.json()
        allure.attach(str(response_data), "Response Data", allure.attachment_type.JSON)

    with allure.step("Проверка загруженного файла"):
        assert response_data['files']['test.txt'] is not None
        assert 'multipart/form-data' in response_data['headers']['content-type']


# Test 6: request POST with custom headers
@allure.feature("POST запросы")
@allure.story("Пользовательские заголовки")
@allure.title("POST запрос с кастомными заголовками")
@allure.description("""
    Тест проверяет отправку POST запроса с пользовательскими заголовками.
    Ожидается:
    - Статус код 200
    - Кастомные заголовки присутствуют в ответе сервера
""")
@allure.severity(allure.severity_level.NORMAL)
def test_post_with_custom_headers(post_url, sample_user):
    custom_headers = {
        'X-Custom-Header': 'MyCustomValue',
        'X-API-Key': 'abc123'
    }

    with allure.step("Подготовка кастомных заголовков"):
        allure.attach(str(custom_headers), "Custom Headers", allure.attachment_type.TEXT)

    with allure.step("Выполнение POST запроса с кастомными заголовками"):
        response = requests.post(
            post_url,
            json=sample_user,
            headers=custom_headers
        )

    with allure.step("Проверка статус кода"):
        assert response.status_code == 200

    with allure.step("Получение и проверка данных ответа"):
        response_data = response.json()
        allure.attach(str(response_data), "Response Data", allure.attachment_type.JSON)

    with allure.step("Проверка кастомных заголовков в ответе"):
        assert response_data['headers']['x-custom-header'] == 'MyCustomValue'
        assert response_data['headers']['x-api-key'] == 'abc123'