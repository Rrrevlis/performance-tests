import time

from clients.http.gateway.users.client import (
    CreateUserRequestDict,
    build_users_gateway_http_client
)

# Инициализируем клиент UsersGatewayHTTPClient
users_gateway_client = build_users_gateway_http_client()

# Инициализируем запрос на создание пользователя
create_user_request = CreateUserRequestDict(
    email=f"user.{time.time()}@example.com",
    lastName="string",
    firstName="string",
    middleName="string",
    phoneNumber="string"
)
# Используем метод create_user
create_user_response = users_gateway_client.create_user()
print('Create user data:', create_user_response)

# Используем метод get_user
get_user_response = users_gateway_client.get_user(create_user_response['user']['id'])
print('Get user data:', get_user_response)
