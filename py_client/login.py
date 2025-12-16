import requests

BASE_URL = "http://127.0.0.1:8080/v1/api"

# Register a new user
register_data = {
    "username": "hanzala",
    "email": "hanzala@gmail.com",
    "password": "password+123",
    "password2": "password+123",
}
r = requests.post(f"{BASE_URL}/register/", json=register_data)
print("Register:", r.status_code, r.json())

# Login to get JWT tokens
login_data = {"username": "hanzala", "password": "password+123"}
r = requests.post(f"{BASE_URL}/login/", json=login_data)
print("Login:", r.status_code, r.json())

tokens = r.json()
access = tokens.get("access")
refresh = tokens.get("refresh")
print("Tokens:", access, refresh)

# # Use access token for authenticated request (example: protected route)
# headers = {"Authorization": f"Bearer {access}"}
# r = requests.get(f"{BASE_URL}/users/", headers=headers)  # requires UserViewSet
# print("Users:", r.status_code, r.json())

# Refresh token
r = requests.post(f"{BASE_URL}/token/refresh/", json={"refresh": refresh})
print("Refresh:", r.status_code, r.json())
