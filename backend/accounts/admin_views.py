from django.db import transaction
from django.db.models import Q
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Account
from .serializers import AccountSerializer


class AdminUserListAPIView(APIView):

    permission_classes = [IsAdminUser]

    def get(self, request):

        users = Account.objects.all().order_by("-created_at")

        search = request.query_params.get("search", "").strip()

        if search:
            users = users.filter(
                Q(username__icontains=search)
                | Q(first_name__icontains=search)
                | Q(last_name__icontains=search)
                | Q(email__icontains=search)
                | Q(phone__icontains=search)
            )

        role = request.query_params.get("role", "").strip()

        if role:
            users = users.filter(role=role)

        serializer = AccountSerializer(
            users,
            many=True,
            context={"request": request},
        )

        return Response(
            {
                "message": "Users fetched successfully.",
                "count": users.count(),
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


class AdminUserDetailAPIView(APIView):

    permission_classes = [IsAdminUser]

    def get(self, request, pk):

        user = get_object_or_404(
            Account,
            pk=pk,
        )

        serializer = AccountSerializer(
            user,
            context={"request": request},
        )

        return Response(
            {
                "message": "User fetched successfully.",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


class AdminUserUpdateAPIView(APIView):

    permission_classes = [IsAdminUser]

    @transaction.atomic
    def put(self, request, pk):

        try:

            user = get_object_or_404(
                Account,
                pk=pk,
            )

            serializer = AccountSerializer(
                user,
                data=request.data,
                partial=True,
                context={"request": request},
            )

            serializer.is_valid(
                raise_exception=True
            )

            serializer.save()

            return Response(
                {
                    "message": "User updated successfully.",
                    "data": serializer.data,
                },
                status=status.HTTP_200_OK,
            )

        except Exception as e:

            transaction.set_rollback(True)

            return Response(
                {
                    "success": False,
                    "message": "Failed to update user.",
                    "error": str(e),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class AdminUserDeleteAPIView(APIView):

    permission_classes = [IsAdminUser]

    @transaction.atomic
    def delete(self, request, pk):

        try:

            user = get_object_or_404(
                Account,
                pk=pk,
            )

            if user == request.user:
                return Response(
                    {
                        "message": "You cannot delete your own account."
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            user.delete()

            return Response(
                {
                    "message": "User deleted successfully."
                },
                status=status.HTTP_200_OK,
            )

        except Exception as e:

            transaction.set_rollback(True)

            return Response(
                {
                    "success": False,
                    "message": "Failed to delete user.",
                    "error": str(e),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class AdminUserStatusAPIView(APIView):

    permission_classes = [IsAdminUser]

    @transaction.atomic
    def patch(self, request, pk):

        try:

            user = get_object_or_404(
                Account,
                pk=pk,
            )

            if user == request.user:
                return Response(
                    {
                        "message": "You cannot change your own account status."
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            user.is_active = not user.is_active

            user.save(
                update_fields=["is_active"]
            )

            return Response(
                {
                    "message": (
                        "User activated successfully."
                        if user.is_active
                        else
                        "User deactivated successfully."
                    ),
                    "data": {
                        "id": user.id,
                        "is_active": user.is_active,
                    },
                },
                status=status.HTTP_200_OK,
            )

        except Exception as e:

            transaction.set_rollback(True)

            return Response(
                {
                    "success": False,
                    "message": "Failed to update user status.",
                    "error": str(e),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class AdminUserCreateAPIView(APIView):

    permission_classes = [IsAdminUser]

    @transaction.atomic
    def post(self, request):

        try:

            serializer = AccountSerializer(
                data=request.data,
                context={"request": request},
            )

            serializer.is_valid(
                raise_exception=True
            )

            serializer.save()

            return Response(
                {
                    "message": "User created successfully.",
                    "data": serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )

        except Exception as e:

            transaction.set_rollback(True)

            return Response(
                {
                    "success": False,
                    "message": "Failed to create user.",
                    "error": str(e),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )