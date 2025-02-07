import requests
import allure
import pytest
from helpers import generate_password_name, generate_email, delete_user
from data import BASE_URL

class TestCreateUser:
    @allure.title("Создание пользователя")
    def test_create_user(self):
        payload = generate_password_name()
        payload["email"] = generate_email()

        response = requests.post(BASE_URL, json=payload)
        assert response.status_code == 200 and 'accessToken' in response.text

        response_delete = delete_user('accessToken')
        assert response_delete.status_code == 403

    @allure.title("Создание пользователя с уже существующим email")
    def test_create_duplicate_user(self):
        payload = generate_password_name()
        payload["email"] = generate_email()

        response_1 = requests.post(BASE_URL, json=payload)
        assert response_1.status_code == 200 and 'accessToken' in response_1.text

        response_2 = requests.post(BASE_URL, json=payload)
        assert response_2.status_code == 403 and response_2.json()['message'] == 'User already exists'

    @pytest.mark.parametrize("missing_field, expected_message", [
        ("password", "Недостаточно данных для создания учетной записи"),
        ("name", "Недостаточно данных для создания учетной записи"),
        ("email", "Недостаточно данных для создания учетной записи")
    ])
    @allure.title("Создание пользователя с отсутствующим обязательным полем")
    def test_create_user_missing_field(self, missing_field, expected_message):
        payload = generate_password_name()
        payload["email"] = generate_email()
        payload.pop(missing_field)
        response = requests.post(BASE_URL, json=payload)

        assert response.status_code == 403 and response.json()['message'] ==  'Email, password and name are required fields'

