from django.contrib.auth import get_user_model
from rest_framework import serializers


User = get_user_model()


class SignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        # fields = ('username', 'email', 'password')
        exclude = ['is_active', 'is_superuser', 'last_login', 'groups', 'user_permissions']