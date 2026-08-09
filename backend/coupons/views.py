from decimal import Decimal

from django.shortcuts import get_object_or_404
from django.utils import timezone

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import (
    Coupon,
)

from .serializers import (
    CouponSerializer,
)


# ==========================================================
# Create Coupon API
# ==========================================================

class CouponCreateAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        if request.user.role != "ADMIN":

            return Response(
                {
                    "message":
                    "Only admin can create coupons."
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = CouponSerializer(
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
                CouponSerializer(coupon).data,
            },
            status=status.HTTP_201_CREATED,
        )

# ==========================================================
# Coupon List API
# ==========================================================

class CouponListAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        coupons = (
            Coupon.objects
            .all()
            .order_by(
                "-created_at",
            )
        )

        serializer = CouponSerializer(
            coupons,
            many=True,
        )

        return Response(
            {
                "count":
                coupons.count(),

                "data":
                serializer.data,
            },
            status=status.HTTP_200_OK,
        )


# ==========================================================
# Coupon Detail API
# ==========================================================

class CouponDetailAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, pk):

        coupon = get_object_or_404(
            Coupon,
            pk=pk,
        )

        serializer = CouponSerializer(
            coupon,
        )

        return Response(
            {
                "data":
                serializer.data,
            },
            status=status.HTTP_200_OK,
        )

# ==========================================================
# Update Coupon API
# ==========================================================

class CouponUpdateAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def put(self, request, pk):

        if request.user.role != "ADMIN":

            return Response(
                {
                    "message":
                    "Only admin can update coupons."
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        coupon = get_object_or_404(
            Coupon,
            pk=pk,
        )

        serializer = CouponSerializer(
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
# Delete Coupon API
# ==========================================================

class CouponDeleteAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):

        if request.user.role != "ADMIN":

            return Response(
                {
                    "message":
                    "Only admin can delete coupons."
                },
                status=status.HTTP_403_FORBIDDEN,
            )

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

# ==========================================================
# Apply Coupon API
# ==========================================================

class ApplyCouponAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        try:

            code = request.data.get(
                "code"
            )

            order_amount = request.data.get(
                "order_amount"
            )


            if not code or not order_amount:

                return Response(
                    {
                        "message":
                        "Coupon code and order amount are required."
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )


            try:

                order_amount = Decimal(
                    order_amount
                )

            except:

                return Response(
                    {
                        "message":
                        "Invalid order amount."
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )


            coupon = Coupon.objects.filter(
                code=code,
                is_active=True,
            ).first()


            if not coupon:

                return Response(
                    {
                        "message":
                        "Invalid coupon."
                    },
                    status=status.HTTP_404_NOT_FOUND,
                )


            now = timezone.now()


            if now < coupon.valid_from:

                return Response(
                    {
                        "message":
                        "Coupon is not active yet."
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )


            if now > coupon.valid_until:

                return Response(
                    {
                        "message":
                        "Coupon has expired."
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )


            if coupon.used_count >= coupon.usage_limit:

                return Response(
                    {
                        "message":
                        "Coupon usage limit exceeded."
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )


            if order_amount < coupon.minimum_order_amount:

                return Response(
                    {
                        "message":
                        f"Minimum order amount is {coupon.minimum_order_amount}."
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )


            if (
                coupon.discount_type
                ==
                Coupon.DiscountType.PERCENTAGE
            ):

                discount = (
                    order_amount *
                    coupon.discount_value
                ) / Decimal("100")


                if coupon.maximum_discount:

                    discount = min(
                        discount,
                        coupon.maximum_discount,
                    )


            else:

                discount = coupon.discount_value



            final_amount = (
                order_amount -
                discount
            )


            if final_amount < 0:

                final_amount = Decimal("0")



            return Response(
                {
                    "message":
                    "Coupon applied successfully.",

                    "coupon":
                    coupon.code,

                    "discount":
                    discount,

                    "final_amount":
                    final_amount,
                },
                status=status.HTTP_200_OK,
            )


        except Exception as e:

            return Response(
                {
                    "success": False,

                    "message":
                    "Failed to apply coupon.",

                    "error":
                    str(e),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )