from django.contrib.auth.models import AnonymousUser
from rest_framework.generics import CreateAPIView, DestroyAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

from restaurants.models import Menu, Restaurant
from restaurants import serializers
from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):  # Put, Patch, Delete 요청 시 필요한 권한 점검
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user

    def has_permission(self, request, view):  # Post 요청 시 필요한 권한 점검
        if not isinstance(request.user, AnonymousUser):
            if request.method in permissions.SAFE_METHODS:
                return True
            return request.user.is_owner
        return False


class IsRestaurantOwner(IsOwner):
    def has_object_permission(self, request, view, obj):  # Post 요청 시 필요한 권한 점검
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.restaurant.owner == request.user


class RestaurantListCreateAPIView(ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    serializer_class = serializers.RestaurantSerializer
    queryset = Restaurant.objects.all()


class RestaurantDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.RestaurantDetailSerializer
    queryset = Restaurant.objects.all()
    permission_classes = [IsOwner]


class MenuCreateAPIView(CreateAPIView):
    serializer_class = serializers.MenuSerializer
    queryset = Menu.objects.all()
    permission_classes = [IsAuthenticated, IsRestaurantOwner]


class MenuDeleteAPIView(DestroyAPIView):
    queryset = Menu.objects.all()
    permission_classes = [IsAuthenticated, IsRestaurantOwner]
