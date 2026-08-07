from django.db.models import Q
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import (
    Review,
)

from .admin_review_serializers import (
    AdminReviewSerializer,
)


# ==========================================================
# Admin Review List API
# ==========================================================

class AdminReviewListAPIView(APIView):

    permission_classes = [IsAdminUser]

    def get(self, request):

        reviews = (
            Review.objects
            .select_related(
                "account",
                "product",
            )
        )

        search = request.query_params.get("search")

        if search:

            reviews = reviews.filter(

                Q(product__name__icontains=search)

                | Q(account__username__icontains=search)

                | Q(account__email__icontains=search)

                | Q(review__icontains=search)

            )

        rating = request.query_params.get("rating")

        if rating:

            reviews = reviews.filter(
                rating=rating,
            )

        reviews = reviews.order_by(
            "-created_at",
        )

        serializer = AdminReviewSerializer(
            reviews,
            many=True,
        )

        return Response(
            {
                "message": "Reviews fetched successfully.",
                "count": reviews.count(),
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


# ==========================================================
# Admin Review Detail API
# ==========================================================

class AdminReviewDetailAPIView(APIView):

    permission_classes = [IsAdminUser]

    def get(self, request, pk):

        review = get_object_or_404(
            Review.objects.select_related(
                "account",
                "product",
            ),
            pk=pk,
        )

        serializer = AdminReviewSerializer(
            review,
        )

        return Response(
            {
                "message": "Review fetched successfully.",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


# ==========================================================
# Admin Review Delete API
# ==========================================================

class AdminReviewDeleteAPIView(APIView):

    permission_classes = [IsAdminUser]

    def delete(self, request, pk):

        try:

            review = get_object_or_404(
                Review,
                pk=pk,
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