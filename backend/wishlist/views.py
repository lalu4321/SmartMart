from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import Wishlist
from .serializers import WishlistSerializer

from products.models import Product

class WishlistCreateAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        try:

            serializer = WishlistSerializer(
                data=request.data
            )

            serializer.is_valid(raise_exception=True)

            product = serializer.validated_data["product"]

            if Wishlist.objects.filter(
                account=request.user,
                product=product
            ).exists():

                return Response(
                    {
                        "message": "Product already exists in wishlist."
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            wishlist = serializer.save(
                account=request.user
            )

            return Response(
                {
                    "message": "Product added to wishlist successfully.",
                    "data": WishlistSerializer(wishlist).data
                },
                status=status.HTTP_201_CREATED
            )

        except Exception as e:

            return Response(
                {
                    "success": False,
                    "message": "Failed to add product to wishlist.",
                    "error": str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
class WishlistListAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        wishlist = Wishlist.objects.filter(
            account=request.user
        )

        serializer = WishlistSerializer(
            wishlist,
            many=True,
            context={"request": request}
        )

        return Response(
            {
                "message": "Wishlist fetched successfully.",
                "count": wishlist.count(),
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )

class WishlistDeleteAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):

        try:

            wishlist = get_object_or_404(
                Wishlist,
                pk=pk,
                account=request.user
            )

            wishlist.delete()

            return Response(
                {
                    "message": "Wishlist item removed successfully."
                },
                status=status.HTTP_200_OK
            )

        except Exception as e:

            return Response(
                {
                    "success": False,
                    "message": "Failed to remove wishlist item.",
                    "error": str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
class WishlistClearAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def delete(self, request):

        try:

            Wishlist.objects.filter(
                account=request.user
            ).delete()

            return Response(
                {
                    "success": True,
                    "message": "Wishlist cleared successfully."
                },
                status=status.HTTP_200_OK
            )

        except Exception as e:

            return Response(
                {
                    "success": False,
                    "message": "Failed to clear wishlist.",
                    "error": str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
class WishlistDetailAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, pk):

        wishlist = get_object_or_404(
            Wishlist,
            pk=pk,
            account=request.user
        )

        serializer = WishlistSerializer(
            wishlist
        )

        return Response(
            {
                "message": "Wishlist item fetched successfully.",
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )