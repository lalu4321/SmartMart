from django.urls import path

from .views import (
    ReviewCreateAPIView,
    ReviewListAPIView,
    ReviewDetailAPIView,
    ReviewUpdateAPIView,
    ReviewDeleteAPIView,
)

urlpatterns = [
    
    path("", ReviewCreateAPIView.as_view(), name="review-create"),
    path("product/<int:product_id>/", ReviewListAPIView.as_view(), name="review-list"),
    path("<int:pk>/", ReviewDetailAPIView.as_view(), name="review-detail"),
    path("<int:pk>/update/", ReviewUpdateAPIView.as_view(), name="review-update"),
    path("<int:pk>/delete/", ReviewDeleteAPIView.as_view(), name="review-delete"),
]