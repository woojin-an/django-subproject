from django.contrib.auth import get_user_model, login, logout
from django.shortcuts import get_object_or_404
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from users import serializers
from django.core import signing
from django.core.mail import send_mail
from django.conf import settings

User = get_user_model()


class SignUpView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = serializers.SignUpSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        signer = signing.TimestampSigner()      # 서명 기능 제공, secret_key 를 가지고 특정값을 암호화
        signed_user_email = signer.sign(user.email)
        signer_dump = signing.dumps(signed_user_email)

        self.verify_link = self.request.build_absolute_uri(f'/api/v1/users/verify/?code={signer_dump}')
        subject = '[Tabling]회원가입 인증 메일입니다.'
        message = f'안녕하세요. {user.email}님, 회원가입을 완료하기 위해 아래 링크를 클릭해주세요. \n{self.verify_link}'

        send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email])


class VerifyEmailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        code = request.GET.get('code')

        signer = signing.TimestampSigner()
        try:
            decoded_user_email = signing.loads(code)
            user_email = signer.unsign(decoded_user_email, max_age=60 * 5)
        except (TypeError, signing.SignatureExpired):
            return Response({"detail": "Invalid or expired code"}, status=status.HTTP_400_BAD_REQUEST)

        user = get_object_or_404(User, email=user_email)
        user.is_active = True
        user.save()
        return Response({"detail": "Email verification successful"}, status=status.HTTP_200_OK)


class SessionLoginAPIView(APIView):
    def post(self, request):
        serializer = serializers.UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            login(request, serializer.validated_data.get('user'))
            return Response({'message': 'login successful'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SessionLogoutAPIView(APIView):
    def get(self, request):
        request.session.flush()
        logout(request)
        return Response({'message': 'logout successful.'}, status=status.HTTP_200_OK)