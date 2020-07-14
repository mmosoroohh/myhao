from rest_framework import serializers
from django.apps import apps
from django.contrib.auth.models import User
from .models import Homes

fields = ('name', 'location', 'size', 'price', 'status')



class HomeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Homes
        fields = fields

    def update(self, instance, validate_data):
        instance.name = validate_data.get("name", instance.name)
        instance.location = validate_data.get("location", instance.location)
        instance.size = validate_data.get("size", instance.size)
        instance.price = validate_data.get("price", instance.price)
        instance.status = validate_data.get("status", instance.status)

        instance.save()

        return instance