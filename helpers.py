import random
import requests
import string
import allure
from data import BASE_URL, DELETE_URL, LOGOUT_URL, LOGIN_URL, INGREDIENTS_LIST, ORDER_URL

@allure.title("Генерация случайного пароля и имени пользователя")
def generate_password_name():
    def generate_random_string(length):
        return ''.join(random.choice(string.ascii_lowercase) for _ in range(length))
    password = generate_random_string(11)
    name = generate_random_string(11)
    return {
        "password": password,
        "name": name
    }

@allure.title("Генерация случайного email адреса")
def generate_email():
    login = ''
    for _ in range(3):
        login += random.choice('qwertyuiopasdfghjklzxcvbnm1234567890')
    domain = random.choice(['yandex.ru', 'gmail.com'])
    email = f'{login}@{domain}'
    return email

@allure.step("Удаление пользователя по access token")
def delete_user(access_token):
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.delete(DELETE_URL, headers=headers)
    return response

@allure.step("Создание нового пользователя")
def create_user():
        payload = generate_password_name()
        payload["email"] = generate_email()

        response = requests.post(BASE_URL, json=payload)
        return response

@allure.step("Выход пользователя из системы")
def logout(refresh_token):
    payload = {
        "token": refresh_token
    }
    response = requests.post(LOGOUT_URL, json=payload)
    return response

@allure.step("Авторизация пользователя")
def login_user(email, password):
    payload = {
        "email": email,
        "password": password
    }
    response = requests.post(LOGIN_URL, json=payload)
    return response

@allure.step("Обновление данных пользователя")
def update_user(access_token, field_to_change, new_value):
    # Проверяем, если в access_token уже есть слово "Bearer", то не добавляем его повторно
    if "Bearer" not in access_token:
        access_token = f"Bearer {access_token}"

    headers = {
        'Authorization': access_token
    }

    update_payload = {field_to_change: new_value}
    response = requests.patch(DELETE_URL, json=update_payload, headers=headers)

    return response

@allure.step("Получение списка ингредиентов")
def get_ingredients():
    return INGREDIENTS_LIST[:2]

@allure.step("Создание заказа с возможной авторизацией")
def create_order(ingredients, access_token=None):
    headers = {}
    if access_token and not access_token.startswith("Bearer "):
        access_token = f"Bearer {access_token}"

    headers = {
        'Authorization': access_token
    }

    payload = {
        "ingredients": ingredients
    }

    response = requests.post(ORDER_URL, json=payload, headers=headers)
    return response

@allure.step("Получение списка заказов пользователя")
def get_orders(access_token=None):
    if access_token and access_token.startswith("Bearer "):
        access_token = access_token[len("Bearer "):]

    headers = {"Authorization": f"Bearer {access_token}"} if access_token else {}
    response = requests.get(ORDER_URL, headers=headers)
    return response




