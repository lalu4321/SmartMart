from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from .models import ContactMessage
from .serializers import ContactMessageSerializer


# ==========================================
# Submit Contact Message
# ==========================================

class ContactCreateAPIView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):

        serializer = ContactMessageSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        serializer.save()

        return Response(
            {
                "message": "Message sent successfully.",
                "data": serializer.data,
            },
            status=status.HTTP_201_CREATED,
        )


# ==========================================
# Contact Detail
# ==========================================

class ContactDetailAPIView(APIView):

    permission_classes = [AllowAny]

    def get(self, request, pk):

        contact = get_object_or_404(
            ContactMessage,
            pk=pk
        )

        serializer = ContactMessageSerializer(
            contact
        )

        return Response(
            {
                "message": "Contact message fetched successfully.",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )