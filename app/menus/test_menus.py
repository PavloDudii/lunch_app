import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIRequestFactory, force_authenticate
from rest_framework import status
from datetime import date

from .models import Menu, MenuVote
from .views import MenuViewSet, MenuVoteViewSet
from restaurants.models import Restaurant


User = get_user_model()


@pytest.fixture
def regular_user():
    return (User.objects.create_user(
        name='Regular User',
        email='regular@example.com',
        password='testpass123',
        is_restaurant_staff=False
    ))


@pytest.fixture
def staff_user():
    return User.objects.create_user(
        name='Staff User',
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
def menu(restaurant):
    return Menu.objects.create(
        restaurant=restaurant,
        date=date.today(),
        dishes="Test Dish 1, Test Dish 2"
    )


@pytest.fixture
def menu_vote(menu, regular_user):
    return MenuVote.objects.create(
        menu=menu,
        user=regular_user
    )


@pytest.fixture
def api_factory():
    return APIRequestFactory()


@pytest.mark.django_db
class TestMenuModel:
    def test_menu_creation(self, menu):
        assert str(menu) == f'{menu.restaurant.title} menu for {menu.date}'
        assert menu.dishes == "Test Dish 1, Test Dish 2"
        assert menu.restaurant.title == 'Test Restaurant'

    def test_unique_together_constraint(self, restaurant):
        Menu.objects.create(
            restaurant=restaurant,
            date=date.today(),
            dishes="First Menu"
        )
        with pytest.raises(Exception):
            Menu.objects.create(
                restaurant=restaurant,
                date=date.today(),
                dishes="Second Menu"
            )


@pytest.mark.django_db
class TestMenuVoteModel:
    def test_menu_vote_creation(self, menu_vote):
        assert str(menu_vote) == f'{menu_vote.user.email} voted at {menu_vote.created_at}'
        assert menu_vote.menu.restaurant.title == 'Test Restaurant'
        assert menu_vote.user.name == 'Regular User'


@pytest.mark.django_db
class TestMenuViewSet:
    def test_list_menus(self, api_factory, menu):
        request = api_factory.get('/menus/')
        view = MenuViewSet.as_view({'get': 'list'})
        response = view(request)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]['restaurant'] == menu.restaurant.id

    def test_create_menu_as_staff(self, api_factory, staff_user, restaurant):
        data = {
            'restaurant': restaurant.id,
            'date': date.today(),
            'dishes': 'Staff Created Menu'
        }
        request = api_factory.post('/menus/', data=data)
        force_authenticate(request, user=staff_user)
        view = MenuViewSet.as_view({'post': 'create'})
        response = view(request)
        assert response.status_code == status.HTTP_201_CREATED
        assert Menu.objects.count() == 1

    def test_create_menu_as_regular_user(self, api_factory, regular_user, restaurant):
        data = {
            'restaurant': restaurant.id,
            'date': date.today(),
            'dishes': 'Regular User Attempt'
        }
        request = api_factory.post('/menus/', data=data)
        force_authenticate(request, user=regular_user)
        view = MenuViewSet.as_view({'post': 'create'})
        response = view(request)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_today_menu_action(self, api_factory, menu):
        # Create another menu with a vote to test ordering
        restaurant2 = Restaurant.objects.create(
            manager=User.objects.create_user(
                name='Second Owner',
                email='owner2@example.com',
                password='testpass123',
                is_restaurant_staff=True
            ),
            title='Second Restaurant',
            address='456 Test St',
            phone_number='+0987654321'
        )
        menu2 = Menu.objects.create(
            restaurant=restaurant2,
            date=date.today(),
            dishes="Second Menu"
        )
        MenuVote.objects.create(menu=menu2, user=regular_user())

        request = api_factory.get('/menus/today_menu/')
        view = MenuViewSet.as_view({'get': 'today_menu'})
        response = view(request)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['restaurant'] == menu2.restaurant.id

    def test_today_rating_action(self, api_factory, menu):
        request = api_factory.get('/menus/today_rating/')
        view = MenuViewSet.as_view({'get': 'today_rating'})
        response = view(request)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]['restaurant'] == menu.restaurant.id


@pytest.mark.django_db
class TestMenuVoteViewSet:
    def test_create_vote_as_regular_user(self, api_factory, regular_user, menu):
        data = {
            'menu': menu.id
        }
        request = api_factory.post('/menus/vote/', data=data)
        force_authenticate(request, user=regular_user)
        view = MenuVoteViewSet.as_view({'post': 'create'})
        response = view(request)
        assert response.status_code == status.HTTP_201_CREATED
        assert MenuVote.objects.count() == 2  # Including the fixture vote

    def test_create_vote_as_staff(self, api_factory, staff_user, menu):
        data = {
            'menu': menu.id
        }
        request = api_factory.post('/menus/vote/', data=data)
        force_authenticate(request, user=staff_user)
        view = MenuVoteViewSet.as_view({'post': 'create'})
        response = view(request)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_duplicate_vote(self, api_factory, regular_user, menu_vote):
        data = {
            'menu': menu_vote.menu.id
        }
        request = api_factory.post('/menus/vote/', data=data)
        force_authenticate(request, user=regular_user)
        view = MenuVoteViewSet.as_view({'post': 'create'})
        response = view(request)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
