import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIRequestFactory, force_authenticate
from rest_framework import status

from .models import Restaurant
from .views import RestaurantViewSet

User = get_user_model()


@pytest.fixture
def regular_user():
    return User.objects.create_user(
        name='regularuser',
        email='regular@example.com',
        password='testpass123',
        is_restaurant_staff=False
    )


@pytest.fixture
def staff_user():
    return User.objects.create_user(
        name='staffuser',
        email='staff@example.com',
        password='testpass123',
        is_restaurant_staff=True
    )


@pytest.fixture
def restaurant(staff_user):
    return Restaurant.objects.create(
        manager=staff_user,
        title='Test Restaurant',
        address='123 Test St',
        phone_number='+1234567890'
    )


@pytest.fixture
def api_factory():
    return APIRequestFactory()


@pytest.mark.django_db
class TestRestaurantPermissions:
    def test_regular_user_cannot_create(self, api_factory, regular_user):
        data = {
            'title': 'New Restaurant',
            'address': '123 Main St',
            'phone_number': '+1234567890'
        }
        request = api_factory.post('/restaurants/', data=data)
        force_authenticate(request, user=regular_user)
        view = RestaurantViewSet.as_view({'post': 'create'})
        response = view(request)
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert Restaurant.objects.count() == 0

    def test_staff_user_can_create(self, api_factory, staff_user):
        data = {
            'title': 'New Restaurant',
            'address': '123 Main St',
            'phone_number': '+1234567890'
        }
        request = api_factory.post('/restaurants/', data=data)
        force_authenticate(request, user=staff_user)
        view = RestaurantViewSet.as_view({'post': 'create'})
        response = view(request)
        assert response.status_code == status.HTTP_201_CREATED
        assert Restaurant.objects.count() == 1
        assert Restaurant.objects.first().manager == staff_user

    def test_regular_user_cannot_update(self, api_factory, regular_user, restaurant):
        data = {
            'title': 'Updated Title',
            'address': restaurant.address,
            'phone_number': restaurant.phone_number
        }
        request = api_factory.put(f'/restaurants/{restaurant.pk}/', data=data)
        force_authenticate(request, user=regular_user)
        view = RestaurantViewSet.as_view({'put': 'update'})
        response = view(request, pk=restaurant.pk)
        assert response.status_code == status.HTTP_403_FORBIDDEN
        restaurant.refresh_from_db()
        assert restaurant.title == 'Test Restaurant'  # Title didn't change

    def test_staff_user_can_update_own_restaurant(self, api_factory, staff_user, restaurant):
        data = {
            'title': 'Updated Title',
            'address': restaurant.address,
            'phone_number': restaurant.phone_number
        }
        request = api_factory.put(f'/restaurants/{restaurant.pk}/', data=data)
        force_authenticate(request, user=staff_user)
        view = RestaurantViewSet.as_view({'put': 'update'})
        response = view(request, pk=restaurant.pk)
        assert response.status_code == status.HTTP_200_OK
        restaurant.refresh_from_db()
        assert restaurant.title == 'Updated Title'

    def test_other_staff_cannot_update_not_their_restaurant(self, api_factory, restaurant):
        other_staff = User.objects.create_user(
            name='otherstaff',
            email='other@example.com',
            password='testpass123',
            is_restaurant_staff=True
        )
        data = {
            'title': 'Hacked Title',
            'address': restaurant.address,
            'phone_number': restaurant.phone_number
        }
        request = api_factory.put(f'/restaurants/{restaurant.pk}/', data=data)
        force_authenticate(request, user=other_staff)
        view = RestaurantViewSet.as_view({'put': 'update'})
        response = view(request, pk=restaurant.pk)
        assert response.status_code == status.HTTP_403_FORBIDDEN
        restaurant.refresh_from_db()
        assert restaurant.title == 'Test Restaurant'


@pytest.mark.django_db
class TestRestaurantViewSet:
    def test_list_restaurants_unauthenticated(self, api_factory, restaurant):
        request = api_factory.get('/restaurants/')
        view = RestaurantViewSet.as_view({'get': 'list'})
        response = view(request)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]['title'] == restaurant.title

    def test_retrieve_restaurant_unauthenticated(self, api_factory, restaurant):
        request = api_factory.get('/restaurants/')
        view = RestaurantViewSet.as_view({'get': 'retrieve'})
        response = view(request, pk=restaurant.pk)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == restaurant.title
