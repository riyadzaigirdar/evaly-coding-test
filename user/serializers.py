import re
from rest_framework import serializers
from django.contrib.auth import get_user_model
from user import models


class UserProfileSerializer(serializers.ModelSerializer):
    is_admin = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = ['id', 'email', 'name', 'password',
                  'profile_photo', 'is_admin', 'is_member']
        read_only_fields = ['is_admin', 'is_member']
        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {'input_type': 'password'}
            }
        }

    def get_is_admin(self, obj):
        return obj.is_superuser

    def create(self, validated_data):
        user = models.User.objects.create_user(**validated_data)
        return user


class UserImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ['id', 'profile_photo']
