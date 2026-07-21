from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

urlpatterns = [

    # Admin
    path("admin/", admin.site.urls),

    # Dashboard
    path("api/dashboard/", include("dashboards.urls")),

    # Accounts
    path("api/accounts/", include("accounts.urls")),

    # Categories
    path("api/categories/", include("categories.urls")),

    # Brands
    path("api/brands/", include("brands.urls")),

    # Products
    path("api/products/", include("products.urls")),

    # Cart
    path("api/cart/", include("cart.urls")),

    # Orders
    path("api/orders/", include("orders.urls")),

    # Seller
    path("api/seller/", include("seller.urls")),

    # Reviews
    path("api/reviews/", include("reviews.urls")),

    # Wishlist
    path("api/wishlist/", include("wishlist.urls")),

    # Notifications
    path("api/notifications/", include("notifications.urls")),

    # Coupons
    path("api/coupons/", include("coupons.urls")),

    # Support
    path("api/support/", include("support.urls")),

    # Payments
    path("api/payments/", include("payments.urls")),

    # JWT Authentication
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # API Documentation
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
]

# Media Files
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)