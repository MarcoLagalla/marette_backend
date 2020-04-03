from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.authtoken.models import Token

from django.contrib.auth.models import User

from ..models import Customer, Business
from .serializers import CustomerSerializer, BusinessSerializer, CustomerRegistationSerializer, LoginSerializer, \
    BusinessRegistationSerializer, ChangePasswordSerializer
from ..permissions import IsOwnerOrReadOnly, IsPostOrIsAdmin


class ListUsersAPIView(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAdminUser]

    def get(self, request):
        customers = Customer.objects.all().order_by('id')
        customers_serializer = CustomerSerializer(customers, many=True)

        businesses = Business.objects.all().order_by('id')
        businesses_serializer = BusinessSerializer(businesses, many=True)

        serializer = list(customers_serializer.data)
        serializer += list(businesses_serializer.data)
        return Response(serializer, status=status.HTTP_200_OK)


class CustomerAPIView(APIView):

    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsPostOrIsAdmin]

    # only admin can list all users details
    def get(self, request):
        customers = Customer.objects.all().order_by('id')
        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # non authenticated users can create a new user
    def post(self, request):
        serializer = CustomerRegistationSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            if not request.user.is_authenticated:
                customer = serializer.save()
                data['response'] = "successfully registered a new customer user"
                data['username'] = customer.user.username
                data['email'] = customer.user.email
                data['token'] = Token.objects.create(user=customer.user).key
                return Response(data, status=status.HTTP_201_CREATED)
            else:
                data['error'] = "already registered"
            return Response(data, status=status.HTTP_403_FORBIDDEN)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BusinessAPIView(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsPostOrIsAdmin]

    # only admin can list all users details
    def get(self, request):
        businesses = Business.objects.all().order_by('id')
        serializer = BusinessSerializer(businesses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # non authenticated users can create a new user
    def post(self, request):
        serializer = BusinessRegistationSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            if not request.user.is_authenticated:
                business = serializer.save()
                data['response'] = "successfully registered a new business user"
                data['username'] = business.user.username
                data['email'] = business.user.email
                data['token'] = Token.objects.create(user=business.user).key
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
            request.user.auth_token.delete()
            data['logout'] = 'user successfully logged out'
        except (AttributeError, ObjectDoesNotExist):
            data['error'] = 'user not logged in'
            return Response(data, status=status.HTTP_204_NO_CONTENT)
        return Response(data, status=status.HTTP_200_OK)


class UpdatePassword(APIView):
    """
    An endpoint for changing password.
    """
    permission_classes = [IsAuthenticated]

    def get_object(self, id, queryset=None):
        return User.objects.get(id=id)

    def put(self, request, id):
        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():

            user_to_update = User.objects.get(id=id)
            # print(user_to_update.username, user_to_update.id, user_to_update.user.id)
            token = Token.objects.get(user_id=user_to_update.id).key

            if request.user.auth_token.key == token:
                # Check old password
                old_password = serializer.data.get("old_password")
                if not user_to_update.check_password(old_password):
                    return Response({"old_password": ["Wrong password."]},
                                    status=status.HTTP_400_BAD_REQUEST)

                # delete auth token
                request.user.auth_token.delete()

                # set_password also hashes the password that the user will get
                user_to_update.set_password(serializer.data.get("new_password"))
                user_to_update.save()

                data = {}
                data['password'] = 'password changed'
                # get new token
                data['token'] = Token.objects.create(user=user_to_update).key
                return Response(data, status=status.HTTP_200_OK)
            else:

                data = {}
                data['error'] = 'invalid authorization token'
                return Response(data, status=status.HTTP_403_FORBIDDEN)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
