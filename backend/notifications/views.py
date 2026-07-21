from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import Notification
from .serializers import NotificationSerializer


class NotificationListAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        notifications = Notification.objects.filter(
            account=request.user
        )

        serializer = NotificationSerializer(
            notifications,
            many=True
        )

        return Response(
            {
                "message": "Notifications fetched successfully.",
                "count": notifications.count(),
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )
    
class NotificationDetailAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, pk):

        notification = get_object_or_404(
            Notification,
            pk=pk,
            account=request.user
        )

        serializer = NotificationSerializer(
            notification
        )

        return Response(
            {
                "message": "Notification fetched successfully.",
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )
    
class NotificationMarkAsReadAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def put(self, request, pk):

        notification = get_object_or_404(
            Notification,
            pk=pk,
            account=request.user
        )

        notification.is_read = True
        notification.save(update_fields=["is_read"])

        return Response(
            {
                "message": "Notification marked as read."
            },
            status=status.HTTP_200_OK
        )

class NotificationMarkAllAsReadAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def put(self, request):

        Notification.objects.filter(
            account=request.user,
            is_read=False
        ).update(
            is_read=True
        )

        return Response(
            {
                "message": "All notifications marked as read."
            },
            status=status.HTTP_200_OK
        )
    

class NotificationDeleteAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):

        try:
            notification = get_object_or_404(
                Notification,
                pk=pk,
                account=request.user
            )

            notification.delete()

            return Response(
                {
                    "message": "Notification deleted successfully."
                },
                status=status.HTTP_200_OK
            )

        except ValidationError:
            raise

        except Exception as e:
            return Response(
                {
                    "success": False,
                    "message": "Failed to delete notification.",
                    "error": str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )