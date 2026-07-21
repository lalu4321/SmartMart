from django.urls import path


from .views import (
    CategoryCreateAPIView,
    CategoryListAPIView,
    CategoryDetailAPIView,
    CategoryUpdateAPIView,
    CategoryDeleteAPIView,
)


urlpatterns = [
    path("create/", CategoryCreateAPIView.as_view()),
    path("list/", CategoryListAPIView.as_view()),
    path("<int:pk>/", CategoryDetailAPIView.as_view()),
    path("<int:pk>/update/", CategoryUpdateAPIView.as_view()),
    path("<int:pk>/delete/", CategoryDeleteAPIView.as_view()),
]