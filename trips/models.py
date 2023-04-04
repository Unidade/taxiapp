import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class User(AbstractUser):
    pass


class Trip(models.Model):
    REQUESTED = "requested"
    STARTED = "started"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    STATUSES = (
        (REQUESTED, "REQUESTED"),
        (STARTED, "STARTED"),
        (IN_PROGRESS, "IN_PROGRESS"),
        (COMPLETED, "COMPLETED"),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    pick_up_address = models.CharField(max_length=255)
    drop_off_address = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUSES, default=REQUESTED)

    def __str__(self):
        return f"{self:id}: {self.pick_up_address} to {self.drop_off_address}"

    def get_absolute_url(self):
        return reverse("trip:trip_detail", kwargs={"trip_id": self.id})
