from rest_framework import serializers

from .models import Restaurant


class RestaurantSerializer(serializers.ModelSerializer):
    manager = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Restaurant
        fields = '__all__'

    def validated_owner(self, value):
        if Restaurant.objects.filter(manager=value).exists():
            raise (serializers.ValidationError('User have already registered a restaurant!'))
        return value
