from django.urls import path

from .views import (
    RegisterAPIView,
    ProfileAPIView,
    UpdateProfileAPIView,
    AddressCreateAPIView,
    AddressListAPIView,
    AddressDetailAPIView,
    AddressUpdateAPIView,
    AddressDeleteAPIView,
    SetDefaultAddressAPIView,
    SellerProfileCreateAPIView,
    SellerProfileAPIView,
    SellerProfileUpdateAPIView,
    SellerProfileDeleteAPIView,
)

urlpatterns = [
    # Account APIs
    path("register/", RegisterAPIView.as_view()),
    path("profile/", ProfileAPIView.as_view()),
    path("profile/update/", UpdateProfileAPIView.as_view()),

    # Address APIs
    path("address/", AddressCreateAPIView.as_view()),
    path("address/list/", AddressListAPIView.as_view()),
    path("address/<int:pk>/", AddressDetailAPIView.as_view()),
    path("address/<int:pk>/update/", AddressUpdateAPIView.as_view()),
    path("address/<int:pk>/delete/", AddressDeleteAPIView.as_view()),
    path(
        "address/<int:pk>/default/",
        SetDefaultAddressAPIView.as_view(),
        name="set-default-address",
    ),

    # Seller Profile APIs
    path("seller-profile/", SellerProfileCreateAPIView.as_view()),
    path("seller-profile/detail/", SellerProfileAPIView.as_view()),
    path("seller-profile/update/", SellerProfileUpdateAPIView.as_view()),
    path("seller-profile/delete/", SellerProfileDeleteAPIView.as_view()),
]