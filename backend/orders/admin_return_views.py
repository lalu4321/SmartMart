from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework import status

from .models import (
    ReturnRequest,
)

from .admin_return_serializers import (
    AdminReturnSerializer,
    AdminRefundSerializer,
)


# ==========================================
# Admin Return List
# ==========================================

class AdminReturnListAPIView(APIView):

    permission_classes = [IsAdminUser]

    def get(self, request):

        returns = ReturnRequest.objects.select_related(
            "order",
            "order__account"
        ).order_by("-requested_at")

        search = request.query_params.get("search")

        if search:

            returns = returns.filter(
                order__order_number__icontains=search
            ) | returns.filter(
                order__account__username__icontains=search
            )

        status_filter = request.query_params.get("status")

        if status_filter:

            returns = returns.filter(
                status=status_filter
            )

        serializer = AdminReturnSerializer(
            returns,
            many=True
        )

        return Response(
            {
                "message": "Return requests fetched successfully.",
                "count": returns.count(),
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


# ==========================================
# Admin Return Detail
# ==========================================

class AdminReturnDetailAPIView(APIView):

    permission_classes = [IsAdminUser]

    def get(self, request, pk):

        return_request = get_object_or_404(
            ReturnRequest.objects.select_related(
                "order",
                "order__account"
            ),
            pk=pk
        )

        serializer = AdminReturnSerializer(
            return_request
        )

        return Response(
            {
                "message": "Return request fetched successfully.",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

from notifications.models import Notification


# ==========================================
# Admin Approve Return
# ==========================================

class AdminApproveReturnAPIView(APIView):

    permission_classes = [IsAdminUser]

    def patch(self, request, pk):

        try:

            return_request = get_object_or_404(
                ReturnRequest,
                pk=pk
            )

            if (
                return_request.status
                == ReturnRequest.ReturnStatus.APPROVED
            ):

                return Response(
                    {
                        "message": "Return request is already approved."
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            return_request.status = (
                ReturnRequest.ReturnStatus.APPROVED
            )

            return_request.save(
                update_fields=["status"]
            )

            Notification.objects.create(
                account=return_request.order.account,
                title="Return Request Approved",
                message=(
                    f"Your return request for "
                    f"{return_request.order.order_number} "
                    f"has been approved."
                ),
                notification_type=(
                    Notification.NotificationType.RETURN
                ),
            )

            return Response(
                {
                    "message": "Return request approved successfully.",
                    "data": AdminReturnSerializer(
                        return_request
                    ).data,
                },
                status=status.HTTP_200_OK,
            )

        except Exception as e:

            return Response(
                {
                    "success": False,
                    "message": "Failed to approve return request.",
                    "error": str(e),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


# ==========================================
# Admin Reject Return
# ==========================================

class AdminRejectReturnAPIView(APIView):

    permission_classes = [IsAdminUser]

    def patch(self, request, pk):

        try:

            return_request = get_object_or_404(
                ReturnRequest,
                pk=pk
            )

            if (
                return_request.status
                == ReturnRequest.ReturnStatus.REJECTED
            ):

                return Response(
                    {
                        "message": "Return request is already rejected."
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            return_request.status = (
                ReturnRequest.ReturnStatus.REJECTED
            )

            return_request.save(
                update_fields=["status"]
            )

            Notification.objects.create(
                account=return_request.order.account,
                title="Return Request Rejected",
                message=(
                    f"Your return request for "
                    f"{return_request.order.order_number} "
                    f"has been rejected."
                ),
                notification_type=(
                    Notification.NotificationType.RETURN
                ),
            )

            return Response(
                {
                    "message": "Return request rejected successfully.",
                    "data": AdminReturnSerializer(
                        return_request
                    ).data,
                },
                status=status.HTTP_200_OK,
            )

        except Exception as e:

            return Response(
                {
                    "success": False,
                    "message": "Failed to reject return request.",
                    "error": str(e),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

from django.utils import timezone

from .models import Refund


# ==========================================
# Admin Refund List
# ==========================================

class AdminRefundListAPIView(APIView):

    permission_classes = [IsAdminUser]

    def get(self, request):

        refunds = Refund.objects.select_related(
            "return_request",
            "return_request__order",
            "return_request__order__account"
        ).order_by("-created_at")

        search = request.query_params.get("search")

        if search:

            refunds = refunds.filter(
                return_request__order__order_number__icontains=search
            ) | refunds.filter(
                return_request__order__account__username__icontains=search
            )

        status_filter = request.query_params.get("status")

        if status_filter:

            refunds = refunds.filter(
                status=status_filter
            )

        serializer = AdminRefundSerializer(
            refunds,
            many=True
        )

        return Response(
            {
                "message": "Refunds fetched successfully.",
                "count": refunds.count(),
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


# ==========================================
# Admin Refund Detail
# ==========================================

class AdminRefundDetailAPIView(APIView):

    permission_classes = [IsAdminUser]

    def get(self, request, pk):

        refund = get_object_or_404(
            Refund.objects.select_related(
                "return_request",
                "return_request__order",
                "return_request__order__account"
            ),
            pk=pk
        )

        serializer = AdminRefundSerializer(
            refund
        )

        return Response(
            {
                "message": "Refund fetched successfully.",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


# ==========================================
# Admin Complete Refund
# ==========================================

class AdminCompleteRefundAPIView(APIView):

    permission_classes = [IsAdminUser]

    def patch(self, request, pk):

        try:

            refund = get_object_or_404(
                Refund,
                pk=pk
            )

            if refund.status == Refund.RefundStatus.COMPLETED:

                return Response(
                    {
                        "message": "Refund already completed."
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            refund.status = Refund.RefundStatus.COMPLETED

            refund.refunded_at = timezone.now()

            refund.save(
                update_fields=[
                    "status",
                    "refunded_at",
                ]
            )

            Notification.objects.create(
                account=refund.return_request.order.account,
                title="Refund Completed",
                message=(
                    f"Refund for Order "
                    f"{refund.return_request.order.order_number} "
                    f"has been completed."
                ),
                notification_type=(
                    Notification.NotificationType.PAYMENT
                ),
            )

            return Response(
                {
                    "message": "Refund completed successfully.",
                    "data": AdminRefundSerializer(
                        refund
                    ).data,
                },
                status=status.HTTP_200_OK,
            )

        except Exception as e:

            return Response(
                {
                    "success": False,
                    "message": "Failed to complete refund.",
                    "error": str(e),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )