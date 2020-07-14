from rest_framework import serializers
from django.apps import apps
from .helper.uploader import uploader
from django.contrib.auth.models import User
from .models import Profile

TABLE = apps.get_model('userprofile', 'Profile')
App = 'profile_api'
fields = ('id', 'personal_identification', 'phone_number', 'birth_date', 'bio', 'image', 'category')


class ProfileSerializer(serializers.ModelSerializer):
    
    image_file = serializers.ImageField(required=False)

    class Meta:
        model = Profile
        fields = fields + ('image_file',)

    def get_username(self, obj):
        return obj.User.username

    def update(self, instance, validated_data):
        instance.personal_identification = validated_data.get("personal_identification", instance.personal_identification)
        instance.phone_number = validated_data.get("phone_number", instance.phone_book)
        instance.birth_date = validated_data.get("birth_data", instance.birth_date)
        instance.bio = validated_data.get("bio", instance.bio)
        instance.category = validated_data.get("category", instance.category)

        if validated_data.get("image_file"):
            image = uploader(validated_data.get("image_file"))
            instance.image = image.get("secure_url", instance.image)

        instance.save()
        return instance