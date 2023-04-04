import base64
import json

from random import random
from channels.auth import get_user_model
from django.core.mail.backends import console
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APITransactionTestCase

from trips.serializers import TripSerializer, UserSerializer
from trips.models import Trip

PASSWORD = "buch4spu"  # default password for all users

DUMMY_USER_DATA_SIGNUP = {
    "username": "testUser123",
    "email": "test@test.com",
    "first_name": "Test",
    "last_name": "User",
    "password1": PASSWORD,
    "password2": PASSWORD,
}


class AuthenticationTest(APITestCase):
    fixtures = ["users.json", "trips.json"]

    def setUp(self):
        self.user = get_user_model().objects.get(username="asc")
        response = self.client.post(
            reverse("login"),
            data={
                "username": self.user.username,
                "password": PASSWORD,
            },
        )
        self.access = response.data["access"]

    def test_user_can_sign_up(self):
        response = self.client.post(
            reverse("signup"),
            data=DUMMY_USER_DATA_SIGNUP,
        )
        user = get_user_model().objects.last()

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(response.data["id"], user.id)
        self.assertEqual(response.data["username"], user.username)
        self.assertEqual(response.data["first_name"], user.first_name)
        self.assertEqual(response.data["last_name"], user.last_name)

    def test_user_cannot_sign_up_with_existing_username(self):
        response = self.client.post(
            reverse("signup"),
            data={
                "username": self.user.username,
                "email": f"{random() * 25}@test.com",
                "first_name": "Batata",
                "last_name": "Doce",
                "password1": PASSWORD,
                "password2": PASSWORD,
            },
        )
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_user_can_login(self):
        response = self.client.post(
            reverse("login"),
            data={
                "username": self.user.username,
                "password": PASSWORD,
            },
        )

        access = response.data["access"]
        header, payload, signature = access.split(".")
        decoded_payload = base64.b64decode(f"{payload}==")
        payload_data = json.loads(decoded_payload)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertIsNotNone(response.data["refresh"])
        self.assertEqual(payload_data["id"], self.user.id)
        self.assertEqual(payload_data["username"], self.user.username)
        self.assertEqual(payload_data["first_name"], self.user.first_name)
        self.assertEqual(payload_data["last_name"], self.user.last_name)

    def test_user_can_list_trips(self):
        Trip.objects.create(pick_up_address="Rua 1", drop_off_address="Rua 2")
        Trip.objects.create(pick_up_address="Rua 2", drop_off_address="Rua 3")

        response = self.client.get(
            reverse("trips:trip_list"),
            HTTP_AUTHORIZATION=f"Bearer {self.access}",
        )

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        AllTrips = Trip.objects.all()

        exp_trips_ids = [str(trip.id) for trip in AllTrips]
        act_trips_ids = [trip["id"] for trip in response.data]
        self.assertCountEqual(exp_trips_ids, act_trips_ids)

    def test_user_can_retrieve_trip_by_id(self):
        trip = Trip.objects.create(pick_up_address="Rua 1", drop_off_address="Rua 2")

        response = self.client.get(
            trip.get_absolute_url(),
            HTTP_AUTHORIZATION=f"Bearer {self.access}",
        )

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(str(trip.id), response.data.get("id"))
