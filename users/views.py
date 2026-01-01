from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.models import User
from .serializers import RegisterSerializer, ProfileSerializer
from rest_framework import status
from rest_framework.views import APIView
from django_rest_passwordreset.models import ResetPasswordToken
from rest_framework.decorators import api_view


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = ProfileSerializer(request.user)
        return Response(serializer.data)


class UpdateProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        serializer = ProfileSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def password_reset_confirm(request):
    token = request.data.get("token")
    password = request.data.get("password")

    # FIXED CONDITION
    if not token or not password:
        return Response({"detail": "Missing token or password"}, status=400)

    try:
        reset_token = ResetPasswordToken.objects.get(key=token)
    except ResetPasswordToken.DoesNotExist:
        return Response({"detail": "Invalid or token expired"}, status=400)

    user = reset_token.user
    user.set_password(password)
    user.save()

    reset_token.delete()

    return Response({"detail": "Password Reset Successful"}, status=200)


@api_view(["GET"])
def create_temp_admin(request):
    if User.objects.filter(username="tempadmin").exists():
        return Response({"message": "Admin already exist"})

    User.objects.create_superuser(
        username="tempadmin", email="admin@example.com", password="Temp@12345"
    )

    return Response({"message": "Temporary admin created"})
