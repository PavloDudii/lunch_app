from django.db import models
from django.conf import settings

from restaurants.models import Restaurant


class Menu(models.Model):
    restaurant = models.ForeignKey(
        Restaurant, on_delete=models.CASCADE, related_name='menus'
    )
    date = models.DateField(auto_now_add=True)
    dishes = models.TextField(default='')

    class Meta:
        unique_together = ('restaurant', 'date')

    def __str__(self):
        return f'{self.restaurant.title} menu for {self.date}'


class MenuVote(models.Model):
    menu = models.ForeignKey(
        Menu, on_delete=models.CASCADE, related_name='menu_votes'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.email} voted at {self.created_at}'
