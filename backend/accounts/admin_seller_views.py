from django.db import transaction
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import SellerProfile
from .admin_seller_serializers import AdminSellerSerializer


class AdminSellerListAPIView(APIView):

    permission_classes = [IsAdminUser]

    def get(self, request):

        sellers = (
            SellerProfile.objects
            .select_related("account")
            .order_by("-created_at")
        )

        serializer = AdminSellerSerializer(
            sellers,
            many=True,
            context={"request": request},
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
            SellerProfile.objects.select_related("account"),
            pk=pk,
        )

        serializer = AdminSellerSerializer(
            seller,
            context={"request": request},
        )

        return Response(
            {
                "message": "Seller fetched successfully.",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


class AdminSellerStatusAPIView(APIView):

    permission_classes = [IsAdminUser]

    @transaction.atomic
    def patch(self, request, pk):

        try:

            seller = get_object_or_404(
                SellerProfile.objects.select_related("account"),
                pk=pk,
            )

            if seller.account == request.user:
                return Response(
                    {
                        "message": "You cannot change your own account status."
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            seller.account.is_active = not seller.account.is_active

            seller.account.save(
                update_fields=["is_active"]
            )

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

        except Exception as e:

            transaction.set_rollback(True)

            return Response(
                {
                    "success": False,
                    "message": "Failed to update seller status.",
                    "error": str(e),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class AdminSellerDeleteAPIView(APIView):

    permission_classes = [IsAdminUser]

    @transaction.atomic
    def delete(self, request, pk):

        try:

            seller = get_object_or_404(
                SellerProfile.objects.select_related("account"),
                pk=pk,
            )

            if seller.account == request.user:
                return Response(
                    {
                        "message": "You cannot delete your own account."
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            seller.account.delete()

            return Response(
                {
                    "message": "Seller deleted successfully."
                },
                status=status.HTTP_200_OK,
            )

        except Exception as e:

            transaction.set_rollback(True)

            return Response(
                {
                    "success": False,
                    "message": "Failed to delete seller.",
                    "error": str(e),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )