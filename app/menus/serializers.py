from rest_framework import serializers
from .models import Menu, MenuVote
from datetime import date
from django.db.models.functions import Cast
from django.db import models


class MenuSerializer(serializers.ModelSerializer):

    class Meta:
        model = Menu
        fields = ['id',
                  'restaurant',
                  'date',
                  'dishes']

    def validate_date(self, value):
        from datetime import date
        if value != date.today():
            raise serializers.ValidationError('Menu can only be created for today!')


class MenuVoteSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = MenuVote
        fields = '__all__'

    def validate(self, data):
        user = data['user']
        today = date.today()

        if (MenuVote.objects.
                annotate(created_at_date=Cast('created_at',
                                              output_field=models.DateField())).
                filter(user=user, created_at=today).exists()):
            raise serializers.ValidationError('You have already voted!')

        return data
