import requests

BASE_URL = "http://127.0.0.1:8080/v1/api"

# # --- Login to get JWT tokens ---
# login_data = {"username": "hanzala7788", "password": "hanzala@7788"}
# r = requests.post(f"{BASE_URL}/login/", json=login_data)
# print("Login:", r.status_code, r.json())

# tokens = r.json()
# access = tokens.get("access")
# refresh = tokens.get("refresh")
# print("Tokens:", access, refresh)
access = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzU2MzczNTE2LCJpYXQiOjE3NTYzNzM0NTYsImp0aSI6IjU2MGI2YmQ5MzUzMDQ3ZGFhZjhhYmQ4MjgyMzhlMWUwIiwidXNlcl9pZCI6IjcifQ.5sWLLseWixbZncGtiyfH-R3jXy2Y4TD10_XkUoAZY8k"

# # --- Refresh token (get a fresh access token) ---
# refresh_data = {"refresh": refresh}
# r = requests.post(f"{BASE_URL}/token/refresh/", json=refresh_data)
# print("Refresh:", r.status_code, r.json())

# # Use the NEW access token from refresh
# access = r.json().get("access")

# --- Get users list ---
headers = {"Authorization": f"Bearer {access}"}
r = requests.get(f"{BASE_URL}/users/", headers=headers)
print("Users:", r.status_code, r.json())
