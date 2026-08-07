import random

from django.db import transaction
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from notifications.models import Notification

from orders.models import (
    Order,
    OrderStatusHistory,
)

from .models import (
    Payment,
)

from .serializers import (
    PaymentSerializer,
)


# ==========================================================
# Create Payment API
# ==========================================================

class PaymentCreateAPIView(APIView):

    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request, order_id):

        try:

            order = get_object_or_404(
                Order,
                pk=order_id,
                account=request.user,
            )

            if hasattr(
                order,
                "payment",
            ):

                return Response(
                    {
                        "message":
                        "Payment already exists."
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            serializer = PaymentSerializer(
                data=request.data,
            )

            serializer.is_valid(
                raise_exception=True,
            )

            payment = serializer.save(
                order=order,
                account=request.user,
                amount=order.total_amount,
                payment_status=(
                    Payment.PaymentStatus.PENDING
                ),
                transaction_id="",
            )

            return Response(
                {
                    "message":
                    "Payment initiated successfully.",
                    "data": PaymentSerializer(
                        payment
                    ).data,
                },
                status=status.HTTP_201_CREATED,
            )

        except Exception as e:

            return Response(
                {
                    "success": False,
                    "message":
                    "Payment initiation failed.",
                    "error": str(e),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

# ==========================================================
# Payment List API
# ==========================================================

class PaymentListAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        payments = (
            Payment.objects
            .select_related(
                "order",
                "account",
            )
            .filter(
                account=request.user,
            )
            .order_by("-created_at")
        )

        serializer = PaymentSerializer(
            payments,
            many=True,
            context={
                "request": request,
            },
        )

        return Response(
            {
                "message":
                "Payments fetched successfully.",
                "count": payments.count(),
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


# ==========================================================
# Payment Detail API
# ==========================================================

class PaymentDetailAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, pk):

        payment = get_object_or_404(
            Payment.objects.select_related(
                "order",
                "account",
            ),
            pk=pk,
            account=request.user,
        )

        serializer = PaymentSerializer(
            payment,
            context={
                "request": request,
            },
        )

        return Response(
            {
                "message":
                "Payment fetched successfully.",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

# ==========================================================
# Confirm Payment API
# ==========================================================

class PaymentConfirmAPIView(APIView):

    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def put(self, request, pk):

        try:

            payment = get_object_or_404(
                Payment,
                pk=pk,
                account=request.user,
            )

            if (
                payment.payment_status
                == Payment.PaymentStatus.SUCCESS
            ):

                return Response(
                    {
                        "message":
                        "Payment already completed."
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )


            # ==========================
            # Update Payment
            # ==========================

            payment.payment_status = (
                Payment.PaymentStatus.SUCCESS
            )

            payment.transaction_id = (
                f"TXN{random.randint(10000000,99999999)}"
            )

            payment.save()


            # ==========================
            # Update Order
            # ==========================

            order = payment.order

            order.status = (
                Order.OrderStatus.CONFIRMED
            )

            order.save()


            # ==========================
            # Order Status History
            # ==========================

            OrderStatusHistory.objects.create(
                order=order,
                status=Order.OrderStatus.CONFIRMED,
                remarks="Payment successful.",
            )


            # ==========================
            # Notification
            # ==========================

            Notification.objects.create(
                account=request.user,
                title="Payment Successful",
                message=(
                    f"Payment received for Order #{order.id}."
                ),
                notification_type=(
                    Notification.NotificationType.PAYMENT
                ),
            )


            return Response(
                {
                    "message":
                    "Payment confirmed successfully.",
                    "data": PaymentSerializer(
                        payment
                    ).data,
                },
                status=status.HTTP_200_OK,
            )


        except Exception as e:

            return Response(
                {
                    "success": False,
                    "message":
                    "Payment confirmation failed.",
                    "error": str(e),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )