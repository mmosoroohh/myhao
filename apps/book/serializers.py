from rest_framework import serializers
from django.apps import apps
from django.contrib.auth.models import User
from ..userprofile.models import Profile
from ..homes.models import Homes
from .models import Book
from ..userprofile.serializers import ProfileSerializer

fields = ('id', 'amount', 'user', 'home')



class BookSerializer(serializers.ModelSerializer):
    developer = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Book
        fields = fields + ('developer',)

    def get_developer(self, obj):
        try:
            serializer = ProfileSerializer(
                instance = Profile.objects.get(user=obj.user)
            )
            return serializer.data
        except:
            return {}

    def update(self, instance, validated_data):
        instance.amount = validated_data.get('amount', instance.amount)
        instance.save()

        return instance
