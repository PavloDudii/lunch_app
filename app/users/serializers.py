"""
Serializer for the employee API View
"""
from django.contrib.auth import get_user_model
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['name', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        """Creates user with encrypted password"""
        user = get_user_model().objects.create_user(**validated_data)
        return user
