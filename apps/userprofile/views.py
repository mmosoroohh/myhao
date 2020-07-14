from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import status
from rest_framework.response import Response
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly, IsAuthenticated, IsAdminUser
)

from .models import Profile
from .serializers import ProfileSerializer
from .helper.permissions import IsOwnerOrReadOnly



class ListCreateProfile(generics.ListAPIView):
    """
    Provides a GET and POST method hadler
    """
    permission_classes = [IsAuthenticated,]
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def post(self, request, *args, **kwargs):
        user = request.user
        image = None
        if request.data.get('image_file'):
            image = uploader(request.data.get('image_file'))
            image = image.get('secure_url')
            del request.data['image_file']
        else:
            profile = Profile.objects.create(
                personal_identification = request.data["personal_identification"],
                birth_date = request.data["birth_date"],
                bio = request.data["bio"],
                phone_number = request.data["phone_number"],
                category= request.data["category"],
                user=request.user
            )
        return Response(
            data=ProfileSerializer(profile).data,
            status=status.HTTP_201_CREATED
        )


class ProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Provides:
    GET profile/:id/
    PUT profile/:id/
    DELETE profile/:id/
    """
    permission_class = [IsOwnerOrReadOnly, IsAuthenticated]
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def get(self, request, *args, **kwargs):
        try:
            profile = self.queryset.get(pk=kwargs["pk"])
            return Response(ProfileSerializer(profile).data)
        except Profile.DoesNotExist:
            return Response(
                data={
                "message": "Profile with id {} does not exist".format(kwargs["pk"])
            },
            status=status.HTTP_404_NOT_FOUND
            )
    
    def put(self, request, *args, **kwargs):
        try:
            profile = self.queryset.get(pk=kwargs["pk"])
            serializer = ProfileSerializer()
            upate_profile = serializer.update(profile, request.data)
            return Response(ProfileSerializer(upate_profile).data)
        except Profile.DoesNotExist:
            return Response(
                data={
                    "message": "Profile with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )


    def delete(self, request, *args, **kwargs):
        try:
            profile = self.queryset.get(pk=kwargs["pk"])
            profile.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Profile.DoesNotExist:
            return Response(
                data={
                    "message": "Profile with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )