from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Address,SellerProfile,Account
from .serializers import AccountSerializer,AddressSerializer,SellerProfileSerializer
from django.shortcuts import get_object_or_404


from rest_framework.exceptions import ValidationError

class RegisterAPIView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):

        try:

            serializer = AccountSerializer(data=request.data)

            if serializer.is_valid():
                serializer.save()

                return Response(
                    {
                        "message": "Account created successfully.",
                        "data": serializer.data,
                    },
                    status=status.HTTP_201_CREATED,
                )

            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

        except ValidationError:
            raise

        except Exception as e:
            return Response(
                {
                    "success": False,
                    "message": "Failed to create account.",
                    "error": str(e),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

class ProfileAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        return Response(
            {
                "id": request.user.id,
                "username": request.user.username,
                "first_name": request.user.first_name,
                "last_name": request.user.last_name,
                "email": request.user.email,
                "phone": request.user.phone,
                "role": request.user.role,
                "gender": request.user.gender,
            },
            status=status.HTTP_200_OK,
        )

class UpdateProfileAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def put(self, request):

        try:

            serializer = AccountSerializer(
                request.user,
                data=request.data,
                partial=True,
            )

            serializer.is_valid(raise_exception=True)

            serializer.save()

            return Response(
                {
                    "message": "Profile updated successfully.",
                    "data": serializer.data,
                },
                status=status.HTTP_200_OK,
            )

        except ValidationError:
            raise

        except Exception as e:
            return Response(
                {
                    "success": False,
                    "message": "Failed to update profile.",
                    "error": str(e),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        
class AddressCreateAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        try:

            serializer = AddressSerializer(data=request.data)

            serializer.is_valid(raise_exception=True)

            serializer.save(account=request.user)

            return Response(
                {
                    "message": "Address added successfully.",
                    "data": serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )

        except ValidationError:
            raise

        except Exception as e:
            return Response(
                {
                    "success": False,
                    "message": "Failed to add address.",
                    "error": str(e),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

class AddressListAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        addresses = Address.objects.filter(account=request.user)

        serializer = AddressSerializer(
            addresses,
            many=True
        )

        return Response(
            {
                "message": "Addresses fetched successfully.",
                "count": addresses.count(),
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

class AddressDetailAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, pk):

        address = get_object_or_404(
            Address,
            pk=pk,
            account=request.user
        )

        serializer = AddressSerializer(address)

        return Response(
            {
                "message": "Address fetched successfully.",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )
    
class AddressUpdateAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def put(self, request, pk):

        try:

            address = get_object_or_404(
                Address,
                pk=pk,
                account=request.user
            )

            serializer = AddressSerializer(
                address,
                data=request.data,
                partial=True
            )

            if serializer.is_valid():

                serializer.save()

                return Response(
                    {
                        "message": "Address updated successfully.",
                        "data": serializer.data
                    },
                    status=status.HTTP_200_OK
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
                    "message": "Failed to update address.",
                    "error": str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
class AddressDeleteAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):

        try:

            address = get_object_or_404(
                Address,
                pk=pk,
                account=request.user
            )

            address.delete()

            return Response(
                {
                    "message": "Address deleted successfully."
                },
                status=status.HTTP_204_NO_CONTENT
            )

        except ValidationError:
            raise

        except Exception as e:
            return Response(
                {
                    "success": False,
                    "message": "Failed to delete address.",
                    "error": str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class SetDefaultAddressAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):

        address = get_object_or_404(
            Address,
            pk=pk,
            account=request.user
        )

        # Remove default from all addresses of this user
        Address.objects.filter(
            account=request.user,
            is_default=True
        ).update(is_default=False)

        # Set selected address as default
        address.is_default = True
        address.save()

        serializer = AddressSerializer(address)

        return Response(
            {
                "message": "Default address updated successfully.",
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )

class SellerProfileCreateAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        try:

            if request.user.role != Account.Role.SELLER:
                return Response(
                    {
                        "message": "Only sellers can create a seller profile."
                    },
                    status=status.HTTP_403_FORBIDDEN
                )

            if SellerProfile.objects.filter(account=request.user).exists():
                return Response(
                    {
                        "message": "Seller profile already exists."
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            serializer = SellerProfileSerializer(data=request.data)

            if serializer.is_valid():

                serializer.save(account=request.user)

                return Response(
                    {
                        "message": "Seller profile created successfully.",
                        "data": serializer.data
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
                    "message": "Failed to create seller profile.",
                    "error": str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
class SellerProfileAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        seller = get_object_or_404(
            SellerProfile,
            account=request.user
        )

        serializer = SellerProfileSerializer(seller)

        return Response(
            {
                "message": "Seller profile fetched successfully.",
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )

class SellerProfileUpdateAPIView(APIView):


    permission_classes = [IsAuthenticated]

    def put(self, request):

        try:

            seller = get_object_or_404(
                SellerProfile,
                account=request.user
            )

            serializer = SellerProfileSerializer(
                seller,
                data=request.data,
                partial=True
            )

            serializer.is_valid(raise_exception=True)

            serializer.save()

            return Response(
                {
                    "message": "Seller profile updated successfully.",
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
                    "message": "Failed to update seller profile.",
                    "error": str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
class SellerProfileDeleteAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def delete(self, request):

        try:

            seller = get_object_or_404(
                SellerProfile,
                account=request.user
            )

            seller.delete()

            return Response(
                {
                    "message": "Seller profile deleted successfully."
                },
                status=status.HTTP_204_NO_CONTENT
            )

        except Exception as e:
            return Response(
                {
                    "success": False,
                    "message": "Failed to delete seller profile.",
                    "error": str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )