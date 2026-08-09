from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import (
    Notification,
)

from .serializers import (
    NotificationSerializer,
)


# ==========================================================
# Notification List API
# ==========================================================

class NotificationListAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        notifications = (
            Notification.objects
            .filter(
                account=request.user,
            )
            .order_by(
                "-created_at",
            )
        )

        serializer = NotificationSerializer(
            notifications,
            many=True,
            context={
                "request": request,
            },
        )

        return Response(
            {
                "message":
                "Notifications fetched successfully.",
                "count":
                notifications.count(),
                "data":
                serializer.data,
            },
            status=status.HTTP_200_OK,
        )

# ==========================================================
# Notification Detail API
# ==========================================================

class NotificationDetailAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, pk):

        notification = get_object_or_404(
            Notification,
            pk=pk,
            account=request.user,
        )

        serializer = NotificationSerializer(
            notification,
            context={
                "request": request,
            },
        )

        return Response(
            {
                "message":
                "Notification fetched successfully.",
                "data":
                serializer.data,
            },
            status=status.HTTP_200_OK,
        )


# ==========================================================
# Mark Notification As Read API
# ==========================================================

class NotificationMarkAsReadAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def put(self, request, pk):

        notification = get_object_or_404(
            Notification,
            pk=pk,
            account=request.user,
        )

        notification.is_read = True

        notification.save(
            update_fields=[
                "is_read",
            ]
        )

        return Response(
            {
                "message":
                "Notification marked as read."
            },
            status=status.HTTP_200_OK,
        )

# ==========================================================
# Mark All Notifications As Read API
# ==========================================================

class NotificationMarkAllAsReadAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def put(self, request):

        Notification.objects.filter(
            account=request.user,
            is_read=False,
        ).update(
            is_read=True,
        )

        return Response(
            {
                "message":
                "All notifications marked as read."
            },
            status=status.HTTP_200_OK,
        )


# ==========================================================
# Delete Notification API
# ==========================================================

class NotificationDeleteAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):

        try:

            notification = get_object_or_404(
                Notification,
                pk=pk,
                account=request.user,
            )

            notification.delete()

            return Response(
                {
                    "message":
                    "Notification deleted successfully."
                },
                status=status.HTTP_200_OK,
            )

        except ValidationError:

            raise

        except Exception as e:

            return Response(
                {
                    "success": False,
                    "message":
                    "Failed to delete notification.",
                    "error": str(e),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )