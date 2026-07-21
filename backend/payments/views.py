import random
from django.db import transaction
from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import Payment
from .serializers import PaymentSerializer

from orders.models import Order, OrderStatusHistory

from notifications.models import Notification

class PaymentCreateAPIView(APIView):

    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request, order_id):

        try:

            order = get_object_or_404(
                Order,
                pk=order_id,
                account=request.user
            )

            if hasattr(order, "payment"):

                return Response(
                    {
                        "message": "Payment already exists."
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            serializer = PaymentSerializer(data=request.data)

            serializer.is_valid(raise_exception=True)

            payment = serializer.save(
                order=order,
                account=request.user,
                amount=order.total_amount,
                payment_status=Payment.PaymentStatus.SUCCESS,
                transaction_id=f"TXN{random.randint(10000000,99999999)}"
            )

            order.status = Order.OrderStatus.CONFIRMED
            order.save()

            OrderStatusHistory.objects.create(
                order=order,
                status=Order.OrderStatus.CONFIRMED,
                remarks="Payment successful."
            )

            Notification.objects.create(
                account=request.user,
                title="Payment Successful",
                message=f"Payment received for Order #{order.id}.",
                notification_type=Notification.NotificationType.PAYMENT
            )

            return Response(
                {
                    "message": "Payment completed successfully.",
                    "data": PaymentSerializer(payment).data
                },
                status=status.HTTP_201_CREATED
            )

        except Exception as e:

            return Response(
                {
                    "success": False,
                    "message": "Payment failed.",
                    "error": str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
class PaymentListAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        payments = Payment.objects.filter(
            account=request.user
        )

        serializer = PaymentSerializer(
            payments,
            many=True
        )

        return Response(
            {
                "count": payments.count(),
                "data": serializer.data
            }
        )
    
class PaymentDetailAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, pk):

        payment = get_object_or_404(
            Payment,
            pk=pk,
            account=request.user
        )

        serializer = PaymentSerializer(payment)

        return Response(serializer.data)