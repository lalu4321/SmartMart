from django.urls import path

from .views import (
    CouponCreateAPIView,
    CouponListAPIView,
    CouponDetailAPIView,
    CouponUpdateAPIView,
    CouponDeleteAPIView,
    ApplyCouponAPIView,
)

urlpatterns = [
    path("", CouponCreateAPIView.as_view(), name="coupon-create"),
    path("list/", CouponListAPIView.as_view(), name="coupon-list"),
    path("<int:pk>/", CouponDetailAPIView.as_view(), name="coupon-detail"),
    path("<int:pk>/update/", CouponUpdateAPIView.as_view(), name="coupon-update"),
    path("<int:pk>/delete/", CouponDeleteAPIView.as_view(), name="coupon-delete"),
    path("apply/", ApplyCouponAPIView.as_view(), name="apply-coupon"),
]