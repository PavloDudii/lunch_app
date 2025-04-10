"""
Custom permissions to separate employees(users) from restaurant staff
"""
from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsRestaurantStaffOrReadOnly(BasePermission):
    """
    Allow staff to do use any methods,
    employees(users) can only read
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        if not request.user.is_authenticated or not request.user.is_restaurant_staff:
            return False

        if view.__class__.__name__ == 'MenuViewSet' and request.method == 'POST':
            restaurant_id = request.data.get('restaurant')
            if restaurant_id:
                from restaurants.models import Restaurant
                try:
                    restaurant = Restaurant.objects.get(pk=restaurant_id)
                    return restaurant.manager == request.user
                except Restaurant.DoesNotExist:
                    return False

        return True

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        if not request.user.is_authenticated or not request.user.is_restaurant_staff:
            return False

        if hasattr(obj, 'manager'):  # Restaurant
            return obj.manager == request.user
        elif hasattr(obj, 'restaurant'):  # Menu
            return obj.restaurant.manager == request.user

        return False


class IsNotRestaurantStaff(BasePermission):
    """
    Allow only employees(users)
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and not request.user.is_restaurant_staff
