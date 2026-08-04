from django.urls import path

from .views import (
    AdminDashboardAPIView,
    AdminProfileAPIView,
    ChangePasswordAPIView,
    UpdateProfileImageAPIView,
)

urlpatterns = [

    path(
        "dashboard/",
        AdminDashboardAPIView.as_view(),
        name="admin-dashboard",
    ),

    path(
        "profile/",
        AdminProfileAPIView.as_view(),
        name="admin-profile",
    ),

    path(
        "change-password/",
        ChangePasswordAPIView.as_view(),
        name="change-password",
    ),

    path(
        "profile-image/",
        UpdateProfileImageAPIView.as_view(),
        name="profile-image",
    ),

]