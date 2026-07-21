from django.db.models import Sum
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from accounts.models import Account
from brands.models import Brand
from categories.models import Category
from products.models import Product
from orders.models import Order
from reviews.models import Review
from support.models import SupportTicket


class AdminDashboardAPIView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):

        data = {
            "total_users": Account.objects.count(),
            "total_customers": Account.objects.filter(role="CUSTOMER").count(),
            "total_sellers": Account.objects.filter(role="SELLER").count(),

            "total_categories": Category.objects.count(),
            "total_brands": Brand.objects.count(),
            "total_products": Product.objects.count(),

            "total_orders": Order.objects.count(),
            "pending_orders": Order.objects.filter(status="PENDING").count(),
            "confirmed_orders": Order.objects.filter(status="CONFIRMED").count(),
            "shipped_orders": Order.objects.filter(status="SHIPPED").count(),
            "delivered_orders": Order.objects.filter(status="DELIVERED").count(),
            "cancelled_orders": Order.objects.filter(status="CANCELLED").count(),

            "total_reviews": Review.objects.count(),
            "total_support_tickets": SupportTicket.objects.count(),

            "total_revenue": Order.objects.filter(
                status="DELIVERED"
            ).aggregate(
                total=Sum("total_amount")
            )["total"] or 0
        }

        return Response({
            "message": "Dashboard fetched successfully.",
            "data": data
        })