from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from orders.models import OrderItem
from products.models import Product

from .models import (
    Review,
)

from .serializers import (
    ReviewSerializer,
)


# ==========================================================
# Review Create API
# ==========================================================

class ReviewCreateAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        try:

            serializer = ReviewSerializer(
                data=request.data,
                context={
                    "request": request,
                },
            )

            serializer.is_valid(
                raise_exception=True,
            )

            product = serializer.validated_data["product"]

            purchased = OrderItem.objects.filter(
                order__account=request.user,
                order__status="DELIVERED",
                variant__product=product,
            ).exists()

            if not purchased:

                return Response(
                    {
                        "message": (
                            "You can review only delivered "
                            "products you have purchased."
                        )
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if Review.objects.filter(
                account=request.user,
                product=product,
            ).exists():

                return Response(
                    {
                        "message":
                        "You have already reviewed this product."
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            review = serializer.save(
                account=request.user,
            )

            return Response(
                {
                    "message":
                    "Review added successfully.",
                    "data": ReviewSerializer(
                        review,
                        context={
                            "request": request,
                        },
                    ).data,
                },
                status=status.HTTP_201_CREATED,
            )

        except Exception as e:

            return Response(
                {
                    "success": False,
                    "message":
                    "Failed to add review.",
                    "error": str(e),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

# ==========================================================
# Review List API
# ==========================================================

class ReviewListAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, product_id):

        product = get_object_or_404(
            Product,
            pk=product_id,
        )

        reviews = (
            Review.objects
            .select_related(
                "account",
                "product",
            )
            .filter(
                product=product,
            )
            .order_by("-created_at")
        )

        serializer = ReviewSerializer(
            reviews,
            many=True,
            context={
                "request": request,
            },
        )

        return Response(
            {
                "message":
                "Reviews fetched successfully.",
                "count": reviews.count(),
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


# ==========================================================
# Review Detail API
# ==========================================================

class ReviewDetailAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, pk):

        review = get_object_or_404(
            Review.objects.select_related(
                "account",
                "product",
            ),
            pk=pk,
        )

        serializer = ReviewSerializer(
            review,
            context={
                "request": request,
            },
        )

        return Response(
            {
                "message":
                "Review fetched successfully.",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

# ==========================================================
# Review Update API
# ==========================================================

class ReviewUpdateAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def put(self, request, pk):

        try:

            review = get_object_or_404(
                Review,
                pk=pk,
                account=request.user,
            )

            serializer = ReviewSerializer(
                review,
                data=request.data,
                partial=True,
                context={
                    "request": request,
                },
            )

            serializer.is_valid(
                raise_exception=True,
            )

            serializer.save()

            return Response(
                {
                    "message":
                    "Review updated successfully.",
                    "data": serializer.data,
                },
                status=status.HTTP_200_OK,
            )

        except Exception as e:

            return Response(
                {
                    "success": False,
                    "message":
                    "Failed to update review.",
                    "error": str(e),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

# ==========================================================
# Review Delete API
# ==========================================================

class ReviewDeleteAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):

        try:

            review = get_object_or_404(
                Review,
                pk=pk,
                account=request.user,
            )

            review.delete()

            return Response(
                {
                    "message":
                    "Review deleted successfully."
                },
                status=status.HTTP_200_OK,
            )

        except Exception as e:

            return Response(
                {
                    "success": False,
                    "message":
                    "Failed to delete review.",
                    "error": str(e),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )