from django.urls import path

from .views import (
    PlaceOrderAPIView,
    OrderListAPIView,
    OrderDetailAPIView,
    CancelOrderAPIView,
    ReturnRequestAPIView,
    RefundAPIView,
    SellerOrderDetailAPIView,
)

from .admin_order_views import (
    AdminOrderListAPIView,
    AdminOrderDetailAPIView,
    AdminOrderStatusAPIView,
    AdminOrderDeleteAPIView,
)

urlpatterns = [

    path("place/", PlaceOrderAPIView.as_view()),

    path("", OrderListAPIView.as_view()),

    path("<int:pk>/", OrderDetailAPIView.as_view()),

    path("<int:pk>/cancel/", CancelOrderAPIView.as_view()),

    path("<int:order_id>/return/", ReturnRequestAPIView.as_view(), name="return-request"),

    path("returns/<int:return_id>/refund/", RefundAPIView.as_view(), name="refund"),

    path("seller/<int:order_id>/",SellerOrderDetailAPIView.as_view(),name="seller-order-detail"),

    # ==========================
    # Admin Order APIs
    # ==========================

    path("admin/list/", AdminOrderListAPIView.as_view(), name="admin-order-list"),

    path("admin/<int:pk>/", AdminOrderDetailAPIView.as_view(), name="admin-order-detail"),

    path("admin/<int:pk>/status/", AdminOrderStatusAPIView.as_view(), name="admin-order-status"),
    
    path("admin/<int:pk>/delete/", AdminOrderDeleteAPIView.as_view(), name="admin-order-delete"),
]