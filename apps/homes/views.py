from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response 
from rest_framework.views import status
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly, IsAuthenticated, IsAdminUser
)

from .models import Homes
from .serializers import HomeSerializer
from ..userprofile.helper.permissions import IsOwnerOrReadOnly


def get_home(name):
    """
    Get a home from the provided name
    """
    try:
        home = Homes.objects.get(name=name)
        return home
    except Homes.DoesNotExist:
        return Response(
            data={
                "message": "Home with this name: {} does not exist"
            },
            status=status.HTTP_404_NOT_FOUND
        )


class ListCreateHomeView(generics.ListAPIView):
    """
    Provides a GET and POST handler
    """
    permission_classes = [IsAuthenticatedOrReadOnly,]
    queryset = Homes.objects.all()
    serializer_class = HomeSerializer

    def post(self, request, *args, **kwargs):
        user = request.user
        home = Homes.objects.create(
            name=request.data["name"],
            location=request.data["location"],
            size=request.data["size"],
            price=request.data["price"],
            status=request.data["status"],
            user= request.user
        )

        return Response(
            data=HomeSerializer(home).data,
            status=status.HTTP_201_CREATED
        )


class HomeDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Provides:
        GET homes/:id/
        PUT homes/:id/
        DELETE homes/:id/
    """
    permission_class = [IsOwnerOrReadOnly, IsAuthenticated]
    queryset = Homes.objects.all()
    serializer_class = HomeSerializer

    def get(self, request, *args, **kwargs):
        try:
            home=self.queryset.get(pk=kwargs["pk"])
            return Response(HomeSerializer(home).data)
        except Homes.DoesNotExist:
            return Response(
                data={
                    "message": "Home with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )

    def put(self, request, *args, **kwargs):
        try:
            home=self.queryset.get(pk=kwargs["pk"])
            serializer = HomeSerializer()
            update_home=serializer.update(home, request.data)
            return Response(HomeSerializer(update_home).data)
        except Homes.DoesNotExist:
            return Response(
                data={
                    "message": "Home with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )

    def delete(self, request, *args, **kwargs):
        try:
            home=self.queryset.get(pk=kwargs["pk"])
            home.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Homes.DoesNotExist:
            return Response(
                data={
                    "message": "Home with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )
