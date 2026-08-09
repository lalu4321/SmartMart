from django.db.models import Sum
from django.contrib.auth.hashers import check_password

from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework import status


from accounts.models import Account
from brands.models import Brand
from categories.models import Category
from products.models import Product
from orders.models import Order
from reviews.models import Review
from support.models import SupportTicket



# ==========================================================
# Admin Dashboard API
# ==========================================================

class AdminDashboardAPIView(APIView):

    permission_classes = [
        IsAdminUser
    ]


    def get(self, request):

        data = {

            "total_users":
            Account.objects.count(),


            "total_customers":
            Account.objects.filter(
                role="CUSTOMER"
            ).count(),


            "total_sellers":
            Account.objects.filter(
                role="SELLER"
            ).count(),


            "total_categories":
            Category.objects.count(),


            "total_brands":
            Brand.objects.count(),


            "total_products":
            Product.objects.count(),


            "total_orders":
            Order.objects.count(),


            "pending_orders":
            Order.objects.filter(
                status="PENDING"
            ).count(),


            "confirmed_orders":
            Order.objects.filter(
                status="CONFIRMED"
            ).count(),


            "shipped_orders":
            Order.objects.filter(
                status="SHIPPED"
            ).count(),


            "delivered_orders":
            Order.objects.filter(
                status="DELIVERED"
            ).count(),


            "cancelled_orders":
            Order.objects.filter(
                status="CANCELLED"
            ).count(),


            "total_reviews":
            Review.objects.count(),


            "total_support_tickets":
            SupportTicket.objects.count(),


            "total_revenue":
            Order.objects.filter(
                status="DELIVERED"
            )
            .aggregate(
                total=Sum("total_amount")
            )["total"] or 0,

        }


        return Response(
            {
                "message":
                "Dashboard fetched successfully.",

                "data":
                data,
            },
            status=status.HTTP_200_OK,
        )

# ==========================================================
# Admin Profile API
# ==========================================================

class AdminProfileAPIView(APIView):

    permission_classes = [
        IsAdminUser
    ]


    def get(self, request):

        user = request.user


        data = {

            "id":
            user.id,

            "username":
            user.username,

            "full_name":
            user.get_full_name(),

            "email":
            user.email,

            "phone":
            user.phone,

            "role":
            user.role,

            "profile_image":
            (
                user.profile_image.url
                if user.profile_image
                else None
            ),

            "created_at":
            user.created_at,

        }


        return Response(
            {
                "message":
                "Profile fetched successfully.",

                "data":
                data,
            },
            status=status.HTTP_200_OK,
        )



    def put(self, request):

        user = request.user


        first_name = request.data.get(
            "full_name",
            "",
        )


        user.first_name = first_name


        user.email = request.data.get(
            "email",
            user.email,
        )


        user.phone = request.data.get(
            "phone",
            user.phone,
        )


        user.save()



        return Response(
            {
                "message":
                "Profile updated successfully.",

                "data":
                {
                    "id":
                    user.id,

                    "username":
                    user.username,

                    "full_name":
                    user.get_full_name(),

                    "email":
                    user.email,

                    "phone":
                    user.phone,

                    "role":
                    user.role,

                    "profile_image":
                    (
                        user.profile_image.url
                        if user.profile_image
                        else None
                    ),

                    "created_at":
                    user.created_at,
                },
            },
            status=status.HTTP_200_OK,
        )

# ==========================================================
# Change Password API
# ==========================================================

class ChangePasswordAPIView(APIView):

    permission_classes = [
        IsAdminUser
    ]


    def patch(self, request):

        user = request.user


        old_password = request.data.get(
            "old_password"
        )

        new_password = request.data.get(
            "new_password"
        )


        if not check_password(
            old_password,
            user.password,
        ):

            return Response(
                {
                    "message":
                    "Old password is incorrect."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


        user.set_password(
            new_password
        )


        user.save()


        return Response(
            {
                "message":
                "Password changed successfully."
            },
            status=status.HTTP_200_OK,
        )



# ==========================================================
# Update Profile Image API
# ==========================================================

class UpdateProfileImageAPIView(APIView):

    permission_classes = [
        IsAdminUser
    ]


    def patch(self, request):

        user = request.user


        image = request.FILES.get(
            "profile_image"
        )


        if not image:

            return Response(
                {
                    "message":
                    "No image uploaded."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


        user.profile_image = image

        user.save()



        return Response(
            {
                "message":
                "Profile image updated successfully.",

                "profile_image":
                user.profile_image.url,
            },
            status=status.HTTP_200_OK,
        )

