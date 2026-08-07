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

from .admin_views import (
    AdminUserListAPIView,
    AdminUserDetailAPIView,
    AdminUserCreateAPIView,
    AdminUserUpdateAPIView,
    AdminUserDeleteAPIView,
    AdminUserStatusAPIView,
)

from .admin_seller_views import (
    AdminSellerListAPIView,
    AdminSellerDetailAPIView,
    AdminSellerStatusAPIView,
    AdminSellerDeleteAPIView,
)

urlpatterns = [

    # ==================================================
    # Account APIs
    # ==================================================

    path("register/", RegisterAPIView.as_view(), name="register"),
    path("profile/", ProfileAPIView.as_view(), name="profile"),
    path("profile/update/", UpdateProfileAPIView.as_view(), name="profile-update"),

    # ==================================================
    # Address APIs
    # ==================================================

    path("address/", AddressCreateAPIView.as_view(), name="address-create"),
    path("address/list/", AddressListAPIView.as_view(), name="address-list"),
    path("address/<int:pk>/", AddressDetailAPIView.as_view(), name="address-detail"),
    path("address/<int:pk>/update/", AddressUpdateAPIView.as_view(), name="address-update"),
    path("address/<int:pk>/delete/", AddressDeleteAPIView.as_view(), name="address-delete"),
    path("address/<int:pk>/default/", SetDefaultAddressAPIView.as_view(), name="set-default-address"),

    # ==================================================
    # Seller Profile APIs
    # ==================================================

    path("seller-profile/", SellerProfileCreateAPIView.as_view(), name="seller-profile-create"),
    path("seller-profile/detail/", SellerProfileAPIView.as_view(), name="seller-profile-detail"),
    path("seller-profile/update/", SellerProfileUpdateAPIView.as_view(), name="seller-profile-update"),
    path("seller-profile/delete/", SellerProfileDeleteAPIView.as_view(), name="seller-profile-delete"),

    # ==================================================
    # Admin User APIs
    # ==================================================

    path("admin/list/", AdminUserListAPIView.as_view(), name="admin-user-list"),
    path("admin/create/", AdminUserCreateAPIView.as_view(), name="admin-user-create"),
    path("admin/<int:pk>/", AdminUserDetailAPIView.as_view(), name="admin-user-detail"),
    path("admin/<int:pk>/update/", AdminUserUpdateAPIView.as_view(), name="admin-user-update"),
    path("admin/<int:pk>/delete/", AdminUserDeleteAPIView.as_view(), name="admin-user-delete"),
    path("admin/<int:pk>/status/", AdminUserStatusAPIView.as_view(), name="admin-user-status"),

    # ==================================================
    # Admin Seller APIs
    # ==================================================

    path("admin/sellers/", AdminSellerListAPIView.as_view(), name="admin-seller-list"),
    path("admin/sellers/<int:pk>/", AdminSellerDetailAPIView.as_view(), name="admin-seller-detail"),
    path("admin/sellers/<int:pk>/status/", AdminSellerStatusAPIView.as_view(), name="admin-seller-status"),
    path("admin/sellers/<int:pk>/delete/", AdminSellerDeleteAPIView.as_view(), name="admin-seller-delete"),
]

