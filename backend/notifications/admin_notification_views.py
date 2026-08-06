from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework import status

from accounts.models import Account

from .models import Notification
from .admin_notification_serializers import (
    AdminNotificationSerializer,
)


# ==========================================
# Admin Notification List
# ==========================================

class AdminNotificationListAPIView(APIView):

    permission_classes = [IsAdminUser]

    def get(self, request):

        notifications = Notification.objects.select_related(
            "account"
        )

        serializer = AdminNotificationSerializer(
            notifications,
            many=True
        )

        return Response(
            {
                "message": "Notifications fetched successfully.",
                "count": notifications.count(),
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


# ==========================================
# Admin Notification Detail
# ==========================================

class AdminNotificationDetailAPIView(APIView):

    permission_classes = [IsAdminUser]

    def get(self, request, pk):

        notification = get_object_or_404(
            Notification,
            pk=pk
        )

        serializer = AdminNotificationSerializer(
            notification
        )

        return Response(
            {
                "message": "Notification fetched successfully.",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


# ==========================================
# Admin Send Notification
# ==========================================

class AdminNotificationCreateAPIView(APIView):

    permission_classes = [IsAdminUser]

    def post(self, request):

        account = get_object_or_404(
            Account,
            pk=request.data.get("account")
        )

        serializer = AdminNotificationSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        serializer.save(
            account=account
        )

        return Response(
            {
                "message": "Notification sent successfully.",
                "data": serializer.data,
            },
            status=status.HTTP_201_CREATED,
        )


# ==========================================
# Admin Mark Read / Unread
# ==========================================

class AdminNotificationStatusAPIView(APIView):

    permission_classes = [IsAdminUser]

    def patch(self, request, pk):

        notification = get_object_or_404(
            Notification,
            pk=pk
        )

        notification.is_read = (
            not notification.is_read
        )

        notification.save(
            update_fields=["is_read"]
        )

        return Response(
            {
                "message": (
                    "Notification marked as read."
                    if notification.is_read
                    else
                    "Notification marked as unread."
                ),
                "data": {
                    "id": notification.id,
                    "is_read": notification.is_read,
                },
            },
            status=status.HTTP_200_OK,
        )


# ==========================================
# Admin Delete Notification
# ==========================================

class AdminNotificationDeleteAPIView(APIView):

    permission_classes = [IsAdminUser]

    def delete(self, request, pk):

        notification = get_object_or_404(
            Notification,
            pk=pk
        )

        notification.delete()

        return Response(
            {
                "message": "Notification deleted successfully."
            },
            status=status.HTTP_200_OK,
        )