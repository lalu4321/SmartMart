from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework import status

from .models import ContactMessage
from .admin_contact_serializers import AdminContactSerializer


# ==========================================
# Admin Contact List
# ==========================================

class AdminContactListAPIView(APIView):

    permission_classes = [IsAdminUser]

    def get(self, request):

        contacts = ContactMessage.objects.all()

        serializer = AdminContactSerializer(
            contacts,
            many=True
        )

        return Response(
            {
                "message": "Contact messages fetched successfully.",
                "count": contacts.count(),
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


# ==========================================
# Admin Contact Detail
# ==========================================

class AdminContactDetailAPIView(APIView):

    permission_classes = [IsAdminUser]

    def get(self, request, pk):

        contact = get_object_or_404(
            ContactMessage,
            pk=pk
        )

        serializer = AdminContactSerializer(contact)

        return Response(
            {
                "message": "Contact message fetched successfully.",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


# ==========================================
# Admin Mark as Read
# ==========================================

class AdminContactReadAPIView(APIView):

    permission_classes = [IsAdminUser]

    def patch(self, request, pk):

        contact = get_object_or_404(
            ContactMessage,
            pk=pk
        )

        contact.is_read = not contact.is_read

        contact.save(
            update_fields=["is_read"]
        )

        return Response(
            {
                "message": (
                    "Message marked as read."
                    if contact.is_read
                    else
                    "Message marked as unread."
                ),
                "data": {
                    "id": contact.id,
                    "is_read": contact.is_read,
                },
            },
            status=status.HTTP_200_OK,
        )


# ==========================================
# Admin Delete Contact
# ==========================================

class AdminContactDeleteAPIView(APIView):

    permission_classes = [IsAdminUser]

    def delete(self, request, pk):

        contact = get_object_or_404(
            ContactMessage,
            pk=pk
        )

        contact.delete()

        return Response(
            {
                "message": "Contact message deleted successfully."
            },
            status=status.HTTP_200_OK,
        )