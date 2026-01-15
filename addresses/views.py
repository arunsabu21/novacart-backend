from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Address
from .serializers import AddressSerializer


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def address_list_create(request):
    if request.method == "GET":
        addresses = Address.objects.filter(user=request.user)
        serializer = AddressSerializer(addresses, many=True)
        return Response(serializer.data)

    if request.method == "POST":
        serializer = AddressSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        if serializer.validated_data.get("is_default", False):
            Address.objects.filter(user=request.user, is_default=True).update(
                is_default=False
            )

        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["GET", "PUT", "PATCH", "DELETE"])
@permission_classes([IsAuthenticated])
def address_update_delete(request, address_id):
    try:
        address = Address.objects.get(id=address_id, user=request.user)
    except Address.DoesNotExist:
        return Response(
            {"error": "Address not found"}, status=status.HTTP_404_NOT_FOUND
        )

    # ---------- GET ----------
    if request.method == "GET":
        serializer = AddressSerializer(address)
        return Response(serializer.data)

    # ---------- UPDATE ----------
    if request.method in ["PUT", "PATCH"]:
        serializer = AddressSerializer(address, data=request.data, partial=True)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        if serializer.validated_data.get("is_default"):
            Address.objects.filter(user=request.user, is_default=True).exclude(
                id=address_id
            ).update(is_default=False)

        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    # ---------- DELETE ----------
    if request.method == "DELETE":
        address.delete()
        return Response(
            {"message": "Address deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )
