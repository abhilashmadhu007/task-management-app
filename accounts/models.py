from django.db import models
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    ROLE_CHOICES = (
        ("SuperAdmin", "SuperAdmin"),
        ("Admin", "Admin"),
        ("User", "User"),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="User")
    # If a User, who is their Admin (nullable for SuperAdmin/Admin)
    assigned_admin = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.SET_NULL, related_name="managed_users",
        limit_choices_to={"role": "Admin"}
    )

    def __str__(self):
        return f"{self.username} ({self.role})"

