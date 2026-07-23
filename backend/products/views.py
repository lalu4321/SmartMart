from django.shortcuts import get_object_or_404
from django.utils.text import slugify
from rest_framework.parsers import MultiPartParser, FormParser
from django.db.models import Avg, Count, Q
from rest_framework.exceptions import ValidationError
from django.http import Http404

from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from accounts.models import Account
from django.db.models import Avg, Count
from .pagination import ProductPagination 

from .models import Product,ProductAttribute,ProductVariant,ProductInventory,ProductImage
from .serializers import ProductSerializer,ProductImageSerializer,ProductAttributeSerializer,ProductVariantSerializer, ProductInventorySerializer

def generate_unique_slug(name, instance=None):

    slug = slugify(name)
    unique_slug = slug
    counter = 1

    while Product.objects.filter(
        slug=unique_slug
    ).exclude(
        pk=instance.pk if instance else None
    ).exists():

        unique_slug = f"{slug}-{counter}"
        counter += 1

    return unique_slug

class ProductCreateAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        try:

            if request.user.role != Account.Role.SELLER:
                return Response(
                    {
                        "message": "Only sellers can create products."
                    },
                    status=status.HTTP_403_FORBIDDEN
                )

            if not hasattr(request.user, "seller_profile"):
                return Response(
                    {
                        "message": "Seller profile not found."
                    },
                    status=status.HTTP_404_NOT_FOUND
                )

            serializer = ProductSerializer(
                data=request.data
            )

            serializer.is_valid(
                raise_exception=True
            )

            product = serializer.save(
                seller=request.user.seller_profile,
                slug=generate_unique_slug(
                    serializer.validated_data["name"]
                )
            )

            return Response(
                {
                    "message": "Product created successfully.",
                    "data": ProductSerializer(product).data
                },
                status=status.HTTP_201_CREATED
            )

        except ValidationError:
            raise

        except Exception as e:

            return Response(
                {
                    "success": False,
                    "message": "Failed to create product.",
                    "error": str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class ProductListAPIView(APIView):

    permission_classes = [AllowAny]

    def get(self, request):

        products = Product.objects.annotate(
            average_rating=Avg("reviews__rating"),
            total_reviews=Count("reviews")
        )

        # Search by product name
        search = request.query_params.get("search")

        if search:
            products = products.filter(
                Q(name__icontains=search)
            )

        # Filter by category
        category = request.query_params.get("category")

        if category:
            products = products.filter(
                category_id=category
            )

        # Filter by brand
        brand = request.query_params.get("brand")

        if brand:
            products = products.filter(
                brand_id=brand
            )

        # Minimum price
        min_price = request.query_params.get("min_price")

        if min_price:
            products = products.filter(
                price__gte=min_price
            )

        # Maximum price
        max_price = request.query_params.get("max_price")

        if max_price:
            products = products.filter(
                price__lte=max_price
            )

        # Ordering
        ordering = request.query_params.get("ordering")

        allowed_ordering = [
            "price",
            "-price",
            "created_at",
            "-created_at",
            "average_rating",
            "-average_rating",
        ]

        if ordering in allowed_ordering:
            products = products.order_by(ordering)

        paginator = ProductPagination()

        page = paginator.paginate_queryset(
        products,
        request
        )

        serializer = ProductSerializer(
        page,
        many=True
            )

        return paginator.get_paginated_response(
    {
        "message": "Products fetched successfully.",
        "data": serializer.data
    }
)

class ProductDetailAPIView(APIView):

    permission_classes = [AllowAny]

    def get(self, request, pk):

        product = get_object_or_404(
            Product.objects.annotate(
            average_rating=Avg("reviews__rating"),
            total_reviews=Count("reviews")
        ),
            pk=pk
        )

        serializer = ProductSerializer(product)

        return Response(
            {
                "message": "Product fetched successfully.",
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )

class ProductUpdateAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def put(self, request, pk):

        try:

            if request.user.role != Account.Role.SELLER:
                return Response(
                    {
                        "message": "Only sellers can update products."
                    },
                    status=status.HTTP_403_FORBIDDEN
                )

            product = get_object_or_404(
                Product,
                pk=pk
            )

            if product.seller != request.user.seller_profile:
                return Response(
                    {
                        "message": "You can update only your own products."
                    },
                    status=status.HTTP_403_FORBIDDEN
                )

            serializer = ProductSerializer(
                product,
                data=request.data
            )

            serializer.is_valid(
                raise_exception=True
            )

            product = serializer.save()

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
                    "data": ProductSerializer(product).data
                },
                status=status.HTTP_200_OK
            )

        except ValidationError:
            raise

        except Exception as e:

            return Response(
                {
                    "success": False,
                    "message": "Failed to update product.",
                    "error": str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
class ProductDeleteAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):

        try:

            if request.user.role != Account.Role.SELLER:
                return Response(
                    {
                        "message": "Only sellers can delete products."
                    },
                    status=status.HTTP_403_FORBIDDEN
                )

            product = get_object_or_404(
                Product,
                pk=pk
            )

            if product.seller != request.user.seller_profile:
                return Response(
                    {
                        "message": "You can delete only your own products."
                    },
                    status=status.HTTP_403_FORBIDDEN
                )

            product.delete()

            return Response(
                {
                    "message": "Product deleted successfully."
                },
                status=status.HTTP_200_OK
            )

        except Http404:
            raise

        except Exception as e:

            return Response(
                {
                    "message": "Failed to delete product.",
                    "error": str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
class ProductImageCreateAPIView(APIView):

    permission_classes = [IsAuthenticated]

    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):

        if request.user.role != Account.Role.SELLER:
            return Response(
                {
                    "message": "Only sellers can upload product images."
                },
                status=status.HTTP_403_FORBIDDEN
            )

        product_id = request.data.get("product")

        product = get_object_or_404(
            Product,
            pk=product_id
        )

        if product.seller != request.user.seller_profile:
            return Response(
                {
                    "message": "You can upload images only for your own products."
                },
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = ProductImageSerializer(
            data=request.data
        )

        if serializer.is_valid():

            image = serializer.save()

            return Response(
                {
                    "message": "Product image uploaded successfully.",
                    "data": ProductImageSerializer(image).data
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    
class ProductImageListAPIView(APIView):

    def get(self, request):

        images = ProductImage.objects.all()

        serializer = ProductImageSerializer(
            images,
            many=True
        )

        return Response(
            {
                "message": "Product images fetched successfully.",
                "count": images.count(),
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )

class ProductImageDetailAPIView(APIView):

    def get(self, request, pk):

        image = get_object_or_404(
            ProductImage,
            pk=pk
        )

        serializer = ProductImageSerializer(image)

        return Response(
            {
                "message": "Product image fetched successfully.",
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )

class ProductImageUpdateAPIView(APIView):

    permission_classes = [IsAuthenticated]

    parser_classes = [MultiPartParser, FormParser]

    def put(self, request, pk):

        try:

            if request.user.role != Account.Role.SELLER:
                return Response(
                    {
                        "message": "Only sellers can update product images."
                    },
                    status=status.HTTP_403_FORBIDDEN
                )

            image = get_object_or_404(
                ProductImage,
                pk=pk
            )

            if image.product.seller != request.user.seller_profile:
                return Response(
                    {
                        "message": "You can update only your own product images."
                    },
                    status=status.HTTP_403_FORBIDDEN
                )

            serializer = ProductImageSerializer(
                image,
                data=request.data
            )

            if serializer.is_valid():

                serializer.save()

                return Response(
                    {
                        "message": "Product image updated successfully.",
                        "data": serializer.data
                    },
                    status=status.HTTP_200_OK
                )

            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        except Exception as e:

            return Response(
                {
                    "success": False,
                    "message": "Failed to update product image.",
                    "error": str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
class ProductImageDeleteAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):

        try:

            if request.user.role != Account.Role.SELLER:
                return Response(
                    {
                        "message": "Only sellers can delete product images."
                    },
                    status=status.HTTP_403_FORBIDDEN
                )

            image = get_object_or_404(
                ProductImage,
                pk=pk
            )

            if image.product.seller != request.user.seller_profile:
                return Response(
                    {
                        "message": "You can delete only your own product images."
                    },
                    status=status.HTTP_403_FORBIDDEN
                )

            image.delete()

            return Response(
                {
                    "message": "Product image deleted successfully."
                },
                status=status.HTTP_200_OK
            )

        except Exception as e:

            return Response(
                {
                    "success": False,
                    "message": "Failed to delete product image.",
                    "error": str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class ProductAttributeCreateAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        if request.user.role != Account.Role.SELLER:
            return Response(
                {
                    "message": "Only sellers can create product attributes."
                },
                status=status.HTTP_403_FORBIDDEN
            )

        product = get_object_or_404(
            Product,
            pk=request.data.get("product")
        )

        if product.seller != request.user.seller_profile:
            return Response(
                {
                    "message": "You can add attributes only to your own products."
                },
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = ProductAttributeSerializer(
            data=request.data
        )

        if serializer.is_valid():

            attribute = serializer.save()

            return Response(
                {
                    "message": "Product attribute created successfully.",
                    "data": ProductAttributeSerializer(attribute).data
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    
class ProductAttributeListAPIView(APIView):

    def get(self, request):

        attributes = ProductAttribute.objects.all()

        serializer = ProductAttributeSerializer(
            attributes,
            many=True
        )

        return Response(
            {
                "message": "Product attributes fetched successfully.",
                "count": attributes.count(),
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )
    
class ProductAttributeDetailAPIView(APIView):

    def get(self, request, pk):

        attribute = get_object_or_404(
            ProductAttribute,
            pk=pk
        )

        serializer = ProductAttributeSerializer(attribute)

        return Response(
            {
                "message": "Product attribute fetched successfully.",
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )
    
class ProductAttributeUpdateAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def put(self, request, pk):

        if request.user.role != Account.Role.SELLER:
            return Response(
                {
                    "message": "Only sellers can update product attributes."
                },
                status=status.HTTP_403_FORBIDDEN
            )

        attribute = get_object_or_404(
            ProductAttribute,
            pk=pk
        )

        if attribute.product.seller != request.user.seller_profile:
            return Response(
                {
                    "message": "You can update only your own product attributes."
                },
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = ProductAttributeSerializer(
            attribute,
            data=request.data
        )

        if serializer.is_valid():

            serializer.save()

            return Response(
                {
                    "message": "Product attribute updated successfully.",
                    "data": serializer.data
                },
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    
class ProductAttributeDeleteAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):

        if request.user.role != Account.Role.SELLER:
            return Response(
                {
                    "message": "Only sellers can delete product attributes."
                },
                status=status.HTTP_403_FORBIDDEN
            )

        attribute = get_object_or_404(
            ProductAttribute,
            pk=pk
        )

        if attribute.product.seller != request.user.seller_profile:
            return Response(
                {
                    "message": "You can delete only your own product attributes."
                },
                status=status.HTTP_403_FORBIDDEN
            )

        attribute.delete()

        return Response(
            {
                "message": "Product attribute deleted successfully."
            },
            status=status.HTTP_200_OK
        )
    
class ProductVariantCreateAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        if request.user.role != Account.Role.SELLER:
            return Response(
                {
                    "message": "Only sellers can create product variants."
                },
                status=status.HTTP_403_FORBIDDEN
            )

        product = get_object_or_404(
            Product,
            pk=request.data.get("product")
        )

        if product.seller != request.user.seller_profile:
            return Response(
                {
                    "message": "You can create variants only for your own products."
                },
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = ProductVariantSerializer(
            data=request.data
        )

        if serializer.is_valid():

            variant = serializer.save()

            return Response(
                {
                    "message": "Product variant created successfully.",
                    "data": ProductVariantSerializer(variant).data
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    
class ProductVariantListAPIView(APIView):

    def get(self, request):

        variants = ProductVariant.objects.all()

        serializer = ProductVariantSerializer(
            variants,
            many=True
        )

        return Response(
            {
                "message": "Product variants fetched successfully.",
                "count": variants.count(),
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )
    
class ProductVariantDetailAPIView(APIView):

    def get(self, request, pk):

        variant = get_object_or_404(
            ProductVariant,
            pk=pk
        )

        serializer = ProductVariantSerializer(
            variant
        )

        return Response(
            {
                "message": "Product variant fetched successfully.",
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )

class ProductVariantUpdateAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def put(self, request, pk):

        try:

            if request.user.role != Account.Role.SELLER:
                return Response(
                    {
                        "message": "Only sellers can update product variants."
                    },
                    status=status.HTTP_403_FORBIDDEN
                )

            variant = get_object_or_404(
                ProductVariant,
                pk=pk
            )

            if variant.product.seller != request.user.seller_profile:
                return Response(
                    {
                        "message": "You can update only your own product variants."
                    },
                    status=status.HTTP_403_FORBIDDEN
                )

            serializer = ProductVariantSerializer(
                variant,
                data=request.data
            )

            serializer.is_valid(
                raise_exception=True
            )

            serializer.save()

            return Response(
                {
                    "message": "Product variant updated successfully.",
                    "data": serializer.data
                },
                status=status.HTTP_200_OK
            )

        except ValidationError:
            raise

        except Exception as e:
            return Response(
                {
                    "message": "Failed to update product variant.",
                    "error": str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
class ProductVariantDeleteAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):

        try:

            if request.user.role != Account.Role.SELLER:
                return Response(
                    {
                        "message": "Only sellers can delete product variants."
                    },
                    status=status.HTTP_403_FORBIDDEN
                )

            variant = get_object_or_404(
                ProductVariant,
                pk=pk
            )

            if variant.product.seller != request.user.seller_profile:
                return Response(
                    {
                        "message": "You can delete only your own product variants."
                    },
                    status=status.HTTP_403_FORBIDDEN
                )

            variant.delete()

            return Response(
                {
                    "message": "Product variant deleted successfully."
                },
                status=status.HTTP_200_OK
            )

        except ValidationError:
            raise

        except Exception as e:
            return Response(
                {
                    "message": "Failed to delete product variant.",
                    "error": str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    

class ProductInventoryCreateAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        try:

            if request.user.role != Account.Role.SELLER:
                return Response(
                    {
                        "message": "Only sellers can create inventory."
                    },
                    status=status.HTTP_403_FORBIDDEN
                )

            variant = get_object_or_404(
                ProductVariant,
                pk=request.data.get("variant")
            )

            if variant.product.seller != request.user.seller_profile:
                return Response(
                    {
                        "message": "You can manage inventory only for your own products."
                    },
                    status=status.HTTP_403_FORBIDDEN
                )

            serializer = ProductInventorySerializer(
                data=request.data
            )

            if serializer.is_valid():

                inventory = serializer.save()

                return Response(
                    {
                        "message": "Inventory created successfully.",
                        "data": ProductInventorySerializer(inventory).data
                    },
                    status=status.HTTP_201_CREATED
                )

            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        except ValidationError:
            raise

        except Exception as e:
            return Response(
                {
                    "success": False,
                    "message": "Failed to create inventory.",
                    "error": str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
class ProductInventoryListAPIView(APIView):

    def get(self, request):

        inventories = ProductInventory.objects.all()

        serializer = ProductInventorySerializer(
            inventories,
            many=True
        )

        return Response(
            {
                "message": "Inventory fetched successfully.",
                "count": inventories.count(),
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )
    
class ProductInventoryDetailAPIView(APIView):

    def get(self, request, pk):

        inventory = get_object_or_404(
            ProductInventory,
            pk=pk
        )

        serializer = ProductInventorySerializer(
            inventory
        )

        return Response(
            {
                "message": "Inventory fetched successfully.",
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )

class ProductInventoryUpdateAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def put(self, request, pk):

        try:

            if request.user.role != Account.Role.SELLER:
                return Response(
                    {
                        "message": "Only sellers can update inventory."
                    },
                    status=status.HTTP_403_FORBIDDEN
                )

            inventory = get_object_or_404(
                ProductInventory,
                pk=pk
            )

            if inventory.variant.product.seller != request.user.seller_profile:
                return Response(
                    {
                        "message": "You can update only your own inventory."
                    },
                    status=status.HTTP_403_FORBIDDEN
                )

            serializer = ProductInventorySerializer(
                inventory,
                data=request.data
            )

            serializer.is_valid(raise_exception=True)

            serializer.save()

            return Response(
                {
                    "message": "Inventory updated successfully.",
                    "data": serializer.data
                },
                status=status.HTTP_200_OK
            )

        except ValidationError:
            raise

        except Exception as e:
            return Response(
                {
                    "success": False,
                    "message": "Failed to update inventory.",
                    "error": str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ProductInventoryDeleteAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):

        try:

            if request.user.role != Account.Role.SELLER:
                return Response(
                    {
                        "message": "Only sellers can delete inventory."
                    },
                    status=status.HTTP_403_FORBIDDEN
                )

            inventory = get_object_or_404(
                ProductInventory,
                pk=pk
            )

            if inventory.variant.product.seller != request.user.seller_profile:
                return Response(
                    {
                        "message": "You can delete only your own inventory."
                    },
                    status=status.HTTP_403_FORBIDDEN
                )

            inventory.delete()

            return Response(
                {
                    "message": "Inventory deleted successfully."
                },
                status=status.HTTP_200_OK
            )

        except ValidationError:
            raise

        except Exception as e:
            return Response(
                {
                    "success": False,
                    "message": "Failed to delete inventory.",
                    "error": str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )