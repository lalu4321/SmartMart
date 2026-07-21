from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from django.utils.text import slugify

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import Category
from .serializers import CategorySerializer


def generate_unique_slug(name, instance=None):

    slug = slugify(name)
    unique_slug = slug
    counter = 1

    while Category.objects.filter(
        slug=unique_slug
    ).exclude(
        pk=instance.pk if instance else None
    ).exists():

        unique_slug = f"{slug}-{counter}"
        counter += 1

    return unique_slug


class CategoryCreateAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        try:

            serializer = CategorySerializer(data=request.data)

            if serializer.is_valid():

                name = serializer.validated_data["name"]

                category = serializer.save(
                    slug=generate_unique_slug(name)
                )

                return Response(
                    {
                        "message": "Category created successfully.",
                        "data": CategorySerializer(category).data
                    },
                    status=status.HTTP_201_CREATED
                )

            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        except Exception as e:

            return Response(
                {
                    "success": False,
                    "message": "Failed to create category.",
                    "error": str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class CategoryListAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        categories = Category.objects.filter(is_active=True)

        serializer = CategorySerializer(
            categories,
            many=True
        )

        return Response(
            {
                "message": "Categories fetched successfully.",
                "count": categories.count(),
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


class CategoryDetailAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, pk):

        category = get_object_or_404(
            Category,
            pk=pk,
            is_active=True
        )

        serializer = CategorySerializer(category)

        return Response(
            {
                "message": "Category fetched successfully.",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

class CategoryUpdateAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def put(self, request, pk):

        try:

            category = get_object_or_404(
                Category,
                pk=pk
            )

            serializer = CategorySerializer(
                category,
                data=request.data,
                partial=True
            )

            serializer.is_valid(raise_exception=True)

            category = serializer.save()

            if "name" in serializer.validated_data:
                category.slug = generate_unique_slug(
                    category.name,
                    category
                )
                category.save(update_fields=["slug"])

            return Response(
                {
                    "message": "Category updated successfully.",
                    "data": CategorySerializer(category).data,
                },
                status=status.HTTP_200_OK,
            )

        except ValidationError:
            raise

        except Exception as e:
            return Response(
                {
                    "success": False,
                    "message": "Failed to update category.",
                    "error": str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class CategoryDeleteAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):

        try:

            category = get_object_or_404(
                Category,
                pk=pk
            )

            category.delete()

            return Response(
                {
                    "message": "Category deleted successfully."
                },
                status=status.HTTP_200_OK
            )

        except ValidationError:
            raise

        except Exception as e:
            return Response(
                {
                    "success": False,
                    "message": "Failed to delete category.",
                    "error": str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )