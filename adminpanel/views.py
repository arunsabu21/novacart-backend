from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAdminUser

class AdminTestView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    def get(self, request):
        return Response({"message": "Admin panel working"})