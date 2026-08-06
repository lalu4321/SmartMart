from django.urls import path

from .views import (
    NotificationListAPIView,
    NotificationDetailAPIView,
    NotificationMarkAsReadAPIView,
    NotificationMarkAllAsReadAPIView,
    NotificationDeleteAPIView,
)

from .admin_notification_views import (
    AdminNotificationListAPIView,
    AdminNotificationDetailAPIView,
    AdminNotificationCreateAPIView,
    AdminNotificationStatusAPIView,
    AdminNotificationDeleteAPIView,
)

urlpatterns = [

    # ==================================
    # Customer Notification APIs
    # ==================================

    path("", NotificationListAPIView.as_view(), name="notification-list"),
    path("<int:pk>/", NotificationDetailAPIView.as_view(), name="notification-detail"),
    path("<int:pk>/read/", NotificationMarkAsReadAPIView.as_view(), name="notification-read"),
    path("read-all/", NotificationMarkAllAsReadAPIView.as_view(), name="notification-read-all"),
    path("<int:pk>/delete/", NotificationDeleteAPIView.as_view(), name="notification-delete"),

    # ==================================
    # Admin Notification APIs
    # ==================================

    path("admin/list/", AdminNotificationListAPIView.as_view(), name="admin-notification-list"),
    path("admin/<int:pk>/", AdminNotificationDetailAPIView.as_view(), name="admin-notification-detail"),
    path("admin/create/", AdminNotificationCreateAPIView.as_view(), name="admin-notification-create"),
    path("admin/<int:pk>/status/", AdminNotificationStatusAPIView.as_view(), name="admin-notification-status"),
    path("admin/<int:pk>/delete/", AdminNotificationDeleteAPIView.as_view(), name="admin-notification-delete"),
]