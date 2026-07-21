from django.urls import path

from .views import (
    NotificationListAPIView,
    NotificationDetailAPIView,
    NotificationMarkAsReadAPIView,
    NotificationMarkAllAsReadAPIView,
    NotificationDeleteAPIView,
)

urlpatterns = [
    path("", NotificationListAPIView.as_view(), name="notification-list"),
    path("<int:pk>/", NotificationDetailAPIView.as_view(), name="notification-detail"),
    path("<int:pk>/read/", NotificationMarkAsReadAPIView.as_view(), name="notification-read"),
    path("read-all/", NotificationMarkAllAsReadAPIView.as_view(), name="notification-read-all"),
    path("<int:pk>/delete/", NotificationDeleteAPIView.as_view(), name="notification-delete"),
]