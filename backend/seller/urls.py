from django.urls import path

from .views import (
    SellerOrderListAPIView,
    SellerOrderDetailAPIView,
    UpdateOrderStatusAPIView,
    SellerReturnListAPIView,
    ApproveReturnAPIView,
    RejectReturnAPIView,
    SellerDashboardAPIView
)

urlpatterns = [

    path("orders/",SellerOrderListAPIView.as_view(),name="seller-order-list"),

    path("orders/<int:pk>/",SellerOrderDetailAPIView.as_view(),name="seller-order-detail"),

    path("orders/<int:pk>/status/",UpdateOrderStatusAPIView.as_view(),name="seller-order-status"),

    path("returns/",SellerReturnListAPIView.as_view()),

    path("returns/<int:pk>/approve/",ApproveReturnAPIView.as_view()),

    path("returns/<int:pk>/reject/",RejectReturnAPIView.as_view()),

    path("dashboard/",SellerDashboardAPIView.as_view(),name="seller-dashboard"),
]