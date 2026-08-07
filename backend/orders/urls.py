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

from .admin_return_views import (
    AdminReturnListAPIView,
    AdminReturnDetailAPIView,
    AdminApproveReturnAPIView,
    AdminRejectReturnAPIView,
    AdminRefundListAPIView,
    AdminRefundDetailAPIView,
    AdminCompleteRefundAPIView,
)

urlpatterns = [

    # ==================================
    # Customer Order APIs
    # ==================================

    path("place/", PlaceOrderAPIView.as_view(), name="place-order"),
    path("", OrderListAPIView.as_view(), name="order-list"),
    path("<int:pk>/", OrderDetailAPIView.as_view(), name="order-detail"),
    path("<int:pk>/cancel/", CancelOrderAPIView.as_view(), name="cancel-order"),
    path("<int:order_id>/return/", ReturnRequestAPIView.as_view(), name="return-request"),
    path("returns/<int:return_id>/refund/", RefundAPIView.as_view(), name="refund"),
    path("seller/<int:order_id>/", SellerOrderDetailAPIView.as_view(), name="seller-order-detail"),

    # ==================================
    # Admin Order APIs
    # ==================================

    path("admin/list/", AdminOrderListAPIView.as_view(), name="admin-order-list"),
    path("admin/<int:pk>/", AdminOrderDetailAPIView.as_view(), name="admin-order-detail"),
    path("admin/<int:pk>/status/", AdminOrderStatusAPIView.as_view(), name="admin-order-status"),
    path("admin/<int:pk>/delete/", AdminOrderDeleteAPIView.as_view(), name="admin-order-delete"),

    # ==================================
    # Admin Return APIs
    # ==================================

    path("admin/returns/", AdminReturnListAPIView.as_view(), name="admin-return-list"),
    path("admin/returns/<int:pk>/", AdminReturnDetailAPIView.as_view(), name="admin-return-detail"),
    path("admin/returns/<int:pk>/approve/", AdminApproveReturnAPIView.as_view(), name="admin-return-approve"),
    path("admin/returns/<int:pk>/reject/", AdminRejectReturnAPIView.as_view(), name="admin-return-reject"),

    # ==================================
    # Admin Refund APIs
    # ==================================

    path("admin/refunds/", AdminRefundListAPIView.as_view(), name="admin-refund-list"),
    path("admin/refunds/<int:pk>/", AdminRefundDetailAPIView.as_view(), name="admin-refund-detail"),
    path("admin/refunds/<int:pk>/complete/", AdminCompleteRefundAPIView.as_view(), name="admin-refund-complete"),
]