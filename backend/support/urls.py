from django.urls import path

from .views import (
    SupportTicketCreateAPIView,
    SupportTicketListAPIView,
    SupportTicketDetailAPIView,
    SupportTicketUpdateAPIView,
    SupportTicketCloseAPIView,
    AdminSupportTicketListAPIView,
    AdminSupportTicketDetailAPIView,
    TicketReplyAPIView,
    UpdateTicketStatusAPIView,
)

urlpatterns = [
    # Customer APIs
    path("", SupportTicketCreateAPIView.as_view(), name="support-create"),
    path("list/", SupportTicketListAPIView.as_view(), name="support-list"),
    path("<int:pk>/", SupportTicketDetailAPIView.as_view(), name="support-detail"),
    path("<int:pk>/update/", SupportTicketUpdateAPIView.as_view(), name="support-update"),
    path("<int:pk>/close/", SupportTicketCloseAPIView.as_view(), name="support-close"),

    # Admin APIs
    path("admin/", AdminSupportTicketListAPIView.as_view(), name="admin-support-list"),
    path("admin/<int:pk>/", AdminSupportTicketDetailAPIView.as_view(), name="admin-support-detail"),
    path("admin/<int:pk>/reply/", TicketReplyAPIView.as_view(), name="ticket-reply"),
    path("admin/<int:pk>/status/", UpdateTicketStatusAPIView.as_view(), name="ticket-status"),
]