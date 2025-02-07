import requests
import allure
import pytest
from helpers import generate_password_name, generate_email, login_user, update_user, create_user
from data import BASE_URL

class TestUpdateUser:

    @pytest.mark.parametrize("field, new_value", [
        ('name', 'new_name_test'),
        ('email', generate_email()),
        ('password', 'new_password_123')
    ])
    @allure.title("Обновление данных пользователя без авторизации")
    def test_update_user_without_authorization(self, field, new_value):
        create_response = create_user()
        assert create_response.status_code == 200

        empty_access_token = ''
        update_response = update_user(empty_access_token, field, new_value)

        assert update_response.status_code == 401 and update_response.json()['message'] == "You should be authorised"

    @pytest.mark.parametrize("field, new_value", [
        ('name', 'new_name_test'),
        ('email', generate_email()),
        ('password', 'new_password_123')
    ])
    @allure.title("Обновление данных пользователя с авторизацией")
    def test_update_user_with_authorization(self, field, new_value):

        user_data = generate_password_name()
        user_data["email"] = generate_email()
        user_data["password"] = user_data["password"]
        response_create = requests.post(BASE_URL, json=user_data)
        assert response_create.status_code == 200

        login_response = login_user(user_data["email"], user_data["password"])
        assert login_response.status_code == 200, f"Ошибка логина: {login_response.json()}"

        access_token = login_response.json()['accessToken']
        update_response = update_user(access_token, field, new_value)
        assert update_response.status_code == 200, f"Ошибка обновления: {update_response.json()}"
