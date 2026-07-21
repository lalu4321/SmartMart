from django.urls import path

from .views import (
    PaymentCreateAPIView,
    PaymentListAPIView,
    PaymentDetailAPIView,
)

urlpatterns = [

    path(
        "<int:order_id>/",
        PaymentCreateAPIView.as_view(),
        name="payment-create",
    ),

    path(
        "",
        PaymentListAPIView.as_view(),
        name="payment-list",
    ),

    path(
        "<int:pk>/detail/",
        PaymentDetailAPIView.as_view(),
        name="payment-detail",
    ),
]