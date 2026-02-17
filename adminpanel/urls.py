from django.urls import path
from .views import AdminTestView

urlpatterns = [
    path("test/", AdminTestView.as_view()),
]