from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.authtoken.models import Token

from django.contrib.auth.models import User

from ..models import Customer
from .serializers import CustomerSerializer, CustomerRegistationSerializer, LoginSerializer
from ..permissions import IsOwnerOrReadOnly, IsPostOrIsAdmin


class CustomerAPIView(APIView):

    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsPostOrIsAdmin]

    # only admin can list all users details
    def get(self, request):
        customers = Customer.objects.all()
        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # non authenticated users can create a new user
    def post(self, request):
        serializer = CustomerRegistationSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            if not request.user.auth_token:
                customer = serializer.save()
                data['response'] = "successfully registered a new user"
                data['username'] = customer.user.username
                data['email'] = customer.user.email
                data['token'] = Token.objects.get(user=customer.user).key
                return Response(data, status=status.HTTP_201_CREATED)
        else:
            data['error'] = "already registered"
            return Response(data, status=status.HTTP_403_FORBIDDEN)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginGetToken(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = {}
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = request.data['email']
            password = request.data['password']
            try:
                user = User.objects.get(email__iexact=email)
                if user:
                    if user.check_password(password):
                        # successfully logged in
                        if not Token.objects.all().filter(user=user):
                            token = Token.objects.create(user=user).key
                            data['token'] = token
                            return Response(data, status=status.HTTP_200_OK)
                        else:
                            token = Token.objects.get(user=user).key
                            data['token'] = token
                            return Response(data, status=status.HTTP_200_OK)
                    else:
                        data['error'] = 'invalid password for this user'
                        return Response(data, status=status.HTTP_400_BAD_REQUEST)
            except User.DoesNotExist:
                data['error'] = 'no existing user with this email'
                return Response(data, status=status.HTTP_400_BAD_REQUEST)

        data['error'] = 'invalid login data'
        return Response(data, status=status.HTTP_400_BAD_REQUEST)


class LogoutAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        return self.logout(request)

    def logout(self, request):
        data = {}
        try:
            print(request.user.auth_token)
            request.user.auth_token.delete()
            data['logout'] = 'user successfully logged out'
        except (AttributeError, ObjectDoesNotExist):
            data['error'] = 'user not logged in'
            return Response(data, status=status.HTTP_204_NO_CONTENT)
        return Response(data, status=status.HTTP_200_OK)

