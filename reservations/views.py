from rest_framework.generics import CreateAPIView
from reservations import serializers
from reservations.models import Reservation


class ReservationCreateAPIView(CreateAPIView):
    serializer_class = serializers.ReservationSerializer
    queryset = Reservation.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


