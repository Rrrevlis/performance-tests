import time

import httpx

create_user_payload = {
    "email": f"user.{time.time()}@example.com",
    "lastName": "string",
    "firstName": "string",
    "middleName": "string",
    "phoneNumber": "string"
}

create_user_response = httpx.post("http://localhost:8003/api/v1/users", json=create_user_payload)
create_user_response_data = create_user_response.json()

print("Create user response:", create_user_response_data)
print("Status Code:", create_user_response.status_code)

open_deposit_account_payload = {
    "userId": f"{create_user_response_data['user']['id']}"
}

open_deposit_account_response = httpx.post("http://localhost:8003/api/v1/accounts/open-deposit-account", json=open_deposit_account_payload)
open_deposit_account_response_data = open_deposit_account_response.json()

print("Open deposit account user response:", open_deposit_account_response_data)
print("Status Code:", open_deposit_account_response.status_code)
