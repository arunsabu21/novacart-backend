from django.urls import path
from .views import RegisterView, UserProfileView, UpdateProfileView, password_reset_confirm

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('profile/update/', UpdateProfileView.as_view(), name='profile-update'),
    path("password-reset/confirm/", password_reset_confirm),
]
