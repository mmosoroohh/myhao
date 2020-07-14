from django.urls import path
from .views import (
    ListCreateProfile,
    ProfileDetailView
)

urlpatterns = [
    path('profile/', ListCreateProfile.as_view(), name="profile-list-create"),
    path('profile/<int:pk>/', ProfileDetailView.as_view(), name="profile-details"),
]