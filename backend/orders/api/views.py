import django
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from backend.account.permissions import IsBusiness
from rest_framework.authentication import TokenAuthentication, SessionAuthentication

from backend.account.models import Business
from ..models import OrderNotification
from .serializers import OrderNotificationSerialzier

from django.core.paginator import Paginator


class AllNotifications(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsBusiness, IsAuthenticated]

    def get(self, request):

        try:
            business = Business.objects.all().get(user=request.user)
        except Business.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        notifications = OrderNotification.objects.all().filter(recipient=business.user).order_by('issued')
        # -----------------------------------------------------------
        page_number = request.query_params.get('page_number', 1)
        page_size = request.query_params.get('page_size', 10)

        try:
            paginator = Paginator(notifications, page_size)
            page = paginator.page(page_number)
        except django.core.paginator.EmptyPage:
            page = paginator.page(1)

        serializer = OrderNotificationSerialzier(page, many=True, context={'request': request})
        # -----------------------------------------------------------

        return Response(serializer.data, status=status.HTTP_200_OK)


class UnReadCount(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsBusiness, IsAuthenticated]

    def get(self, request):

        try:
            business = Business.objects.all().get(user=request.user)
        except Business.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        notifications = OrderNotification.objects.all().filter(recipient=business.user).filter(status__iexact='U')

        data = {'unread_count': notifications.count()}
        return Response(data, status=status.HTTP_200_OK)


class UnReadList(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsBusiness, IsAuthenticated]

    def get(self, request):

        try:
            business = Business.objects.all().get(user=request.user)
        except Business.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        notifications = OrderNotification.objects.all().filter(recipient=business.user).filter(status__iexact='U')
        serializer = OrderNotificationSerialzier(notifications, many=True)

        data = {'unread_count': notifications.count()}
        data.update({'notifications': serializer.data})
        return Response(data, status=status.HTTP_200_OK)


class MarkAsRead(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsBusiness, IsAuthenticated]

    def post(self, request, id):

        try:
            business = Business.objects.all().get(user=request.user)
        except Business.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        try:
            notification = OrderNotification.objects.all().filter(recipient=business.user).get(id=id)
        except OrderNotification.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if notification.status == 'U':
            notification.status = 'R'
            notification.save()
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = OrderNotificationSerialzier(notification)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MarkAsUnread(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsBusiness, IsAuthenticated]

    def post(self, request, id):

        try:
            business = Business.objects.all().get(user=request.user)
        except Business.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        try:
            notification = OrderNotification.objects.all().filter(recipient=business.user).get(id=id)
        except OrderNotification.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if notification.status == 'R':
            notification.status = 'U'
            notification.save()
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = OrderNotificationSerialzier(notification)
        return Response(serializer.data, status=status.HTTP_200_OK)