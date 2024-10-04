from django.urls import path
from reservations import views
urlpatterns = [
    path('', views.ReservationCreateAPIView.as_view(), name='reservation_create'),
]