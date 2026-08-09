from django.urls import path

from .views import (
    CouponCreateAPIView,
    CouponListAPIView,
    CouponDetailAPIView,
    CouponUpdateAPIView,
    CouponDeleteAPIView,
    ApplyCouponAPIView,
)

from .admin_coupon_views import (
    AdminCouponListAPIView,
    AdminCouponDetailAPIView,
    AdminCouponCreateAPIView,
    AdminCouponUpdateAPIView,
    AdminCouponDeleteAPIView,
    AdminCouponStatusAPIView,
)

urlpatterns = [

    # ==================================
    # Customer Coupon APIs
    # ==================================

    path("", CouponCreateAPIView.as_view(), name="coupon-create"),
    path("list/", CouponListAPIView.as_view(), name="coupon-list"),
    path("<int:pk>/", CouponDetailAPIView.as_view(), name="coupon-detail"),
    path("<int:pk>/update/", CouponUpdateAPIView.as_view(), name="coupon-update"),
    path("<int:pk>/delete/", CouponDeleteAPIView.as_view(), name="coupon-delete"),
    path("apply/", ApplyCouponAPIView.as_view(), name="apply-coupon"),

    # ==================================
    # Admin Coupon APIs
    # ==================================

    path("admin/list/", AdminCouponListAPIView.as_view(), name="admin-coupon-list"),
    path("admin/create/", AdminCouponCreateAPIView.as_view(), name="admin-coupon-create"),
    path("admin/<int:pk>/", AdminCouponDetailAPIView.as_view(), name="admin-coupon-detail"),
    path("admin/<int:pk>/update/", AdminCouponUpdateAPIView.as_view(), name="admin-coupon-update"),
    path("admin/<int:pk>/delete/", AdminCouponDeleteAPIView.as_view(), name="admin-coupon-delete"),
    path("admin/<int:pk>/status/", AdminCouponStatusAPIView.as_view(), name="admin-coupon-status"),
]