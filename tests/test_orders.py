import requests
import allure
from helpers import generate_password_name, generate_email, get_ingredients, create_order, login_user
from data import BASE_URL

class TestOrders:
    @allure.title("Создание заказа зарегистрированным пользователем")
    def test_create_order(self):
        user_data = generate_password_name()
        user_data["email"] = generate_email()

        response_create = requests.post(BASE_URL, json=user_data)
        assert response_create.status_code == 200

        response_login = login_user(user_data["email"], user_data["password"])
        assert response_login.status_code == 200
        access_token = response_login.json().get("accessToken", "")

        ingredients = get_ingredients()
        response_create_order = create_order(ingredients, access_token)
        assert response_create_order.status_code == 200 and response_create_order.json()["success"] == True

    @allure.title("Создание заказа неавторизованным пользователем")
    def test_create_order_user_not_aut(self):
        ingredients = get_ingredients()

        response_create_order = create_order(ingredients)
        assert response_create_order.status_code == 200 and response_create_order.json()["success"] == True

    @allure.title("Создание заказа с ошибочным ингредиентом")
    def test_create_order_with_mistake_ingredient(self):
        ingredient = ["61c0c5a71d1f82001mistak6d"]

        response_create_order = create_order(ingredient)
        assert response_create_order.status_code == 500

    @allure.title("Создание заказа без ингредиентов")
    def test_create_order_with_no_ingredient(self):
        ingredient = []
        response_create_order = create_order(ingredient)
        assert response_create_order.status_code == 400 and response_create_order.json()['message'] =="Ingredient ids must be provided"

