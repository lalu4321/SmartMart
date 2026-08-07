from django.urls import path

from .views import (
    AddToCartAPIView,
    ViewCartAPIView,
    UpdateCartItemAPIView,
    RemoveCartItemAPIView,
    ClearCartAPIView,
)

urlpatterns = [

    # ==================================
    # Cart APIs
    # ==================================

    path("add/", AddToCartAPIView.as_view(), name="cart-add"),
    path("view/", ViewCartAPIView.as_view(), name="cart-view"),
    path("item/<int:pk>/update/", UpdateCartItemAPIView.as_view(), name="cart-item-update"),
    path("item/<int:pk>/delete/", RemoveCartItemAPIView.as_view(), name="cart-item-delete"),
    path("clear/", ClearCartAPIView.as_view(), name="cart-clear"),
]