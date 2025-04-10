from django.urls import path
from rest_framework_simplejwt.views import (TokenRefreshView,
                                            TokenObtainPairView)
from . import views


app_name = 'user'


urlpatterns = [
    path('register/', views.CreateUserView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('me/', views.ManageUserView.as_view(), name='me')
]
