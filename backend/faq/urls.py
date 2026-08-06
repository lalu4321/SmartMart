from django.urls import path

from .views import (
    FAQListAPIView,
    FAQDetailAPIView,
)

from .admin_faq_views import (
    AdminFAQListAPIView,
    AdminFAQDetailAPIView,
    AdminFAQCreateAPIView,
    AdminFAQUpdateAPIView,
    AdminFAQDeleteAPIView,
)

urlpatterns = [

    # ==================================
    # Public FAQ APIs
    # ==================================

    path("", FAQListAPIView.as_view(), name="faq-list"),
    path("<int:pk>/", FAQDetailAPIView.as_view(), name="faq-detail"),

    # ==================================
    # Admin FAQ APIs
    # ==================================

    path("admin/list/", AdminFAQListAPIView.as_view(), name="admin-faq-list"),
    path("admin/<int:pk>/", AdminFAQDetailAPIView.as_view(), name="admin-faq-detail"),
    path("admin/create/", AdminFAQCreateAPIView.as_view(), name="admin-faq-create"),
    path("admin/<int:pk>/update/", AdminFAQUpdateAPIView.as_view(), name="admin-faq-update"),
    path("admin/<int:pk>/delete/", AdminFAQDeleteAPIView.as_view(), name="admin-faq-delete"),
]