import requests
import allure
import pytest
from helpers import generate_password_name, generate_email, login_user
from data import BASE_URL

class TestLoginUser:
    @allure.title("Успешная авторизация пользователя")
    def test_login_user(self):
        user_data = generate_password_name()
        user_data["email"] = generate_email()
        response_create = requests.post(BASE_URL, json=user_data)
        assert response_create.status_code == 200

        response_login = login_user(user_data["email"], user_data["password"])
        assert response_login.status_code == 200

    @pytest.mark.parametrize("field_to_change, wrong_value, expected_message", [
        ("email", "wrongEmail", "Учетная запись не найдена"),
        ("password", "wrongPassword", "Учетная запись не найдена")
    ])
    @allure.title("Ошибка авторизации при неверных учетных данных")
    def test_invalid_login_or_password(self, field_to_change, wrong_value, expected_message):
        base_payload = {
            "email": "testqa@yandex.ru",
            "password": "111111"
        }
        payload = base_payload.copy()
        payload[field_to_change] = wrong_value

        login_response = login_user(payload["email"], payload["password"])
        assert login_response.status_code == 401 and login_response.json()['message'] == 'email or password are incorrect'






