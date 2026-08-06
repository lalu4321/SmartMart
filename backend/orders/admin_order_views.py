from django.shortcuts import get_object_or_404
from django.db.models import Q

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework import status

from notifications.models import Notification

from .models import (
    Order,
    OrderStatusHistory,
)

from .admin_order_serializers import (
    AdminOrderSerializer,
    AdminOrderStatusSerializer,
)


class AdminOrderListAPIView(APIView):

    permission_classes = [IsAdminUser]

    def get(self, request):

        orders = Order.objects.select_related(
            "account",
            "shipping_address"
        ).prefetch_related(
            "items",
            "status_history"
        )

        search = request.query_params.get("search")

        if search:

            orders = orders.filter(

                Q(order_number__icontains=search)

                | Q(account__username__icontains=search)

                | Q(account__email__icontains=search)

                | Q(account__phone__icontains=search)

            )

        status_filter = request.query_params.get("status")

        if status_filter:

            orders = orders.filter(
                status=status_filter
            )

        serializer = AdminOrderSerializer(
            orders.order_by("-created_at"),
            many=True,
            context={"request": request},
        )

        return Response(
            {
                "message": "Orders fetched successfully.",
                "count": orders.count(),
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

class AdminOrderDetailAPIView(APIView):

    permission_classes = [IsAdminUser]

    def get(self, request, pk):

        order = get_object_or_404(
            Order.objects.select_related(
                "account",
                "shipping_address"
            ).prefetch_related(
                "items",
                "status_history"
            ),
            pk=pk
        )

        serializer = AdminOrderSerializer(
            order,
            context={
                "request": request
            }
        )

        return Response(
            {
                "message": "Order fetched successfully.",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

class AdminOrderStatusAPIView(APIView):

    permission_classes = [IsAdminUser]

    def put(self, request, pk):

        try:

            order = get_object_or_404(
                Order,
                pk=pk
            )

            serializer = AdminOrderStatusSerializer(
                data=request.data
            )

            serializer.is_valid(
                raise_exception=True
            )

            new_status = serializer.validated_data["status"]

            order.status = new_status

            order.save(
                update_fields=["status"]
            )

            OrderStatusHistory.objects.create(
                order=order,
                status=new_status,
                remarks=f"Order status updated to {new_status} by admin."
            )

            Notification.objects.create(
                account=order.account,
                title="Order Status Updated",
                message=f"Your order {order.order_number} status has been updated to {new_status}.",
                notification_type=Notification.NotificationType.ORDER
            )

            return Response(
                {
                    "message": "Order status updated successfully.",
                    "data": {
                        "id": order.id,
                        "order_number": order.order_number,
                        "status": order.status,
                    },
                },
                status=status.HTTP_200_OK,
            )

        except Exception as e:

            return Response(
                {
                    "success": False,
                    "message": "Failed to update order status.",
                    "error": str(e),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

class AdminOrderDeleteAPIView(APIView):

    permission_classes = [IsAdminUser]

    def delete(self, request, pk):

        try:

            order = get_object_or_404(
                Order,
                pk=pk
            )

            order_number = order.order_number

            order.delete()

            return Response(
                {
                    "message": f"Order {order_number} deleted successfully."
                },
                status=status.HTTP_200_OK,
            )

        except Exception as e:

            return Response(
                {
                    "success": False,
                    "message": "Failed to delete order.",
                    "error": str(e),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )