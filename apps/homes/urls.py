from django.urls import path
from .views import (
    ListCreateHomeView,
    HomeDetailView
)

urlpatterns = [
    path('homes/', ListCreateHomeView.as_view(), name="homes-list-create"),
    path('homes/<int:pk>/', HomeDetailView.as_view(), name="homes-detail"),
]