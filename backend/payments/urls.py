from django.urls import path

from .views import (
    PaymentCreateAPIView,
    PaymentListAPIView,
    PaymentDetailAPIView,
    PaymentConfirmAPIView,
)

from .admin_payment_views import (
    AdminPaymentListAPIView,
    AdminPaymentDetailAPIView,
    AdminPaymentStatusAPIView,
)

urlpatterns = [

    # ==================================
    # Customer Payment APIs
    # ==================================

    path("<int:order_id>/", PaymentCreateAPIView.as_view(), name="payment-create"),
    path("", PaymentListAPIView.as_view(), name="payment-list"),
    path("<int:pk>/detail/", PaymentDetailAPIView.as_view(), name="payment-detail"),
    path("<int:pk>/confirm/", PaymentConfirmAPIView.as_view(), name="payment-confirm"),

    # ==================================
    # Admin Payment APIs
    # ==================================

    path("admin/list/", AdminPaymentListAPIView.as_view(), name="admin-payment-list"),
    path("admin/<int:pk>/", AdminPaymentDetailAPIView.as_view(), name="admin-payment-detail"),
    path("admin/<int:pk>/status/", AdminPaymentStatusAPIView.as_view(), name="admin-payment-status"),
]