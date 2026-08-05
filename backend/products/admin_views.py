from django.shortcuts import get_object_or_404
from django.db.models import Avg, Count, Q
from .utils import generate_unique_slug

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser

from .models import Product
from .serializers import ProductSerializer


class AdminProductListAPIView(APIView):

    permission_classes = [IsAdminUser]

    def get(self, request):

        products = Product.objects.annotate(

            average_rating=Avg("reviews__rating"),

            total_reviews=Count("reviews")

        )

        search = request.query_params.get("search")

        if search:

            products = products.filter(

                Q(name__icontains=search)

                | Q(description__icontains=search)

                | Q(category__name__icontains=search)

                | Q(brand__name__icontains=search)

                | Q(seller__shop_name__icontains=search)

            ).distinct()

        category = request.query_params.get("category")

        if category:

            products = products.filter(
                category_id=category
            )

        brand = request.query_params.get("brand")

        if brand:

            products = products.filter(
                brand_id=brand
            )

        seller = request.query_params.get("seller")

        if seller:

            products = products.filter(
                seller_id=seller
            )

        serializer = ProductSerializer(

            products,

            many=True,

            context={"request": request}

        )

        return Response(

            {

                "message": "Products fetched successfully.",

                "count": products.count(),

                "data": serializer.data,

            },

            status=status.HTTP_200_OK,

        )
    
class AdminProductDetailAPIView(APIView):

    permission_classes = [IsAdminUser]

    def get(self, request, pk):

        product = get_object_or_404(

            Product.objects.annotate(

                average_rating=Avg("reviews__rating"),

                total_reviews=Count("reviews")

            ),

            pk=pk

        )

        serializer = ProductSerializer(

            product,

            context={"request": request}

        )

        return Response(

            {

                "message": "Product fetched successfully.",

                "data": serializer.data,

            },

            status=status.HTTP_200_OK,

        )

class AdminProductUpdateAPIView(APIView):

    permission_classes = [IsAdminUser]

    def put(self, request, pk):

        try:

            product = get_object_or_404(
                Product,
                pk=pk
            )

            serializer = ProductSerializer(
                product,
                data=request.data,
                partial=True
            )

            serializer.is_valid(
                raise_exception=True
            )

            product = serializer.save()

            if "name" in serializer.validated_data:

                product.slug = generate_unique_slug(
                    product.name,
                    product
                )

                product.save(
                    update_fields=["slug"]
                )

            return Response(
                {
                    "message": "Product updated successfully.",
                    "data": ProductSerializer(
                        product,
                        context={"request": request}
                    ).data,
                },
                status=status.HTTP_200_OK,
            )

        except Exception as e:

            return Response(
                {
                    "success": False,
                    "message": "Failed to update product.",
                    "error": str(e),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

class AdminProductDeleteAPIView(APIView):

    permission_classes = [IsAdminUser]

    def delete(self, request, pk):

        try:

            product = get_object_or_404(
                Product,
                pk=pk
            )

            product.delete()

            return Response(
                {
                    "message": "Product deleted successfully."
                },
                status=status.HTTP_200_OK
            )

        except Exception as e:

            return Response(
                {
                    "success": False,
                    "message": "Failed to delete product.",
                    "error": str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class AdminProductStatusAPIView(APIView):

    permission_classes = [IsAdminUser]

    def patch(self, request, pk):

        try:

            product = get_object_or_404(
                Product,
                pk=pk
            )

            product.is_active = (
                not product.is_active
            )

            product.save(
                update_fields=["is_active"]
            )

            return Response(
                {
                    "message": (
                        "Product enabled successfully."
                        if product.is_active
                        else
                        "Product disabled successfully."
                    ),
                    "data": {
                        "id": product.id,
                        "is_active": product.is_active,
                    },
                },
                status=status.HTTP_200_OK,
            )

        except Exception as e:

            return Response(
                {
                    "success": False,
                    "message": "Failed to update product status.",
                    "error": str(e),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

class AdminProductFeaturedAPIView(APIView):

    permission_classes = [IsAdminUser]

    def patch(self, request, pk):

        try:

            product = get_object_or_404(
                Product,
                pk=pk
            )

            product.is_featured = (
                not product.is_featured
            )

            product.save(
                update_fields=["is_featured"]
            )

            return Response(
                {
                    "message": (
                        "Product marked as featured successfully."
                        if product.is_featured
                        else
                        "Product removed from featured successfully."
                    ),
                    "data": {
                        "id": product.id,
                        "is_featured": product.is_featured,
                    },
                },
                status=status.HTTP_200_OK,
            )

        except Exception as e:

            return Response(
                {
                    "success": False,
                    "message": "Failed to update featured status.",
                    "error": str(e),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )