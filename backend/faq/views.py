from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import (
    FAQ,
)

from .serializers import (
    FAQSerializer,
)


# ==========================================================
# FAQ List API
# ==========================================================

class FAQListAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        faqs = (
            FAQ.objects
            .filter(
                is_active=True,
            )
            .order_by(
                "-created_at",
            )
        )

        serializer = FAQSerializer(
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
# FAQ Detail API
# ==========================================================

class FAQDetailAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, pk):

        faq = get_object_or_404(
            FAQ,
            pk=pk,
            is_active=True,
        )

        serializer = FAQSerializer(
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