from django.contrib.auth.models import User, update_last_login
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import CustomerSerializer, BusinessSerializer, LoginSerializer, \
    ChangePasswordSerializer, ResetPasswordSerializer, AskResetPasswordSerializer
from ..models import Customer, Business
from ..tokens import account_activation_token, passwordreset_token
from ..views import send_welcome_email, send_reset_email


class ListUsersAPIView(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAdminUser]

    def get(self, request):
        customers = Customer.objects.all().order_by('user')
        customers_serializer = CustomerSerializer(customers, many=True)

        businesses = Business.objects.all().order_by('user')
        businesses_serializer = BusinessSerializer(businesses, many=True)

        serializer = list(customers_serializer.data)
        serializer += list(businesses_serializer.data)
        return Response(serializer, status=status.HTTP_200_OK)


class CustomerAPIView(APIView):

    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [AllowAny]

    # non authenticated users can create a new user
    def post(self, request):
        serializer = CustomerSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            if (not request.user.is_authenticated) or request.user.is_superuser:
                try:
                    customer = serializer.save()
                    activation_token = account_activation_token.make_token(customer.user)
                    send_welcome_email(customer.user, activation_token)
                    data['response'] = "Utente corretamente registrato."
                    data['username'] = customer.user.username
                    data['id'] = customer.user.id
                    data['email'] = customer.user.email
                    data['token'] = Token.objects.create(user=customer.user).key
                    return Response(data, status=status.HTTP_201_CREATED)
                except:
                    data['error'] = ["Errore generico."]
                    return Response(data, status=status.HTTP_403_FORBIDDEN)
            else:
                data['error'] = ["L'utente è già registrato."]
            return Response(data, status=status.HTTP_403_FORBIDDEN)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BusinessAPIView(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [AllowAny]

    # non authenticated users can create a new user
    def post(self, request):
        serializer = BusinessSerializer(data=request.data)
        data = {}
        if serializer.is_valid():

            if (not request.user.is_authenticated) or request.user.is_superuser:

                business = serializer.save()
                print(serializer.validated_data)

                activation_token = account_activation_token.make_token(business.user)
                send_welcome_email(business.user, activation_token)
                data['response'] = "Utente correttamente registrato."
                data['username'] = business.user.username
                data['id'] = business.user.id
                data['email'] = business.user.email
                data['token'] = Token.objects.create(user=business.user).key
                return Response(data, status=status.HTTP_201_CREATED)

            else:
                data['error'] = ["L'utente è già registrato."]
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
                        update_last_login(None, user)
                        if not Token.objects.all().filter(user=user):
                            token = Token.objects.create(user=user).key
                            data['token'] = token
                            data['id'] = user.id
                            return Response(data, status=status.HTTP_200_OK)
                        else:
                            token = Token.objects.get(user=user).key
                            data['token'] = token
                            data['id'] = user.id
                            return Response(data, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                data['error'] = ["L'utente non esiste."]
                return Response(data, status=status.HTTP_400_BAD_REQUEST)

        data['error'] = ["Credenziali sbagliate."]
        return Response(data, status=status.HTTP_400_BAD_REQUEST)


class LogoutAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        return self.logout(request)

    def logout(self, request):
        data = {}
        try:
            request.user.auth_token.delete()
            data['logout'] = 'Logout effettuato.'
        except (AttributeError, ObjectDoesNotExist):
            data['error'] = ["L'utente non ha effettuato il login."]
            return Response(data, status=status.HTTP_403_FORBIDDEN)
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
                data['password'] = 'Cambio password effettuato.'
                # get new token
                data['token'] = Token.objects.create(user=user_to_update).key
                return Response(data, status=status.HTTP_200_OK)
            else:
                data = {}
                data['error'] = ['Token di autorizzazione sbagliato.']
                return Response(data, status=status.HTTP_403_FORBIDDEN)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ActivateUserAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, id, token):
        try:
            user = User.objects.get(pk=id)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None:
            if not user.is_active:
                if account_activation_token.check_token(user, token):
                    user.is_active = True
                    user.save()
                else:
                    return Response({'error': ['Token di autorizzazione non valido.']},
                                    status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response({'error': ["L'utente ha già confermato l'email."]},
                                status=status.HTTP_204_NO_CONTENT)
            return Response({'activation': 'Indirizzo email confermato, account attivo.'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': ['Token di autorizzazione non valido.']}, status=status.HTTP_400_BAD_REQUEST)


class AskPasswordAPIView(APIView):

    def post(self, request):
        serializer = AskResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user = get_object_or_404(User, email=email)
            if user:
                reset_token = passwordreset_token.make_token(user)
                send_reset_email(user, reset_token)
                return Response(status.HTTP_200_OK)
            else:
                return Response(status.HTTP_404_NOT_FOUND)
        else:
            return Response(status.HTTP_400_BAD_REQUEST)


class ResetPasswordAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data, many=False)
        if serializer.is_valid():
            given_token = serializer.validated_data['token']
            password = serializer.validated_data['password']

            users = User.objects.all()
            for user in users:

                if passwordreset_token.check_token(user, given_token):
                    user.set_password(password)
                    user.save()
                    return Response(status=status.HTTP_200_OK)

            return Response({'error':  ['Token di autorizzazione non valido.']}, status.HTTP_404_NOT_FOUND)
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class UserProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        user = get_object_or_404(User, id=id)

        if user and not user.is_superuser:
            token = get_object_or_404(Token, user=user)
            if request.user.auth_token.key == token.key:
                # check if customer
                try:
                    customer = Customer.objects.all().get(user=user)
                    serializer = CustomerSerializer(customer, many=False)
                except Customer.DoesNotExist:
                    try:
                        business = Business.objects.all().get(user=user)
                        serializer = BusinessSerializer(business, many=False)
                    except Business.DoesNotExist:
                        return Response({'error':["Utente non trovato."]}, status.HTTP_404_NOT_FOUND)

                return Response(serializer.data, status.HTTP_200_OK)
            else:
                return Response({'error': ["Utente non autorizzato."]}, status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'error': ["Utente non trovato."]}, status.HTTP_404_NOT_FOUND)
