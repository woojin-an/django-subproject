from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers


User = get_user_model()


class SignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        exclude = ['is_active', 'is_superuser', 'last_login', 'groups', 'user_permissions']

    def create(self, validated_data):
        user = super().create(validated_data)
        if validated_data.get('password'):
            user.set_password(validated_data.get('password'))
            user.save()
        else:
            raise serializers.ValidationError(
                detail='Password is required.', code='password'
            )
        return user


class UserLoginSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'), **attrs)
            if not user:
                raise serializers.ValidationError(
                    detail='Unable to log in with provided credentials.', code='authorization'
                )
        else:
            raise serializers.ValidationError(
                detail='Must be Required "email" and "password".', code='authorization'
            )

        attrs['user'] = user
        return attrs
