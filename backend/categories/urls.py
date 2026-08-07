from django.urls import path

from .views import (
    CategoryCreateAPIView,
    CategoryListAPIView,
    CategoryDetailAPIView,
    CategoryUpdateAPIView,
    CategoryDeleteAPIView,
)

urlpatterns = [

    # ==================================
    # Category APIs
    # ==================================

    path("create/", CategoryCreateAPIView.as_view(), name="category-create"),
    path("list/", CategoryListAPIView.as_view(), name="category-list"),
    path("<int:pk>/", CategoryDetailAPIView.as_view(), name="category-detail"),
    path("<int:pk>/update/", CategoryUpdateAPIView.as_view(), name="category-update"),
    path("<int:pk>/delete/", CategoryDeleteAPIView.as_view(), name="category-delete"),
] already