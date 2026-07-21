from django.urls import path

from .views import (
    WishlistCreateAPIView,
    WishlistListAPIView,
    WishlistDetailAPIView,
    WishlistDeleteAPIView,
    WishlistClearAPIView,
)

urlpatterns = [
    path("", WishlistCreateAPIView.as_view(), name="wishlist-create"),
    path("list/", WishlistListAPIView.as_view(), name="wishlist-list"),
    path("<int:pk>/", WishlistDetailAPIView.as_view(), name="wishlist-detail"),
    path("<int:pk>/delete/", WishlistDeleteAPIView.as_view(), name="wishlist-delete"),
    path("clear/", WishlistClearAPIView.as_view(), name="wishlist-clear"),
]