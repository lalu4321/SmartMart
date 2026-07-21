from django.urls import path

from .views import (
    BrandCreateAPIView,
    BrandListAPIView,
    BrandDetailAPIView,
    BrandUpdateAPIView,
    BrandDeleteAPIView,
)

urlpatterns = [

    path("create/",BrandCreateAPIView.as_view(),name="brand-create"),

    path("list/",BrandListAPIView.as_view(),name="brand-list"),

    path("<int:pk>/",BrandDetailAPIView.as_view(),name="brand-detail"),

    path("<int:pk>/update/",BrandUpdateAPIView.as_view(),name="brand-update"),

    path("<int:pk>/delete/",BrandDeleteAPIView.as_view(),name="brand-delete"),

]