from django.shortcuts import get_object_or_404
from django.db.models import Q

from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import (
    Coupon,
)

from .admin_coupon_serializers import (
    AdminCouponSerializer,
    AdminCouponStatusSerializer,
)


# ==========================================================
# Admin Coupon List API
# ==========================================================

class AdminCouponListAPIView(APIView):

    permission_classes = [IsAdminUser]

    def get(self, request):

        coupons = Coupon.objects.all()

        search = request.query_params.get(
            "search"
        )

        if search:

            coupons = coupons.filter(

                Q(
                    code__icontains=search
                )

                |

                Q(
                    description__icontains=search
                )

            )


        status_filter = request.query_params.get(
            "status"
        )


        if status_filter:

            if status_filter.lower() == "active":

                coupons = coupons.filter(
                    is_active=True
                )

            elif status_filter.lower() == "inactive":

                coupons = coupons.filter(
                    is_active=False
                )


        serializer = AdminCouponSerializer(
            coupons.order_by(
                "-created_at"
            ),
            many=True,
        )


        return Response(
            {
                "message":
                "Coupons fetched successfully.",

                "count":
                coupons.count(),

                "data":
                serializer.data,
            },
            status=status.HTTP_200_OK,
        )

# ==========================================================
# Admin Coupon Detail API
# ==========================================================

class AdminCouponDetailAPIView(APIView):

    permission_classes = [IsAdminUser]

    def get(self, request, pk):

        coupon = get_object_or_404(
            Coupon,
            pk=pk,
        )

        serializer = AdminCouponSerializer(
            coupon,
        )

        return Response(
            {
                "message":
                "Coupon fetched successfully.",

                "data":
                serializer.data,
            },
            status=status.HTTP_200_OK,
        )


# ==========================================================
# Admin Coupon Create API
# ==========================================================

class AdminCouponCreateAPIView(APIView):

    permission_classes = [IsAdminUser]

    def post(self, request):

        serializer = AdminCouponSerializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        coupon = serializer.save()

        return Response(
            {
                "message":
                "Coupon created successfully.",

                "data":
                AdminCouponSerializer(
                    coupon
                ).data,
            },
            status=status.HTTP_201_CREATED,
        )

# ==========================================================
# Admin Coupon Update API
# ==========================================================

class AdminCouponUpdateAPIView(APIView):

    permission_classes = [IsAdminUser]

    def put(self, request, pk):

        coupon = get_object_or_404(
            Coupon,
            pk=pk,
        )

        serializer = AdminCouponSerializer(
            coupon,
            data=request.data,
            partial=True,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        serializer.save()

        return Response(
            {
                "message":
                "Coupon updated successfully.",

                "data":
                serializer.data,
            },
            status=status.HTTP_200_OK,
        )


# ==========================================================
# Admin Coupon Delete API
# ==========================================================

class AdminCouponDeleteAPIView(APIView):

    permission_classes = [IsAdminUser]

    def delete(self, request, pk):

        try:

            coupon = get_object_or_404(
                Coupon,
                pk=pk,
            )

            coupon.delete()

            return Response(
                {
                    "message":
                    "Coupon deleted successfully."
                },
                status=status.HTTP_200_OK,
            )


        except Exception as e:

            return Response(
                {
                    "success": False,

                    "message":
                    "Failed to delete coupon.",

                    "error":
                    str(e),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

# ==========================================================
# Admin Coupon Status API
# ==========================================================

class AdminCouponStatusAPIView(APIView):

    permission_classes = [IsAdminUser]

    def patch(self, request, pk):

        try:

            coupon = get_object_or_404(
                Coupon,
                pk=pk,
            )


            coupon.is_active = (
                not coupon.is_active
            )


            coupon.save(
                update_fields=[
                    "is_active",
                ]
            )


            return Response(
                {
                    "message": (
                        "Coupon activated successfully."
                        if coupon.is_active
                        else
                        "Coupon deactivated successfully."
                    ),

                    "data": {
                        "id":
                        coupon.id,

                        "is_active":
                        coupon.is_active,
                    },
                },
                status=status.HTTP_200_OK,
            )


        except Exception as e:

            return Response(
                {
                    "success": False,

                    "message":
                    "Failed to update coupon status.",

                    "error":
                    str(e),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )