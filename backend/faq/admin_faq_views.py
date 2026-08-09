from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import (
    FAQ,
)

from .admin_faq_serializers import (
    AdminFAQSerializer,
)


# ==========================================================
# Admin FAQ List API
# ==========================================================

class AdminFAQListAPIView(APIView):

    permission_classes = [IsAdminUser]

    def get(self, request):

        faqs = (
            FAQ.objects
            .all()
            .order_by(
                "-created_at",
            )
        )

        serializer = AdminFAQSerializer(
            faqs,
            many=True,
        )

        return Response(
            {
                "message":
                "FAQs fetched successfully.",
                "count":
                faqs.count(),
                "data":
                serializer.data,
            },
            status=status.HTTP_200_OK,
        )

# ==========================================================
# Admin FAQ Detail API
# ==========================================================

class AdminFAQDetailAPIView(APIView):

    permission_classes = [IsAdminUser]

    def get(self, request, pk):

        faq = get_object_or_404(
            FAQ,
            pk=pk,
        )

        serializer = AdminFAQSerializer(
            faq,
        )

        return Response(
            {
                "message":
                "FAQ fetched successfully.",
                "data":
                serializer.data,
            },
            status=status.HTTP_200_OK,
        )


# ==========================================================
# Admin FAQ Create API
# ==========================================================

class AdminFAQCreateAPIView(APIView):

    permission_classes = [IsAdminUser]

    def post(self, request):

        serializer = AdminFAQSerializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        serializer.save()

        return Response(
            {
                "message":
                "FAQ created successfully.",
                "data":
                serializer.data,
            },
            status=status.HTTP_201_CREATED,
        )

# ==========================================================
# Admin FAQ Update API
# ==========================================================

class AdminFAQUpdateAPIView(APIView):

    permission_classes = [IsAdminUser]

    def put(self, request, pk):

        faq = get_object_or_404(
            FAQ,
            pk=pk,
        )

        serializer = AdminFAQSerializer(
            faq,
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
                "FAQ updated successfully.",
                "data":
                serializer.data,
            },
            status=status.HTTP_200_OK,
        )


# ==========================================================
# Admin FAQ Delete API
# ==========================================================

class AdminFAQDeleteAPIView(APIView):

    permission_classes = [IsAdminUser]

    def delete(self, request, pk):

        faq = get_object_or_404(
            FAQ,
            pk=pk,
        )

        faq.delete()

        return Response(
            {
                "message":
                "FAQ deleted successfully."
            },
            status=status.HTTP_200_OK,
        )