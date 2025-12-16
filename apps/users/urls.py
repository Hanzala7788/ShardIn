from django.urls import path
from .views import RegisterView, LoginView, UserAPIView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("users/", UserAPIView.as_view(), name="users_list"),
    path("users/me/", UserAPIView.as_view(), name="users_me"),
    path("users/<int:pk>/", UserAPIView.as_view(), name="users_filter"),
]
