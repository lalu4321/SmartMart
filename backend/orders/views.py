import random

from django.db import transaction
from django.shortcuts import get_object_or_404
from django.utils import timezone

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import Address
from cart.models import Cart
from notifications.models import Notification
from products.models import ProductInventory

from .models import (
    Order,
    OrderItem,
    ReturnRequest,
    Refund,
)
from .serializers import (
    OrderSerializer,
    ReturnRequestSerializer,
    RefundSerializer,
)


# ==========================================================
# Place Order API
# ==========================================================

class PlaceOrderAPIView(APIView):

    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request):

        try:

            address = get_object_or_404(
                Address,
                pk=request.data.get("shipping_address"),
                account=request.user,
            )

            cart = get_object_or_404(
                Cart,
                account=request.user,
            )

            if not cart.items.exists():

                return Response(
                    {
                        "message": "Cart is empty."
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            total_amount = 0

            for item in cart.items.select_related("variant"):

                inventory = get_object_or_404(
                    ProductInventory,
                    variant=item.variant,
                )

                if item.quantity > inventory.available_stock:

                    return Response(
                        {
                            "message": (
                                f"Insufficient stock for "
                                f"{item.variant.variant_name}"
                            )
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                total_amount += (
                    item.variant.price * item.quantity
                )

            order = Order.objects.create(
                account=request.user,
                shipping_address=address,
                order_number=f"ORD{random.randint(100000, 999999)}",
                total_amount=total_amount,
            )

            Notification.objects.create(
                account=request.user,
                title="Order Placed",
                message=(
                    f"Your order #{order.id} "
                    f"has been placed successfully."
                ),
                notification_type=(
                    Notification.NotificationType.ORDER
                ),
            )

            for item in cart.items.select_related("variant"):

                inventory = ProductInventory.objects.get(
                    variant=item.variant
                )

                OrderItem.objects.create(
                    order=order,
                    variant=item.variant,
                    quantity=item.quantity,
                    unit_price=item.variant.price,
                    total_price=(
                        item.variant.price * item.quantity
                    ),
                )

                inventory.stock_quantity -= item.quantity
                inventory.save()

            cart.items.all().delete()

            serializer = OrderSerializer(
                order,
                context={"request": request},
            )

            return Response(
                {
                    "message": "Order placed successfully.",
                    "data": serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )

        except Exception as e:

            transaction.set_rollback(True)

            return Response(
                {
                    "success": False,
                    "message": "Failed to place order.",
                    "error": str(e),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

# ==========================================================
# Order List API
# ==========================================================

class OrderListAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        orders = (
            Order.objects.filter(
                account=request.user
            )
            .prefetch_related(
                "items",
                "items__variant",
                "items__variant__product",
                "status_history",
            )
            .order_by("-created_at")
        )

        serializer = OrderSerializer(
            orders,
            many=True,
            context={
                "request": request
            },
        )

        return Response(
            {
                "message": "Orders fetched successfully.",
                "count": orders.count(),
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


# ==========================================================
# Order Detail API
# ==========================================================

class OrderDetailAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, pk):

        order = get_object_or_404(
            Order.objects.prefetch_related(
                "items",
                "items__variant",
                "items__variant__product",
                "status_history",
            ),
            pk=pk,
            account=request.user,
        )

        serializer = OrderSerializer(
            order,
            context={
                "request": request
            },
        )

        return Response(
            {
                "message": "Order fetched successfully.",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

# ==========================================================
# Cancel Order API
# ==========================================================

class CancelOrderAPIView(APIView):

    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def put(self, request, pk):

        try:

            order = get_object_or_404(
                Order.objects.prefetch_related(
                    "items",
                    "items__variant",
                ),
                pk=pk,
                account=request.user,
            )

            if order.status in [

                Order.OrderStatus.SHIPPED,

                Order.OrderStatus.OUT_FOR_DELIVERY,

                Order.OrderStatus.DELIVERED,

            ]:

                return Response(
                    {
                        "message": (
                            "Order cannot be cancelled "
                            "after shipment."
                        )
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if order.status == Order.OrderStatus.CANCELLED:

                return Response(
                    {
                        "message": "Order is already cancelled."
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            for item in order.items.all():

                inventory = get_object_or_404(
                    ProductInventory,
                    variant=item.variant,
                )

                inventory.stock_quantity += item.quantity

                inventory.save(
                    update_fields=[
                        "stock_quantity",
                    ]
                )

            order.status = Order.OrderStatus.CANCELLED

            order.save(
                update_fields=[
                    "status",
                ]
            )

            serializer = OrderSerializer(
                order,
                context={
                    "request": request,
                },
            )

            return Response(
                {
                    "message": "Order cancelled successfully.",
                    "data": serializer.data,
                },
                status=status.HTTP_200_OK,
            )

        except Exception as e:

            transaction.set_rollback(True)

            return Response(
                {
                    "success": False,
                    "message": "Failed to cancel order.",
                    "error": str(e),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

# ==========================================================
# Return Request API
# ==========================================================

class ReturnRequestAPIView(APIView):

    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request, order_id):

        try:

            order = get_object_or_404(
                Order.objects.prefetch_related(
                    "returns",
                ),
                id=order_id,
                account=request.user,
            )

            if order.status != Order.OrderStatus.DELIVERED:

                return Response(
                    {
                        "message": (
                            "Only delivered orders "
                            "can be returned."
                        )
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if ReturnRequest.objects.filter(
                order=order
            ).exists():

                return Response(
                    {
                        "message":
                        "Return request already exists."
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            serializer = ReturnRequestSerializer(
                data=request.data,
                context={
                    "request": request,
                },
            )

            serializer.is_valid(
                raise_exception=True
            )

            return_request = serializer.save(
                order=order,
            )

            return Response(
                {
                    "message":
                    "Return request submitted successfully.",
                    "data": ReturnRequestSerializer(
                        return_request,
                        context={
                            "request": request,
                        },
                    ).data,
                },
                status=status.HTTP_201_CREATED,
            )

        except Exception as e:

            transaction.set_rollback(True)

            return Response(
                {
                    "success": False,
                    "message":
                    "Failed to submit return request.",
                    "error": str(e),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

# ==========================================================
# Refund API
# ==========================================================

class RefundAPIView(APIView):

    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request, return_id):

        try:

            return_request = get_object_or_404(
                ReturnRequest.objects.select_related(
                    "order",
                    "order__account",
                ),
                id=return_id,
                order__account=request.user,
            )

            if (
                return_request.status
                != ReturnRequest.ReturnStatus.APPROVED
            ):

                return Response(
                    {
                        "message": (
                            "Return request is not approved."
                        )
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if hasattr(
                return_request,
                "refund",
            ):

                return Response(
                    {
                        "message":
                        "Refund already processed."
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            refund = Refund.objects.create(
                return_request=return_request,
                amount=return_request.order.total_amount,
                status=Refund.RefundStatus.COMPLETED,
                refunded_at=timezone.now(),
            )

            Notification.objects.create(
                account=refund.return_request.order.account,
                title="Refund Processed",
                message=(
                    "Your refund has been "
                    "processed successfully."
                ),
                notification_type=(
                    Notification.NotificationType.REFUND
                ),
            )

            serializer = RefundSerializer(
                refund,
                context={
                    "request": request,
                },
            )

            return Response(
                {
                    "message":
                    "Refund processed successfully.",
                    "data": serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )

        except Exception as e:

            transaction.set_rollback(True)

            return Response(
                {
                    "success": False,
                    "message":
                    "Failed to process refund.",
                    "error": str(e),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

# ==========================================================
# Seller Order Detail API
# ==========================================================

class SellerOrderDetailAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, order_id):

        try:

            if not hasattr(request.user, "seller_profile"):

                return Response(
                    {
                        "message": "Seller profile not found."
                    },
                    status=status.HTTP_404_NOT_FOUND,
                )

            order = get_object_or_404(
                Order.objects.prefetch_related(
                    "items",
                    "items__variant",
                    "items__variant__product",
                    "status_history",
                ),
                id=order_id,
                items__variant__product__seller=request.user.seller_profile,
            )

            serializer = OrderSerializer(
                order,
                context={
                    "request": request,
                },
            )

            return Response(
                {
                    "message": "Order fetched successfully.",
                    "data": serializer.data,
                },
                status=status.HTTP_200_OK,
            )

        except Exception as e:

            return Response(
                {
                    "success": False,
                    "message": "Failed to fetch order.",
                    "error": str(e),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )