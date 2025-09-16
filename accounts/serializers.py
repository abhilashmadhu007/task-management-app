from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("id", "username", "password", "email", "role", "assigned_admin")
        extra_kwargs = {
            "role": {"read_only": True},  # default role is "User"
            "assigned_admin": {"required": False},
        }

    def create(self, validated_data):
        user = User(
            username=validated_data["username"],
            email=validated_data.get("email", ""),
            role="User",  # always User for self-registration
        )
        user.set_password(validated_data["password"])
        user.save()
        return user
