from channels.auth import get_user_model
from django.shortcuts import render
from rest_framework import generics, permissions, viewsets
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import Trip
from .serializers import LogInSerializer, TripSerializer, UserSerializer


class SignUpView(generics.CreateAPIView):
    User_Model = get_user_model()
    queryset = User_Model.objects.all()
    serializer_class = UserSerializer


class LogInView(TokenObtainPairView):
    serializer_class = LogInSerializer


class TripView(viewsets.ReadOnlyModelViewSet):
    lookup_field = "id" # The lookup_field variable tells the view to get the trip record by its id value
    lookup_url_kwarg = "trip_id" # The lookup_url_kwarg variable tells the view what named parameter to use to extract the id value from the URL
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Trip.objects.all()
    serializer_class = TripSerializer
