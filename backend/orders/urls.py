from django.urls import path

from .views import (
    PlaceOrderAPIView,
    OrderListAPIView,
    OrderDetailAPIView,
    CancelOrderAPIView,
    ReturnRequestAPIView,
    RefundAPIView,
)

urlpatterns = [

    path("place/", PlaceOrderAPIView.as_view()),

    path("", OrderListAPIView.as_view()),

    path("<int:pk>/", OrderDetailAPIView.as_view()),

    path("<int:pk>/cancel/", CancelOrderAPIView.as_view()),

    path("<int:order_id>/return/", ReturnRequestAPIView.as_view(), name="return-request"),

    path("returns/<int:return_id>/refund/", RefundAPIView.as_view(), name="refund"),
]