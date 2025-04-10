from django.urls import path
from .views import MenuViewSet, MenuVoteViewSet

app_name = 'menus'


urlpatterns = [
    path('', MenuViewSet.as_view({'get': 'list', 'post': 'create'}), name='menus'),
    path('<int:pk>/', MenuViewSet.as_view({'get': 'retrieve',
                                           'put': 'update',
                                           'delete': 'destroy'})),
    path('today_menu/', MenuViewSet.as_view({'get': 'today_menu'})),
    path('today_rating/', MenuViewSet.as_view({'get': 'today_rating'})),
    path('vote/', MenuVoteViewSet.as_view({'post': 'create'})),
]
