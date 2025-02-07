import requests
import allure
from helpers import generate_password_name, generate_email, login_user, get_orders
from data import BASE_URL

class TestUsersOrders:

    @allure.title("Получение заказов пользователя без авторизации")
    def test_get_users_orders_with_no_login(self):
        response_get_orders = get_orders(access_token=None)
        assert response_get_orders.status_code == 401 and response_get_orders.json()['message'] == "You should be authorised"

    @allure.title("Получение заказов пользователя с авторизацией")
    def test_get_users_orders(self):
        user_data = generate_password_name()
        user_data["email"] = generate_email()

        response_create = requests.post(BASE_URL, json=user_data)
        assert response_create.status_code == 200

        response_login = login_user(user_data["email"], user_data["password"])
        assert response_login.status_code == 200
        access_token = response_login.json().get("accessToken", "")

        response_get_orders = get_orders(access_token)
        assert response_get_orders.status_code == 200




