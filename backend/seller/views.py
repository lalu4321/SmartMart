from django.shortcuts import get_object_or_404

from notifications.models import Notification
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from accounts.models import SellerProfile
from django.db.models import Sum, Avg

from products.models import Product
from reviews.models import Review
from orders.models import (Order,OrderStatusHistory,ReturnRequest,)

from .serializers import SellerOrderSerializer,UpdateOrderStatusSerializer,SellerReturnRequestSerializer

class SellerOrderListAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        seller = get_object_or_404(
            SellerProfile,
            account=request.user
        )

        orders = Order.objects.filter(
            items__variant__product__seller=seller
        ).distinct()

        serializer = SellerOrderSerializer(
            orders,
            many=True
        )

        return Response(
            {
                "message": "Orders fetched successfully.",
                "count": orders.count(),
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )
class SellerOrderDetailAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, pk):

        seller = get_object_or_404(
            SellerProfile,
            account=request.user
        )

        order = get_object_or_404(
            Order.objects.filter(
                items__variant__product__seller=seller
            ).distinct(),
            pk=pk
        )

        serializer = SellerOrderSerializer(order)

        return Response(
            {
                "message": "Order fetched successfully.",
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )

class UpdateOrderStatusAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def put(self, request, pk):

        try:

            seller = get_object_or_404(
                SellerProfile,
                account=request.user
            )

            order = get_object_or_404(
                Order.objects.filter(
                    items__variant__product__seller=seller
                ).distinct(),
                pk=pk
            )

            serializer = UpdateOrderStatusSerializer(
                data=request.data
            )

            serializer.is_valid(raise_exception=True)

            new_status = serializer.validated_data["status"]

            order.status = new_status
            order.save()

            Notification.objects.create(
                account=order.account,
                title="Order Status Updated",
                message=f"Your order status has been updated to {order.status}.",
                notification_type=Notification.NotificationType.ORDER
            )

            OrderStatusHistory.objects.create(
                order=order,
                status=new_status,
                remarks=f"Order status updated to {new_status} by seller."
            )

            return Response(
                {
                    "success": True,
                    "message": "Order status updated successfully.",
                    "status": order.status
                },
                status=status.HTTP_200_OK
            )

        except Exception as e:

            return Response(
                {
                    "success": False,
                    "message": "Failed to update order status.",
                    "error": str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
class SellerReturnListAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        seller = get_object_or_404(
            SellerProfile,
            account=request.user
        )

        returns = ReturnRequest.objects.filter(
            order__items__variant__product__seller=seller
        ).distinct()

        serializer = SellerReturnRequestSerializer(
            returns,
            many=True
        )

        return Response(
            {
                "message": "Return requests fetched successfully.",
                "count": returns.count(),
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )
    
class ApproveReturnAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def put(self, request, pk):

        try:

            seller = get_object_or_404(
                SellerProfile,
                account=request.user
            )

            return_request = get_object_or_404(
                ReturnRequest.objects.filter(
                    order__items__variant__product__seller=seller
                ).distinct(),
                pk=pk
            )

            return_request.status = ReturnRequest.ReturnStatus.APPROVED
            return_request.save()

            Notification.objects.create(
                account=return_request.order.account,
                title="Return Approved",
                message="Your return request has been approved.",
                notification_type=Notification.NotificationType.RETURN
            )

            return Response(
                {
                    "message": "Return approved successfully."
                },
                status=status.HTTP_200_OK
            )

        except Exception as e:

            return Response(
                {
                    "success": False,
                    "message": "Failed to approve return request.",
                    "error": str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class RejectReturnAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def put(self, request, pk):

        try:

            seller = get_object_or_404(
                SellerProfile,
                account=request.user
            )

            return_request = get_object_or_404(
                ReturnRequest.objects.filter(
                    order__items__variant__product__seller=seller
                ).distinct(),
                pk=pk
            )

            return_request.status = ReturnRequest.ReturnStatus.REJECTED
            return_request.save()

            Notification.objects.create(
                account=return_request.order.account,
                title="Return Rejected",
                message="Your return request has been rejected.",
                notification_type=Notification.NotificationType.RETURN
            )

            return Response(
                {
                    "message": "Return rejected successfully."
                },
                status=status.HTTP_200_OK
            )

        except Exception as e:

            return Response(
                {
                    "success": False,
                    "message": "Failed to reject return request.",
                    "error": str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
class SellerDashboardAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        seller = get_object_or_404(
            SellerProfile,
            account=request.user
        )

        products = Product.objects.filter(
            seller=seller
        )

        orders = Order.objects.filter(
            items__variant__product__seller=seller
        ).distinct()

        reviews = Review.objects.filter(
            product__seller=seller
        )

        data = {

            "total_products": products.count(),

            "active_products": products.filter(
                is_active=True
            ).count(),

            "inactive_products": products.filter(
                is_active=False
            ).count(),

            "total_orders": orders.count(),

            "pending_orders": orders.filter(
                status=Order.OrderStatus.PENDING
            ).count(),

            "confirmed_orders": orders.filter(
                status=Order.OrderStatus.CONFIRMED
            ).count(),

            "shipped_orders": orders.filter(
                status=Order.OrderStatus.SHIPPED
            ).count(),

            "out_for_delivery_orders": orders.filter(
                status=Order.OrderStatus.OUT_FOR_DELIVERY
            ).count(),

            "delivered_orders": orders.filter(
                status=Order.OrderStatus.DELIVERED
            ).count(),

            "cancelled_orders": orders.filter(
                status=Order.OrderStatus.CANCELLED
            ).count(),

            "total_revenue": orders.filter(
                status=Order.OrderStatus.DELIVERED
            ).aggregate(
                revenue=Sum("total_amount")
            )["revenue"] or 0,

            "total_reviews": reviews.count(),

            "average_rating": reviews.aggregate(
                average=Avg("rating")
            )["average"] or 0

        }

        return Response(
            {
                "message": "Seller dashboard fetched successfully.",
                "data": data
            },
            status=status.HTTP_200_OK
        )