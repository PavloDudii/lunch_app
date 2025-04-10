from django.db.models import Count
from rest_framework import viewsets, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.decorators import action
from datetime import date

from .serializers import MenuSerializer, MenuVoteSerializer
from .models import Menu, MenuVote
from common.permissions import (IsRestaurantStaffOrReadOnly,
                                IsNotRestaurantStaff)


class MenuViewSet(viewsets.ModelViewSet):
    serializer_class = MenuSerializer
    permission_classes = [IsRestaurantStaffOrReadOnly]
    queryset = Menu.objects.all()

    @action(methods=['get'], url_path='today_menu', detail=False)
    def today_menu(self, request):
        menu = (self.queryset
                .filter(date=date.today())
                .annotate(votes=Count('menu_votes'))
                .order_by('-votes')
                .first())

        serializer = self.get_serializer(menu)
        return Response(serializer.data)

    @action(methods=['get'], url_path='today_rating', detail=False)
    def today_rating(self, request):
        menus = (self.queryset
                .filter(date=date.today())
                .annotate(votes=Count('menu_votes'))
                .order_by('-votes'))

        serializer = self.get_serializer(menus, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        return self.queryset


class MenuVoteViewSet(viewsets.ModelViewSet):
    serializer_class = MenuVoteSerializer
    permission_classes = [IsNotRestaurantStaff]
    queryset = MenuVote.objects.all()

    def get_queryset(self):
        return self.queryset

    def perform_create(self, serializer):
        user = self.request.user
        today = date.today()
        app_version = self.request.app_version

        if MenuVote.objects.filter(user=user, created_at=today).exists():
            raise ValidationError('You have already voted!')

        if app_version < '2.0.0':
            warning_message = 'Your app version is outdated.'
            response_data = {
                'warning': warning_message,
                'voting_allowed': False
            }
            return Response(response_data, status=status.HTTP_200_OK)

        serializer.save(user=user)
