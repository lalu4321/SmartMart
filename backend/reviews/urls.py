from django.urls import path

from .views import (
    ReviewCreateAPIView,
    ReviewListAPIView,
    ReviewDetailAPIView,
    ReviewUpdateAPIView,
    ReviewDeleteAPIView,
)

from .admin_review_views import (
    AdminReviewListAPIView,
    AdminReviewDetailAPIView,
    AdminReviewDeleteAPIView,
)

urlpatterns = [

    # ==================================
    # Review APIs
    # ==================================

    path("", ReviewCreateAPIView.as_view(), name="review-create"),
    path("product/<int:product_id>/", ReviewListAPIView.as_view(), name="review-list"),
    path("<int:pk>/", ReviewDetailAPIView.as_view(), name="review-detail"),
    path("<int:pk>/update/", ReviewUpdateAPIView.as_view(), name="review-update"),
    path("<int:pk>/delete/", ReviewDeleteAPIView.as_view(), name="review-delete"),

    # ==================================
    # Admin Review APIs
    # ==================================

    path("admin/list/", AdminReviewListAPIView.as_view(), name="admin-review-list"),
    path("admin/<int:pk>/", AdminReviewDetailAPIView.as_view(), name="admin-review-detail"),
    path("admin/<int:pk>/delete/", AdminReviewDeleteAPIView.as_view(), name="admin-review-delete"),
]