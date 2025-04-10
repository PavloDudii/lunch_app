from rest_framework import viewsets

from .models import Restaurant
from .serializers import RestaurantSerializer
from common.permissions import IsRestaurantStaffOrReadOnly


class RestaurantViewSet(viewsets.ModelViewSet):
    serializer_class = RestaurantSerializer
    permission_classes = [IsRestaurantStaffOrReadOnly]
    queryset = Restaurant.objects.all()

    def get_queryset(self):
        return self.queryset

    def perform_create(self, serializer):
        serializer.save(manager=self.request.user)
