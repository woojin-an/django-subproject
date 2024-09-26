from django.urls import path

from users import views

urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='signup'),
]
