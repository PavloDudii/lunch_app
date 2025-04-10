import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status

from rest_framework.test import APIClient

CREATE_USER_URL = reverse('user:register')


@pytest.fixture
def api_client():
    """Fixture for creating a client instance for each test."""
    return APIClient()


@pytest.fixture
def create_user():
    """Fixture to create a user."""
    def _create_user(**params):
        return get_user_model().objects.create_user(**params)
    return _create_user


@pytest.mark.django_db
def test_create_user_with_email_successful(create_user):
    """Test creating a user with email is successful."""
    email = "test@example.com"
    password = "test_password"
    user = create_user(email=email, password=password)

    assert user.email == email
    assert user.check_password(password)


@pytest.mark.django_db
def test_new_user_email_normalized(create_user):
    """Test email is normalized for new user."""
    sample_emails = [
        ['test1@EXAMPLE.com', 'test1@example.com'],
        ['Test2@EXAmPLE.com', 'Test2@example.com'],
        ['TEST3@EXAMPLE.com', 'TEST3@example.com'],
        ['test4@example.COM', 'test4@example.com'],
    ]
    for email, expected_email in sample_emails:
        user = create_user(email=email, password='sample123')
        assert user.email == expected_email


@pytest.mark.django_db
def test_new_user_without_email_raises_error():
    """Test that creating a user without an email raises a ValueError."""
    with pytest.raises(ValueError):
        get_user_model().objects.create_user('', 'sample123')


@pytest.mark.django_db
def test_create_superuser(create_user):
    """Test creating a superuser."""
    user = get_user_model().objects.create_superuser(
        'test@example.com', 'sample123'
    )

    assert user.is_superuser
    assert user.is_staff


@pytest.mark.django_db
def test_create_user_success(api_client, create_user):
    """Test creating a user via the public API."""
    payload = {
        'email': 'test@example.com',
        'password': 'test123',
        'name': 'Test Name',
    }
    res = api_client.post(CREATE_USER_URL, payload)

    assert res.status_code == status.HTTP_201_CREATED
    user = get_user_model().objects.get(email=payload['email'])
    assert user.check_password(payload['password'])
    assert 'password' not in res.data


@pytest.mark.django_db
def test_user_with_email_exists_error(api_client, create_user):
    """Test creating a user with an email that already exists."""
    payload = {
        'email': 'test@example.com',
        'password': 'test123',
        'name': 'Test Name',
    }
    create_user(**payload)
    res = api_client.post(CREATE_USER_URL, payload)

    assert res.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_password_too_short(api_client):
    """Test that the password is too short for the user."""
    payload = {
        'email': 'test@example.com',
        'password': 'te',
        'name': 'Test Name',
    }
    res = api_client.post(CREATE_USER_URL, payload)

    assert res.status_code == status.HTTP_400_BAD_REQUEST
    user_exists = get_user_model().objects.filter(
        email=payload['email']
    ).exists()
    assert not user_exists
