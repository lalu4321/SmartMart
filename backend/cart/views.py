from django.shortcuts import get_object_or_404
from django.http import Http404
from rest_framework.exceptions import ValidationError

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import Cart, CartItem
from .serializers import CartSerializer

from products.models import (
    ProductVariant,
    ProductInventory,
)

class AddToCartAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        try:

            variant = get_object_or_404(
                ProductVariant,
                pk=request.data.get("variant")
            )

            quantity = int(
                request.data.get("quantity", 1)
            )

            if quantity <= 0:
                return Response(
                    {
                        "message": "Quantity must be greater than zero."
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            inventory = get_object_or_404(
                ProductInventory,
                variant=variant
            )

            if quantity > inventory.available_stock:
                return Response(
                    {
                        "message": "Insufficient stock."
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            cart, created = Cart.objects.get_or_create(
                account=request.user
            )

            cart_item, created = CartItem.objects.get_or_create(
                cart=cart,
                variant=variant,
                defaults={
                    "quantity": quantity
                }
            )

            if not created:

                new_quantity = (
                    cart_item.quantity + quantity
                )

                if new_quantity > inventory.available_stock:
                    return Response(
                        {
                            "message": "Insufficient stock."
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )

                cart_item.quantity = new_quantity
                cart_item.save()

            serializer = CartSerializer(cart)

            return Response(
                {
                    "message": "Product added to cart successfully.",
                    "data": serializer.data
                },
                status=status.HTTP_200_OK
            )

        except Exception as e:

            return Response(
                {
                    "success": False,
                    "message": "Failed to add product to cart.",
                    "error": str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
class ViewCartAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        cart = get_object_or_404(
            Cart,
            account=request.user
        )

        serializer = CartSerializer(cart)

        return Response(
            {
                "message": "Cart fetched successfully.",
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )

class UpdateCartItemAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def put(self, request, pk):

        try:

            cart_item = get_object_or_404(
                CartItem,
                pk=pk
            )

            if cart_item.cart.account != request.user:
                return Response(
                    {
                        "message": "You can update only your own cart."
                    },
                    status=status.HTTP_403_FORBIDDEN
                )

            try:
                quantity = int(
                    request.data.get("quantity", 1)
                )
            except (TypeError, ValueError):
                return Response(
                    {
                        "message": "Quantity must be a valid integer."
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            inventory = get_object_or_404(
                ProductInventory,
                variant=cart_item.variant
            )

            if quantity > inventory.available_stock:
                return Response(
                    {
                        "message": "Insufficient stock."
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            cart_item.quantity = quantity
            cart_item.save()

            serializer = CartSerializer(cart_item.cart)

            return Response(
                {
                    "message": "Cart item updated successfully.",
                    "data": serializer.data
                },
                status=status.HTTP_200_OK
            )

        except Exception as e:

            return Response(
                {
                    "success": False,
                    "message": "Failed to update cart item.",
                    "error": str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
class RemoveCartItemAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):

        try:

            cart_item = get_object_or_404(
                CartItem,
                pk=pk
            )

            if cart_item.cart.account != request.user:
                return Response(
                    {
                        "message": "You can delete only your own cart items."
                    },
                    status=status.HTTP_403_FORBIDDEN
                )

            cart_item.delete()

            return Response(
                {
                    "message": "Cart item removed successfully."
                },
                status=status.HTTP_200_OK
            )

        except Exception as e:

            return Response(
                {
                    "success": False,
                    "message": "Failed to remove cart item.",
                    "error": str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class ClearCartAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def delete(self, request):

        try:

            cart = get_object_or_404(
                Cart,
                account=request.user
            )

            cart.items.all().delete()

            return Response(
                {
                    "message": "Cart cleared successfully."
                },
                status=status.HTTP_200_OK
            )

        except Exception as e:

            return Response(
                {
                    "success": False,
                    "message": "Failed to clear cart.",
                    "error": str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )