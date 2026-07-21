from django.urls import path
from .views import AdminDashboardAPIView

urlpatterns = [
    path("", AdminDashboardAPIView.as_view(), name="admin-dashboard"),
]