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
import traceback


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            print("REGISTER ERROR ------------------------")
            print(e)
            traceback.print_exc()

            return Response(
                {"detail": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


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



