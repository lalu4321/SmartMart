from django.urls import path

from .views import (
    ContactCreateAPIView,
    ContactDetailAPIView,
)

from .admin_contact_views import (
    AdminContactListAPIView,
    AdminContactDetailAPIView,
    AdminContactReadAPIView,
    AdminContactDeleteAPIView,
)

urlpatterns = [

    # ==================================
    # Public Contact APIs
    # ==================================

    path("", ContactCreateAPIView.as_view(), name="contact-create"),
    path("<int:pk>/", ContactDetailAPIView.as_view(), name="contact-detail"),

    # ==================================
    # Admin Contact APIs
    # ==================================

    path("admin/list/", AdminContactListAPIView.as_view(), name="admin-contact-list"),
    path("admin/<int:pk>/", AdminContactDetailAPIView.as_view(), name="admin-contact-detail"),
    path("admin/<int:pk>/read/", AdminContactReadAPIView.as_view(), name="admin-contact-read"),
    path("admin/<int:pk>/delete/", AdminContactDeleteAPIView.as_view(), name="admin-contact-delete"),
]