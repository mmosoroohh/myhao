from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response 
from rest_framework.views import status
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly, IsAuthenticated, IsAdminUser
)

from .models import Book
from .serializers import BookSerializer, Homes
from ..userprofile.helper.permissions import IsOwnerOrReadOnly



class ListCreateBookView(generics.ListAPIView):
    """Book a home"""
    permission_classes = [IsAuthenticatedOrReadOnly,]
    serializer_class = BookSerializer
    queryset = Book.objects.all()

    def post(self, request, *args, **kwargs):
        """" create a book"""
        home = Homes.objects.get(pk=kwargs["pk"])
        serializer = BookSerializer(
            data={"home": home, "amount": request.data.get('amount')}
        )
        if serializer.is_valid():
            data = serializer.save(
                amount=request.data.get('amount'),
                user=request.user,
                home=home
            )
            return Response(message, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'invalid data'}, status=status.HTTP_400_BAD_REQUEST)


class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    
    permission_classes = [IsOwnerOrReadOnly, IsAuthenticated]
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get(self, request, *args, **kwargs):
        try:
            book = self.queryset.get(pk=kwargs["pk"])
            return Response(BookSerializer(book).data)
        except Book.DoesNotExist:
            return Response(
                data={
                    "message" : "Book with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )
    
    def put(self,request, *args, **kwargs):
        try:
            book = self.queryset.get(pk=kwargs["pk"])
            serializer = BookSerializer()
            update_book = serializer.update(book, request.data)
            return Response(BookSerializer(update_book).data)
        except Book.DoesNotExist:
            return Response(
                data={
                    "message": "Book with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )

    def delete(self, request, *args, **kwargs):
        try:
            book = self.queryset.get(pk=kwargs["pk"])
            book.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Book.DoesNotExist:
            return Response(
                data={
                    "message": "Book with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )
            