import pytest
import requests


# Test 1: request GET without parameters
def test_get_without_parameters(get_url):
    response = requests.get(get_url)

    # Checks
    assert response.status_code == 200
    response_data = response.json()

    # We check that the data was returned in the response.
    assert response_data['url'] == get_url


# Test 2: request GET with url post
def test_get_request_with_url_post(post_url):
    response = requests.get(post_url)

    # Checks
    assert response.status_code == 200


# Test 3: request POST  with JSON data
def test_post_json_data(post_url, sample_user):
    response = requests.post(post_url, json=sample_user)

    # Checks
    assert response.status_code == 200
    response_data = response.json()

    # We check that the data was returned in the response.
    assert response_data['json'] == sample_user
    assert response_data['data'] is not None
    assert response_data['headers']['content-type'] == 'application/json'


# Test 4: request POST  with form-data
def test_post_form_data(post_url):
    form_data = {
        'username': 'testuser',
        'password': 'secret123',
        'remember': 'true'
    }

    response = requests.post(post_url, data=form_data)

    # Checks
    assert response.status_code == 200
    response_data = response.json()

    # We check that the data was returned in the response.
    assert response_data['form'] == form_data
    assert 'username' in response_data['form']
    assert response_data['form']['password'] == 'secret123'


# Test 5: request POST  with file
def test_post_with_file(post_url):
    test_file_content = "Hello, this is a test file!"
    files = {
        'file': ('test.txt', test_file_content, 'text/plain')
    }

    data = {
        'description': 'Test file upload'
    }

    response = requests.post(post_url, files=files, data=data)

    # Checks
    assert response.status_code == 200
    response_data = response.json()

    # We check that the data was returned in the response.
    assert response_data['files']['test.txt'] is not None
    assert 'multipart/form-data' in response_data['headers']['content-type']


# Test 6 request POST  with custom headers
def test_post_with_custom_headers(post_url, sample_user):
    custom_headers = {
        'X-Custom-Header': 'MyCustomValue',
        'X-API-Key': 'abc123'
    }

    response = requests.post(
        post_url,
        json=sample_user,
        headers=custom_headers
    )

    # Checks
    assert response.status_code == 200
    response_data = response.json()

    # We check that the data was returned in the response.
    assert response_data['headers']['x-custom-header'] == 'MyCustomValue'
    assert response_data['headers']['x-api-key'] == 'abc123'
