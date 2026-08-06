from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework import status

from .models import SellerProfile
from .admin_seller_serializers import AdminSellerSerializer


class AdminSellerListAPIView(APIView):

    permission_classes = [IsAdminUser]

    def get(self, request):

        sellers = SellerProfile.objects.select_related("account")

        serializer = AdminSellerSerializer(
            sellers,
            many=True
        )

        return Response(
            {
                "message": "Sellers fetched successfully.",
                "count": sellers.count(),
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


class AdminSellerDetailAPIView(APIView):

    permission_classes = [IsAdminUser]

    def get(self, request, pk):

        seller = get_object_or_404(
            SellerProfile,
            pk=pk
        )

        serializer = AdminSellerSerializer(seller)

        return Response(
            {
                "message": "Seller fetched successfully.",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

class AdminSellerStatusAPIView(APIView):

    permission_classes = [IsAdminUser]

    def patch(self, request, pk):

        print("Logged in admin:", request.user.username)

        seller = get_object_or_404(
            SellerProfile,
            pk=pk
        )

        print("Seller account:", seller.account.username)

        seller.account.is_active = not seller.account.is_active
        seller.account.save(update_fields=["is_active"])

        print("Seller active:", seller.account.is_active)

        return Response(
            {
                "message": (
                    "Seller activated successfully."
                    if seller.account.is_active
                    else
                    "Seller deactivated successfully."
                ),
                "data": {
                    "id": seller.id,
                    "is_active": seller.account.is_active,
                },
            },
            status=status.HTTP_200_OK,
        )

class AdminSellerDeleteAPIView(APIView):

    permission_classes = [IsAdminUser]

    def delete(self, request, pk):

        seller = get_object_or_404(
            SellerProfile,
            pk=pk
        )

        seller.account.delete()

        return Response(
            {
                "message": "Seller deleted successfully."
            },
            status=status.HTTP_200_OK,
        )