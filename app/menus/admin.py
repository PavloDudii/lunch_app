from django.contrib import admin
from .models import Menu, MenuVote


class MenuVoteAdmin(admin.ModelAdmin):
    list_display = ('menu', 'user', 'created_at')


class MenuAdmin(admin.ModelAdmin):
    list_display = ('restaurant', 'date')
    list_filter = ('date', )


admin.site.register(MenuVote, MenuVoteAdmin)
admin.site.register(Menu, MenuAdmin)
