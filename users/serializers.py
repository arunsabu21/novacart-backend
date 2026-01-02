from rest_framework import serializers
from django.contrib.auth.models import User


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "email", "password"]

        def create(self, validate_data):
            username = (validate_data["username"],)
            email = (validate_data["email"],)
            password = validate_data["password"]

            if User.objects.filter(username=username).exists():
                raise serializers.ValidationError("Username already exist")

            if email and User.objects.filter(email=email).exists():
                raise serializers.ValidationError("Email already exist")

            user = User.objects.create_user(
                username=username, email=email, password=password
            )
            return user


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name"]
        read_only_fields = ["id", "email"]
