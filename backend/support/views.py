from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import (
    SupportTicket,
    TicketReply,
)

from .serializers import (
    SupportTicketSerializer,
    TicketReplySerializer,
)

class SupportTicketCreateAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = SupportTicketSerializer(
            data=request.data
        )

        serializer.is_valid(raise_exception=True)

        ticket = serializer.save(
            account=request.user
        )

        return Response(
            {
                "message": "Support ticket created successfully.",
                "data": SupportTicketSerializer(ticket).data
            },
            status=status.HTTP_201_CREATED
        )
    
class SupportTicketListAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        tickets = SupportTicket.objects.filter(
            account=request.user
        )

        serializer = SupportTicketSerializer(
            tickets,
            many=True
        )

        return Response(
            {
                "message": "Support tickets fetched successfully.",
                "count": tickets.count(),
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )
    
class SupportTicketDetailAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, pk):

        ticket = get_object_or_404(
            SupportTicket,
            pk=pk,
            account=request.user
        )

        serializer = SupportTicketSerializer(
            ticket
        )

        return Response(
            {
                "message": "Support ticket fetched successfully.",
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )

class SupportTicketUpdateAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def put(self, request, pk):

        ticket = get_object_or_404(
            SupportTicket,
            pk=pk,
            account=request.user
        )

        if ticket.status == SupportTicket.Status.CLOSED:

            return Response(
                {
                    "message": "Closed tickets cannot be updated."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = SupportTicketSerializer(
            ticket,
            data=request.data,
            partial=True
        )

        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(
            {
                "message": "Support ticket updated successfully.",
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )
    
class SupportTicketCloseAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def put(self, request, pk):

        ticket = get_object_or_404(
            SupportTicket,
            pk=pk,
            account=request.user
        )

        ticket.status = SupportTicket.Status.CLOSED

        ticket.save()

        return Response(
            {
                "message": "Support ticket closed successfully."
            },
            status=status.HTTP_200_OK
        )
    
class AdminSupportTicketListAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        if request.user.role != "ADMIN":

            return Response(
                {
                    "message": "Only admin can access this."
                },
                status=status.HTTP_403_FORBIDDEN
            )

        tickets = SupportTicket.objects.all()

        serializer = SupportTicketSerializer(
            tickets,
            many=True
        )

        return Response(
            {
                "message": "Support tickets fetched successfully.",
                "count": tickets.count(),
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )
    
class AdminSupportTicketDetailAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, pk):

        if request.user.role != "ADMIN":

            return Response(
                {
                    "message": "Only admin can access this."
                },
                status=status.HTTP_403_FORBIDDEN
            )

        ticket = get_object_or_404(
            SupportTicket,
            pk=pk
        )

        serializer = SupportTicketSerializer(ticket)

        return Response(
            {
                "message": "Support ticket fetched successfully.",
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )
    
class TicketReplyAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, pk):

        if request.user.role != "ADMIN":

            return Response(
                {
                    "message": "Only admin can reply."
                },
                status=status.HTTP_403_FORBIDDEN
            )

        ticket = get_object_or_404(
            SupportTicket,
            pk=pk
        )

        serializer = TicketReplySerializer(
            data=request.data
        )

        serializer.is_valid(raise_exception=True)

        reply = serializer.save(
            ticket=ticket,
            account=request.user
        )

        return Response(
            {
                "message": "Reply added successfully.",
                "data": TicketReplySerializer(reply).data
            },
            status=status.HTTP_201_CREATED
        )
    
class UpdateTicketStatusAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def put(self, request, pk):

        if request.user.role != "ADMIN":

            return Response(
                {
                    "message": "Only admin can update ticket status."
                },
                status=status.HTTP_403_FORBIDDEN
            )

        ticket = get_object_or_404(
            SupportTicket,
            pk=pk
        )

        status_value = request.data.get("status")

        if status_value not in SupportTicket.Status.values:

            return Response(
                {
                    "message": "Invalid status."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        ticket.status = status_value

        ticket.save()

        return Response(
            {
                "message": "Ticket status updated successfully.",
                "data": SupportTicketSerializer(ticket).data
            },
            status=status.HTTP_200_OK
        )
    
