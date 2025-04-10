from django.urls import path
from .views import RestaurantViewSet


app_name = 'restaurants'


urlpatterns = [
    path('', RestaurantViewSet.as_view({'get': 'list', 'post': 'create'}), name='restaurants'),
    path('<int:pk>/', RestaurantViewSet.as_view({'get': 'retrieve',
                                                 'put': 'update',
                                                 'delete': 'destroy'}),
         name='restaurant-detail')
]
