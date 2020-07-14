from django.urls import path
from .views import (
    ListCreateBookView,
    BookDetailView
)

urlpatterns = [
    path('homes/<int:pk>/books', ListCreateBookView.as_view(), name="books-list-create"),
    path('books/<int:pk>/', BookDetailView.as_view(), name="book-detail"),
]
