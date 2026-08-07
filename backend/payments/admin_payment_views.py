from django.db.models import Q
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.permissions import IsAdminUser
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

from .admin_payment_serializers import (
    AdminPaymentSerializer,
    AdminPaymentStatusSerializer,
)


# ==========================================================
# Admin Payment List API
# ==========================================================

class AdminPaymentListAPIView(APIView):

    permission_classes = [IsAdminUser]

    def get(self, request):

        payments = (
            Payment.objects
            .select_related(
                "account",
                "order",
            )
        )

        search = request.query_params.get(
            "search"
        )

        if search:

            payments = payments.filter(

                Q(
                    transaction_id__icontains=search
                )

                | Q(
                    order__order_number__icontains=search
                )

                | Q(
                    account__username__icontains=search
                )

                | Q(
                    account__email__icontains=search
                )

                | Q(
                    account__phone__icontains=search
                )

            )

        payment_status = request.query_params.get(
            "payment_status"
        )

        if payment_status:

            payments = payments.filter(
                payment_status=payment_status
            )

        payments = payments.order_by(
            "-created_at"
        )

        serializer = AdminPaymentSerializer(
            payments,
            many=True,
        )

        return Response(
            {
                "message":
                "Payments fetched successfully.",
                "count":
                payments.count(),
                "data":
                serializer.data,
            },
            status=status.HTTP_200_OK,
        )

# ==========================================================
# Admin Payment Detail API
# ==========================================================

class AdminPaymentDetailAPIView(APIView):

    permission_classes = [IsAdminUser]

    def get(self, request, pk):

        payment = get_object_or_404(
            Payment.objects.select_related(
                "account",
                "order",
            ),
            pk=pk,
        )

        serializer = AdminPaymentSerializer(
            payment,
        )

        return Response(
            {
                "message":
                "Payment fetched successfully.",
                "data":
                serializer.data,
            },
            status=status.HTTP_200_OK,
        )

# ==========================================================
# Admin Payment Status Update API
# ==========================================================

class AdminPaymentStatusAPIView(APIView):

    permission_classes = [IsAdminUser]

    def put(self, request, pk):

        try:

            payment = get_object_or_404(
                Payment,
                pk=pk,
            )

            serializer = AdminPaymentStatusSerializer(
                data=request.data,
            )

            serializer.is_valid(
                raise_exception=True,
            )

            new_status = serializer.validated_data[
                "payment_status"
            ]

            payment.payment_status = new_status

            payment.save(
                update_fields=[
                    "payment_status",
                ]
            )


            # ==================================
            # If Payment Successful
            # Update Order Status
            # ==================================

            if (
                new_status
                == Payment.PaymentStatus.SUCCESS
            ):

                order = payment.order

                if (
                    order.status
                    == Order.OrderStatus.PENDING
                ):

                    order.status = (
                        Order.OrderStatus.CONFIRMED
                    )

                    order.save(
                        update_fields=[
                            "status",
                        ]
                    )


                    OrderStatusHistory.objects.create(
                        order=order,
                        status=(
                            Order.OrderStatus.CONFIRMED
                        ),
                        remarks=(
                            "Payment confirmed by admin."
                        ),
                    )


                Notification.objects.create(
                    account=payment.account,
                    title="Payment Successful",
                    message=(
                        f"Payment for Order "
                        f"{order.order_number} "
                        f"has been confirmed."
                    ),
                    notification_type=(
                        Notification.NotificationType.PAYMENT
                    ),
                )


            return Response(
                {
                    "message":
                    "Payment status updated successfully.",
                    "data": {
                        "id": payment.id,
                        "payment_status":
                        payment.payment_status,
                    },
                },
                status=status.HTTP_200_OK,
            )


        except Exception as e:

            return Response(
                {
                    "success": False,
                    "message":
                    "Failed to update payment status.",
                    "error": str(e),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )