from django.urls import path

from .views import (
    AdminDashboardAPIView,
    AdminProfileAPIView,
    ChangePasswordAPIView,
    UpdateProfileImageAPIView,
)

urlpatterns = [

    # ==================================
    # Admin Dashboard API
    # ==================================

    path("dashboard/", AdminDashboardAPIView.as_view(), name="admin-dashboard"),

    # ==================================
    # Admin Profile APIs
    # ==================================

    path("profile/", AdminProfileAPIView.as_view(), name="admin-profile"),
    path("change-password/", ChangePasswordAPIView.as_view(), name="change-password"),
    path("profile-image/", UpdateProfileImageAPIView.as_view(), name="profile-image"),
]