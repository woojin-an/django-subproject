from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from users import views

urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('verify/', views.VerifyEmailView.as_view(), name='verify'),
    path('login/', views.SessionLoginAPIView.as_view(), name='session-login'),
    path('logout/', views.SessionLogoutAPIView.as_view(), name='session-logout'),
    # 유저가 보낸 Credential(인증 정보 - email, password)를 검증하고 Access Token과 Refresh 토큰을 응답으로 반환
    path('jwt/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # 유저가 보낸 요청에서 헤더에 담긴 Refresh Token을 검증하여 Access Token을 재생성하여 응답으로 반환
    path('jwt/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('kakao/login/', views.KakaoLoginView.as_view(), name='kakao_login'),
    path('kakao/callback/', views.KakaoCallbackView.as_view(), name='kakao_callback'),
]
