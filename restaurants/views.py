from django.contrib.auth.models import AnonymousUser
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from restaurants.models import Restaurant
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


class RestaurantListCreateAPIView(ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    serializer_class = serializers.RestaurantSerializer
    queryset = Restaurant.objects.all()


class RestaurantDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.RestaurantDetailSerializer
    queryset = Restaurant.objects.all()
    permission_classes = [IsOwner]