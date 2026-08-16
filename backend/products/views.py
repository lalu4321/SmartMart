from django.db import transaction
from django.db.models import Avg, Count, Q
from django.http import Http404
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import Account, SellerProfile

from .models import (
    Product,
    ProductAttribute,
    ProductImage,
    ProductInventory,
    ProductVariant,
)

from .pagination import ProductPagination
from .serializers import (
    ProductSerializer,
    ProductImageSerializer,
    ProductAttributeSerializer,
    ProductVariantSerializer,
    ProductInventorySerializer,
)
from .utils import generate_unique_slug


# ==========================================================
# Product Create API
# ==========================================================

class ProductCreateAPIView(APIView):

    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request):

        try:

            # -----------------------------
            # Seller Role Check
            # -----------------------------

            if request.user.role != Account.Role.SELLER:
                return Response(
                    {
                        "message": "Only sellers can create products."
                    },
                    status=status.HTTP_403_FORBIDDEN,
                )

            # -----------------------------
            # Seller Profile Check
            # -----------------------------

            if not hasattr(request.user, "seller_profile"):
                return Response(
                    {
                        "message": "Seller profile not found."
                    },
                    status=status.HTTP_404_NOT_FOUND,
                )

            seller = request.user.seller_profile

            serializer = ProductSerializer(
                data=request.data,
                context={"request": request},
            )

            serializer.is_valid(
                raise_exception=True
            )

            product = serializer.save(
                seller=seller,
                slug=generate_unique_slug(
                    serializer.validated_data["name"]
                ),
            )

            return Response(
                {
                    "message": "Product created successfully.",
                    "data": ProductSerializer(
                        product,
                        context={"request": request},
                    ).data,
                },
                status=status.HTTP_201_CREATED,
            )

        except ValidationError:
            raise

        except Exception as e:

            transaction.set_rollback(True)

            return Response(
                {
                    "success": False,
                    "message": "Failed to create product.",
                    "error": str(e),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        # ==========================================================
# Product List API
# ==========================================================

class ProductListAPIView(APIView):

    permission_classes = [AllowAny]

    def get(self, request):

        products = (
            Product.objects.select_related(
                "seller",
                "category",
                "brand",
            )
            .prefetch_related(
                "images",
                "variants",
                "attributes",
            )
            .annotate(
                average_rating=Avg("reviews__rating"),
                total_reviews=Count(
                    "reviews",
                    distinct=True,
                ),
            )
        )

        # ==========================================
        # Search
        # ==========================================

        search = (
            request.query_params
            .get("search", "")
            .strip()
        )

        if search:

            products = products.filter(

                Q(name__icontains=search)

                | Q(description__icontains=search)

                | Q(category__name__icontains=search)

                | Q(brand__name__icontains=search)

            ).distinct()

        # ==========================================
        # Category Filter
        # ==========================================

        category = request.query_params.get(
            "category"
        )

        if category:

            products = products.filter(
                category_id=category
            )

        # ==========================================
        # Brand Filter
        # ==========================================

        brand = request.query_params.get(
            "brand"
        )

        if brand:

            products = products.filter(
                brand_id=brand
            )

        # ==========================================
        # Featured Filter
        # ==========================================

        featured = request.query_params.get(
            "featured"
        )

        if featured is not None:

            if featured.lower() == "true":
                products = products.filter(
                    is_featured=True
                )

            elif featured.lower() == "false":
                products = products.filter(
                    is_featured=False
                )

        # ==========================================
        # Active Filter
        # ==========================================

        active = request.query_params.get(
            "active"
        )

        if active is not None:

            if active.lower() == "true":
                products = products.filter(
                    is_active=True
                )

            elif active.lower() == "false":
                products = products.filter(
                    is_active=False
                )

        # ==========================================
        # Price Filters
        # ==========================================

        min_price = request.query_params.get(
            "min_price"
        )

        max_price = request.query_params.get(
            "max_price"
        )

        if min_price:
            products = products.filter(
                price__gte=min_price
            )

        if max_price:
            products = products.filter(
                price__lte=max_price
            )

        # ==========================================
        # Ordering
        # ==========================================

        ordering = request.query_params.get(
            "ordering",
            "-created_at",
        )

        allowed_ordering = {
            "price",
            "-price",
            "name",
            "-name",
            "created_at",
            "-created_at",
        }

        if ordering in allowed_ordering:
            products = products.order_by(ordering)
        else:
            products = products.order_by("-created_at")

        # ==========================================
        # Pagination
        # ==========================================

        paginator = ProductPagination()

        paginated_products = paginator.paginate_queryset(
            products,
            request,
        )

        serializer = ProductSerializer(
            paginated_products,
            many=True,
            context={"request": request},
        )

        return paginator.get_paginated_response(
            {
                "message": "Products fetched successfully.",
                "count": products.count(),
                "data": serializer.data,
            }
        )


# ==========================================================
# Product Detail API
# ==========================================================

class ProductDetailAPIView(APIView):

    permission_classes = [AllowAny]

    def get(self, request, pk):

        try:

            product = (
                Product.objects
                .select_related(
                    "seller",
                    "category",
                    "brand",
                )
                .prefetch_related(
                    "images",
                    "attributes",
                    "variants__inventory",
                )
                .annotate(
                    average_rating=Avg("reviews__rating"),
                    total_reviews=Count(
                        "reviews",
                        distinct=True,
                    ),
                )
                .get(
                    pk=pk,
                    is_active=True,
                )
            )

        except Product.DoesNotExist:
            raise Http404("Product not found.")

        serializer = ProductSerializer(
            product,
            context={"request": request},
        )

        return Response(
            {
                "message": "Product fetched successfully.",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

        # ==========================================
        # Ordering
        # ==========================================

        ordering = request.query_params.get(
            "ordering",
            "-created_at",
        )

        allowed_ordering = {
            "price",
            "-price",
            "name",
            "-name",
            "created_at",
            "-created_at",
        }

        if ordering in allowed_ordering:
            products = products.order_by(ordering)
        else:
            products = products.order_by("-created_at")

        # ==========================================
        # Pagination
        # ==========================================

        paginator = ProductPagination()

        paginated_products = paginator.paginate_queryset(
            products,
            request,
        )

        serializer = ProductSerializer(
            paginated_products,
            many=True,
            context={"request": request},
        )

        return paginator.get_paginated_response(
            {
                "message": "Products fetched successfully.",
                "count": products.count(),
                "data": serializer.data,
            }
        )


# ==========================================================
# Product Detail API
# ==========================================================

class ProductDetailAPIView(APIView):

    permission_classes = [AllowAny]

    def get(self, request, pk):

        try:

            product = (
                Product.objects
                .select_related(
                    "seller",
                    "category",
                    "brand",
                )
                .prefetch_related(
                    "images",
                    "attributes",
                    "variants__inventory",
                )
                .annotate(
                    average_rating=Avg("reviews__rating"),
                    total_reviews=Count(
                        "reviews",
                        distinct=True,
                    ),
                )
                .get(
                    pk=pk,
                    is_active=True,
                )
            )

        except Product.DoesNotExist:
            raise Http404("Product not found.")

        serializer = ProductSerializer(
            product,
            context={"request": request},
        )

        return Response(
            {
                "message": "Product fetched successfully.",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

# ==========================================================
# Product Update API
# ==========================================================

class ProductUpdateAPIView(APIView):

    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def put(self, request, pk):

        try:

            if request.user.role != Account.Role.SELLER:

                return Response(
                    {
                        "message": "Only sellers can update products."
                    },
                    status=status.HTTP_403_FORBIDDEN,
                )

            seller = request.user.seller_profile

            product = get_object_or_404(
                Product,
                pk=pk,
                seller=seller,
            )

            serializer = ProductSerializer(
                product,
                data=request.data,
                partial=True,
                context={"request": request},
            )

            serializer.is_valid(
                raise_exception=True
            )

            product = serializer.save()

            if "name" in serializer.validated_data:

                product.slug = generate_unique_slug(
                    product.name,
                    product,
                )

                product.save(
                    update_fields=["slug"]
                )

            return Response(
                {
                    "message": "Product updated successfully.",
                    "data": ProductSerializer(
                        product,
                        context={
                            "request": request
                        },
                    ).data,
                },
                status=status.HTTP_200_OK,
            )

        except ValidationError:
            raise

        except Exception as e:

            transaction.set_rollback(True)

            return Response(
                {
                    "success": False,
                    "message": "Failed to update product.",
                    "error": str(e),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


# ==========================================================
# Product Delete API
# ==========================================================

class ProductDeleteAPIView(APIView):

    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def delete(self, request, pk):

        try:

            if request.user.role != Account.Role.SELLER:

                return Response(
                    {
                        "message": "Only sellers can delete products."
                    },
                    status=status.HTTP_403_FORBIDDEN,
                )

            seller = request.user.seller_profile

            product = get_object_or_404(
                Product,
                pk=pk,
                seller=seller,
            )

            product.delete()

            return Response(
                {
                    "message": "Product deleted successfully."
                },
                status=status.HTTP_200_OK,
            )

        except Exception as e:

            transaction.set_rollback(True)

            return Response(
                {
                    "success": False,
                    "message": "Failed to delete product.",
                    "error": str(e),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

# ==========================================================
# Product Image Create API
# ==========================================================

class ProductImageCreateAPIView(APIView):

    permission_classes = [IsAuthenticated]

    parser_classes = (
        MultiPartParser,
        FormParser,
    )

    @transaction.atomic
    def post(self, request):

        try:

            if request.user.role != Account.Role.SELLER:

                return Response(
                    {
                        "message": "Only sellers can upload product images."
                    },
                    status=status.HTTP_403_FORBIDDEN,
                )

            product_id = request.data.get("product")

            product = get_object_or_404(
                Product,
                pk=product_id,
                seller=request.user.seller_profile,
            )

            serializer = ProductImageSerializer(
                data=request.data,
                context={"request": request},
            )

            serializer.is_valid(
                raise_exception=True
            )

            image = serializer.save(
                product=product
            )

            return Response(
                {
                    "message": "Product image uploaded successfully.",
                    "data": ProductImageSerializer(
                        image,
                        context={"request": request},
                    ).data,
                },
                status=status.HTTP_201_CREATED,
            )

        except ValidationError:
            raise

        except Exception as e:

            transaction.set_rollback(True)

            return Response(
                {
                    "success": False,
                    "message": "Failed to upload product image.",
                    "error": str(e),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


# ==========================================================
# Product Image List API
# ==========================================================

class ProductImageListAPIView(APIView):

    permission_classes = [AllowAny]

    def get(self, request, product_id):

        product = get_object_or_404(
            Product,
            pk=product_id,
            is_active=True,
        )

        images = (
            ProductImage.objects.filter(
                product=product
            )
            .order_by(
                "-is_primary",
                "created_at",
            )
        )

        serializer = ProductImageSerializer(
            images,
            many=True,
            context={"request": request},
        )

        return Response(
            {
                "message": "Product images fetched successfully.",
                "count": images.count(),
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


# ==========================================================
# Product Image Detail API
# ==========================================================

class ProductImageDetailAPIView(APIView):

    permission_classes = [AllowAny]

    def get(self, request, pk):

        image = get_object_or_404(
            ProductImage.objects.select_related("product"),
            pk=pk,
            product__is_active=True,
        )

        serializer = ProductImageSerializer(
            image,
            context={"request": request},
        )

        return Response(
            {
                "message": "Product image fetched successfully.",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


# ==========================================================
# Product Image Update API
# ==========================================================

class ProductImageUpdateAPIView(APIView):

    permission_classes = [IsAuthenticated]

    parser_classes = (
        MultiPartParser,
        FormParser,
    )

    @transaction.atomic
    def put(self, request, pk):

        try:

            if request.user.role != Account.Role.SELLER:

                return Response(
                    {
                        "message": "Only sellers can update product images."
                    },
                    status=status.HTTP_403_FORBIDDEN,
                )

            image = get_object_or_404(
                ProductImage.objects.select_related(
                    "product",
                    "product__seller",
                ),
                pk=pk,
                product__seller=request.user.seller_profile,
            )

            serializer = ProductImageSerializer(
                image,
                data=request.data,
                partial=True,
                context={"request": request},
            )

            serializer.is_valid(
                raise_exception=True
            )

            image = serializer.save()

            return Response(
                {
                    "message": "Product image updated successfully.",
                    "data": ProductImageSerializer(
                        image,
                        context={"request": request},
                    ).data,
                },
                status=status.HTTP_200_OK,
            )

        except ValidationError:
            raise

        except Exception as e:

            transaction.set_rollback(True)

            return Response(
                {
                    "success": False,
                    "message": "Failed to update product image.",
                    "error": str(e),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


# ==========================================================
# Product Image Delete API
# ==========================================================

class ProductImageDeleteAPIView(APIView):

    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def delete(self, request, pk):

        try:

            if request.user.role != Account.Role.SELLER:

                return Response(
                    {
                        "message": "Only sellers can delete product images."
                    },
                    status=status.HTTP_403_FORBIDDEN,
                )

            image = get_object_or_404(
                ProductImage.objects.select_related(
                    "product",
                    "product__seller",
                ),
                pk=pk,
                product__seller=request.user.seller_profile,
            )

            image.delete()

            return Response(
                {
                    "message": "Product image deleted successfully."
                },
                status=status.HTTP_200_OK,
            )

        except Exception as e:

            transaction.set_rollback(True)

            return Response(
                {
                    "success": False,
                    "message": "Failed to delete product image.",
                    "error": str(e),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

# ==========================================================
# Product Attribute Create API
# ==========================================================

class ProductAttributeCreateAPIView(APIView):

    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request):

        try:

            if request.user.role != Account.Role.SELLER:

                return Response(
                    {
                        "message": "Only sellers can create product attributes."
                    },
                    status=status.HTTP_403_FORBIDDEN,
                )

            product = get_object_or_404(
                Product,
                pk=request.data.get("product"),
                seller=request.user.seller_profile,
            )

            serializer = ProductAttributeSerializer(
                data=request.data,
                context={"request": request},
            )

            serializer.is_valid(
                raise_exception=True
            )

            attribute = serializer.save(
                product=product
            )

            return Response(
                {
                    "message": "Product attribute created successfully.",
                    "data": ProductAttributeSerializer(
                        attribute,
                        context={"request": request},
                    ).data,
                },
                status=status.HTTP_201_CREATED,
            )

        except ValidationError:
            raise

        except Exception as e:

            transaction.set_rollback(True)

            return Response(
                {
                    "success": False,
                    "message": "Failed to create product attribute.",
                    "error": str(e),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


# ==========================================================
# Product Attribute List API
# ==========================================================

class ProductAttributeListAPIView(APIView):

    permission_classes = [AllowAny]

    def get(self, request):

        product_id = request.query_params.get("product")

        attributes = ProductAttribute.objects.select_related(
            "product"
        )

        if product_id:

            attributes = attributes.filter(
                product_id=product_id
            )

        serializer = ProductAttributeSerializer(
            attributes,
            many=True,
            context={"request": request},
        )

        return Response(
            {
                "message": "Product attributes fetched successfully.",
                "count": attributes.count(),
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


# ==========================================================
# Product Attribute Detail API
# ==========================================================

class ProductAttributeDetailAPIView(APIView):

    permission_classes = [AllowAny]

    def get(self, request, pk):

        attribute = get_object_or_404(
            ProductAttribute.objects.select_related(
                "product"
            ),
            pk=pk,
        )

        serializer = ProductAttributeSerializer(
            attribute,
            context={"request": request},
        )

        return Response(
            {
                "message": "Product attribute fetched successfully.",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

# ==========================================================
# Product Attribute Update API
# ==========================================================

class ProductAttributeUpdateAPIView(APIView):

    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def put(self, request, pk):

        try:

            if request.user.role != Account.Role.SELLER:

                return Response(
                    {
                        "message": "Only sellers can update product attributes."
                    },
                    status=status.HTTP_403_FORBIDDEN,
                )

            attribute = get_object_or_404(
                ProductAttribute.objects.select_related(
                    "product",
                    "product__seller",
                ),
                pk=pk,
                product__seller=request.user.seller_profile,
            )

            serializer = ProductAttributeSerializer(
                attribute,
                data=request.data,
                partial=True,
                context={"request": request},
            )

            serializer.is_valid(
                raise_exception=True
            )

            attribute = serializer.save()

            return Response(
                {
                    "message": "Product attribute updated successfully.",
                    "data": ProductAttributeSerializer(
                        attribute,
                        context={"request": request},
                    ).data,
                },
                status=status.HTTP_200_OK,
            )

        except ValidationError:
            raise

        except Exception as e:

            transaction.set_rollback(True)

            return Response(
                {
                    "success": False,
                    "message": "Failed to update product attribute.",
                    "error": str(e),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


# ==========================================================
# Product Attribute Delete API
# ==========================================================

class ProductAttributeDeleteAPIView(APIView):

    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def delete(self, request, pk):

        try:

            if request.user.role != Account.Role.SELLER:

                return Response(
                    {
                        "message": "Only sellers can delete product attributes."
                    },
                    status=status.HTTP_403_FORBIDDEN,
                )

            attribute = get_object_or_404(
                ProductAttribute.objects.select_related(
                    "product",
                    "product__seller",
                ),
                pk=pk,
                product__seller=request.user.seller_profile,
            )

            attribute.delete()

            return Response(
                {
                    "message": "Product attribute deleted successfully."
                },
                status=status.HTTP_200_OK,
            )

        except Exception as e:

            transaction.set_rollback(True)

            return Response(
                {
                    "success": False,
                    "message": "Failed to delete product attribute.",
                    "error": str(e),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

# ==========================================================
# Product Variant Create API
# ==========================================================

class ProductVariantCreateAPIView(APIView):

    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request):

        try:

            if request.user.role != Account.Role.SELLER:

                return Response(
                    {
                        "message": "Only sellers can create product variants."
                    },
                    status=status.HTTP_403_FORBIDDEN,
                )

            product = get_object_or_404(
                Product,
                pk=request.data.get("product"),
                seller=request.user.seller_profile,
            )

            serializer = ProductVariantSerializer(
                data=request.data,
                context={"request": request},
            )

            serializer.is_valid(
                raise_exception=True
            )

            variant = serializer.save(
                product=product
            )

            return Response(
                {
                    "message": "Product variant created successfully.",
                    "data": ProductVariantSerializer(
                        variant,
                        context={"request": request},
                    ).data,
                },
                status=status.HTTP_201_CREATED,
            )

        except ValidationError:
            raise

        except Exception as e:

            transaction.set_rollback(True)

            return Response(
                {
                    "success": False,
                    "message": "Failed to create product variant.",
                    "error": str(e),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


# ==========================================================
# Product Variant List API
# ==========================================================

class ProductVariantListAPIView(APIView):

    permission_classes = [AllowAny]

    def get(self, request):

        product_id = request.query_params.get("product")

        variants = (
            ProductVariant.objects
            .select_related("product")
            .order_by("variant_name")
        )

        if product_id:

            variants = variants.filter(
                product_id=product_id
            )

        serializer = ProductVariantSerializer(
            variants,
            many=True,
            context={"request": request},
        )

        return Response(
            {
                "message": "Product variants fetched successfully.",
                "count": variants.count(),
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

# ==========================================================
# Product Variant Detail API
# ==========================================================

class ProductVariantDetailAPIView(APIView):

    permission_classes = [AllowAny]

    def get(self, request, pk):

        variant = get_object_or_404(
            ProductVariant.objects.select_related(
                "product"
            ),
            pk=pk,
        )

        serializer = ProductVariantSerializer(
            variant,
            context={"request": request},
        )

        return Response(
            {
                "message": "Product variant fetched successfully.",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


# ==========================================================
# Product Variant Update API
# ==========================================================

class ProductVariantUpdateAPIView(APIView):

    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def put(self, request, pk):

        try:

            if request.user.role != Account.Role.SELLER:

                return Response(
                    {
                        "message": "Only sellers can update product variants."
                    },
                    status=status.HTTP_403_FORBIDDEN,
                )

            variant = get_object_or_404(
                ProductVariant.objects.select_related(
                    "product",
                    "product__seller",
                ),
                pk=pk,
                product__seller=request.user.seller_profile,
            )

            serializer = ProductVariantSerializer(
                variant,
                data=request.data,
                partial=True,
                context={"request": request},
            )

            serializer.is_valid(
                raise_exception=True
            )

            variant = serializer.save()

            return Response(
                {
                    "message": "Product variant updated successfully.",
                    "data": ProductVariantSerializer(
                        variant,
                        context={"request": request},
                    ).data,
                },
                status=status.HTTP_200_OK,
            )

        except ValidationError:
            raise

        except Exception as e:

            transaction.set_rollback(True)

            return Response(
                {
                    "success": False,
                    "message": "Failed to update product variant.",
                    "error": str(e),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


# ==========================================================
# Product Variant Delete API
# ==========================================================

class ProductVariantDeleteAPIView(APIView):

    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def delete(self, request, pk):

        try:

            if request.user.role != Account.Role.SELLER:

                return Response(
                    {
                        "message": "Only sellers can delete product variants."
                    },
                    status=status.HTTP_403_FORBIDDEN,
                )

            variant = get_object_or_404(
                ProductVariant.objects.select_related(
                    "product",
                    "product__seller",
                ),
                pk=pk,
                product__seller=request.user.seller_profile,
            )

            variant.delete()

            return Response(
                {
                    "message": "Product variant deleted successfully."
                },
                status=status.HTTP_200_OK,
            )

        except Exception as e:

            transaction.set_rollback(True)

            return Response(
                {
                    "success": False,
                    "message": "Failed to delete product variant.",
                    "error": str(e),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

# ==========================================================
# Product Inventory Create API
# ==========================================================

class ProductInventoryCreateAPIView(APIView):

    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request):

        try:

            if request.user.role != Account.Role.SELLER:

                return Response(
                    {
                        "message": "Only sellers can create inventory."
                    },
                    status=status.HTTP_403_FORBIDDEN,
                )

            variant = get_object_or_404(
                ProductVariant.objects.select_related(
                    "product",
                    "product__seller",
                ),
                pk=request.data.get("variant"),
                product__seller=request.user.seller_profile,
            )

            serializer = ProductInventorySerializer(
                data=request.data,
                context={"request": request},
            )

            serializer.is_valid(
                raise_exception=True
            )

            inventory = serializer.save(
                variant=variant
            )

            return Response(
                {
                    "message": "Inventory created successfully.",
                    "data": ProductInventorySerializer(
                        inventory,
                        context={"request": request},
                    ).data,
                },
                status=status.HTTP_201_CREATED,
            )

        except ValidationError:
            raise

        except Exception as e:

            transaction.set_rollback(True)

            return Response(
                {
                    "success": False,
                    "message": "Failed to create inventory.",
                    "error": str(e),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


# ==========================================================
# Product Inventory List API
# ==========================================================

class ProductInventoryListAPIView(APIView):

    permission_classes = [AllowAny]

    def get(self, request):

        variant_id = request.query_params.get("variant")

        inventories = (
            ProductInventory.objects
            .select_related(
                "variant",
                "variant__product",
            )
            .order_by(
                "variant__variant_name"
            )
        )

        if variant_id:

            inventories = inventories.filter(
                variant_id=variant_id
            )

        serializer = ProductInventorySerializer(
            inventories,
            many=True,
            context={"request": request},
        )

        return Response(
            {
                "message": "Inventory fetched successfully.",
                "count": inventories.count(),
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

# ==========================================================
# Product Inventory Detail API
# ==========================================================

class ProductInventoryDetailAPIView(APIView):

    permission_classes = [AllowAny]

    def get(self, request, pk):

        inventory = get_object_or_404(
            ProductInventory.objects.select_related(
                "variant",
                "variant__product",
            ),
            pk=pk,
        )

        serializer = ProductInventorySerializer(
            inventory,
            context={"request": request},
        )

        return Response(
            {
                "message": "Inventory fetched successfully.",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


# ==========================================================
# Product Inventory Update API
# ==========================================================

class ProductInventoryUpdateAPIView(APIView):

    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def put(self, request, pk):

        try:

            if request.user.role != Account.Role.SELLER:

                return Response(
                    {
                        "message": "Only sellers can update inventory."
                    },
                    status=status.HTTP_403_FORBIDDEN,
                )

            inventory = get_object_or_404(
                ProductInventory.objects.select_related(
                    "variant",
                    "variant__product",
                    "variant__product__seller",
                ),
                pk=pk,
                variant__product__seller=request.user.seller_profile,
            )

            serializer = ProductInventorySerializer(
                inventory,
                data=request.data,
                partial=True,
                context={"request": request},
            )

            serializer.is_valid(
                raise_exception=True
            )

            inventory = serializer.save()

            return Response(
                {
                    "message": "Inventory updated successfully.",
                    "data": ProductInventorySerializer(
                        inventory,
                        context={"request": request},
                    ).data,
                },
                status=status.HTTP_200_OK,
            )

        except ValidationError:
            raise

        except Exception as e:

            transaction.set_rollback(True)

            return Response(
                {
                    "success": False,
                    "message": "Failed to update inventory.",
                    "error": str(e),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


# ==========================================================
# Product Inventory Delete API
# ==========================================================

class ProductInventoryDeleteAPIView(APIView):

    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def delete(self, request, pk):

        try:

            if request.user.role != Account.Role.SELLER:

                return Response(
                    {
                        "message": "Only sellers can delete inventory."
                    },
                    status=status.HTTP_403_FORBIDDEN,
                )

            inventory = get_object_or_404(
                ProductInventory.objects.select_related(
                    "variant",
                    "variant__product",
                    "variant__product__seller",
                ),
                pk=pk,
                variant__product__seller=request.user.seller_profile,
            )

            inventory.delete()

            return Response(
                {
                    "message": "Inventory deleted successfully."
                },
                status=status.HTTP_200_OK,
            )

        except Exception as e:

            transaction.set_rollback(True)

            return Response(
                {
                    "success": False,
                    "message": "Failed to delete inventory.",
                    "error": str(e),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

# ==========================================================
# My Products API
# ==========================================================

class MyProductsAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        try:

            if request.user.role != Account.Role.SELLER:

                return Response(
                    {
                        "message": "Only sellers can view their products."
                    },
                    status=status.HTTP_403_FORBIDDEN,
                )

            seller = get_object_or_404(
                SellerProfile.objects.select_related(
                    "account"
                ),
                account=request.user,
            )

            products = (
                Product.objects.all()   
                .select_related(
                    "category",
                    "brand",
                )
                .prefetch_related(
                    "images",
                    "attributes",
                    "variants",
                )
                .annotate(
                    average_rating=Avg(
                        "reviews__rating"
                    ),
                    total_reviews=Count(
                        "reviews",
                        distinct=True,
                    ),
                )
                .order_by(
                    "-created_at"
                )
            )

            serializer = ProductSerializer(
                products,
                many=True,
                context={
                    "request": request
                },
            )

            return Response(
                {
                    "message": "Products fetched successfully.",
                    "count": products.count(),
                    "data": serializer.data,
                },
                status=status.HTTP_200_OK,
            )

        except Http404:

            return Response(
                {
                    "message": "Seller profile not found."
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        except Exception as e:

            return Response(
                {
                    "success": False,
                    "message": "Failed to fetch products.",
                    "error": str(e),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )