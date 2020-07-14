from django.urls import path
from .views import (
    SignUpAPIView,
    SignInAPIView
)

urlpatterns = [
    path('users/', SignUpAPIView.as_view(), name="register"),
    path('users/login/', SignInAPIView.as_view(), name="login"),
]