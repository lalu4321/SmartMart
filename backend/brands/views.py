from django.shortcuts import get_object_or_404
from django.utils.text import slugify
from rest_framework.exceptions import ValidationError

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import Brand
from .serializers import BrandSerializer

def generate_unique_slug(name, instance=None):

    slug = slugify(name)
    unique_slug = slug
    counter = 1

    while Brand.objects.filter(
        slug=unique_slug
    ).exclude(
        pk=instance.pk if instance else None
    ).exists():

        unique_slug = f"{slug}-{counter}"
        counter += 1

    return unique_slug


class BrandCreateAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        try:

            serializer = BrandSerializer(data=request.data)

            serializer.is_valid(raise_exception=True)

            name = serializer.validated_data["name"]

            brand = serializer.save(
                slug=generate_unique_slug(name)
            )

            return Response(
                {
                    "message": "Brand created successfully.",
                    "data": BrandSerializer(brand).data
                },
                status=status.HTTP_201_CREATED
            )

        except ValidationError:
            raise

        except Exception as e:
            return Response(
                {
                    "success": False,
                    "message": "Failed to create brand.",
                    "error": str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
class BrandListAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        brands = Brand.objects.filter(is_active=True)

        serializer = BrandSerializer(
            brands,
            many=True
        )

        return Response(
            {
                "message": "Brands fetched successfully.",
                "count": brands.count(),
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )
    
class BrandDetailAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, pk):

        brand = get_object_or_404(
            Brand,
            pk=pk,
            is_active=True
        )

        serializer = BrandSerializer(brand)

        return Response(
            {
                "message": "Brand fetched successfully.",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

class BrandUpdateAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def put(self, request, pk):

        try:

            brand = get_object_or_404(
                Brand,
                pk=pk
            )

            serializer = BrandSerializer(
                brand,
                data=request.data,
                partial=True
            )

            serializer.is_valid(raise_exception=True)

            brand = serializer.save()

            if "name" in serializer.validated_data:
                brand.slug = generate_unique_slug(
                    brand.name,
                    brand
                )
                brand.save(update_fields=["slug"])

            return Response(
                {
                    "message": "Brand updated successfully.",
                    "data": BrandSerializer(brand).data,
                },
                status=status.HTTP_200_OK,
            )

        except ValidationError:
            raise

        except Exception as e:
            return Response(
                {
                    "success": False,
                    "message": "Failed to update brand.",
                    "error": str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
class BrandDeleteAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):

        try:

            brand = get_object_or_404(
                Brand,
                pk=pk
            )

            brand.delete()

            return Response(
                {
                    "message": "Brand deleted successfully."
                },
                status=status.HTTP_200_OK
            )

        except ValidationError:
            raise

        except Exception as e:
            return Response(
                {
                    "success": False,
                    "message": "Failed to delete brand.",
                    "error": str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )