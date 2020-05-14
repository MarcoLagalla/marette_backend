import json

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from django.db import transaction
from backend.account.permissions import IsBusiness
from rest_framework.authtoken.models import Token

from ..models.models import Restaurant, Picture
from ..models.menu import Menu
from ..models.components import MenuComponent, GalleriaComponent, EventiComponent, \
    VetrinaComponent, HomeComponent, ContattaciComponent

from .serializers import HomeSerializer, VetrinaSerializer, ContattaciSerializer, EventiSerializer, \
    MenuSerializer, GalleriaSerializer, PictureSerializer


class ActivateComponent(APIView):
    permission_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated, IsBusiness]

    @transaction.atomic()
    def post(self, request, id, type):
        # controllo se gli oggetti esistono
        try:
            restaurant = Restaurant.objects.get(id=id)
        except Restaurant.DoesNotExist:
            return Response({'error': 'Ristorante non trovato'}, status=status.HTTP_404_NOT_FOUND)

        try:
            token = Token.objects.all().get(user=restaurant.owner.user).key
        except Token.DoesNotExist:
            return Response({'error': 'Token non valido'}, status.HTTP_401_UNAUTHORIZED)

        if request.user.auth_token.key != token:
            return Response({'error': 'Token non valido'}, status.HTTP_401_UNAUTHORIZED)

        if request.user == restaurant.owner.user:
            # autorizzato
            panel = None
            type = type.lower()
            if type == 'home':
                try:
                    panel = HomeComponent.objects.all().get(restaurant=restaurant)
                except HomeComponent.DoesNotExist:
                    return Response(status=status.HTTP_404_NOT_FOUND)
            elif type == 'vetrina':
                try:
                    panel = VetrinaComponent.objects.all().get(restaurant=restaurant)
                except VetrinaComponent.DoesNotExist:
                    return Response(status=status.HTTP_404_NOT_FOUND)
            elif type == 'menu':
                try:
                    panel = MenuComponent.objects.all().get(restaurant=restaurant)
                except MenuComponent.DoesNotExist:
                    return Response(status=status.HTTP_404_NOT_FOUND)
            elif type == 'galleria':
                try:
                    panel = GalleriaComponent.objects.all().get(restaurant=restaurant)
                except GalleriaComponent.DoesNotExist:
                    return Response(status=status.HTTP_404_NOT_FOUND)
            elif type == 'eventi':
                try:
                    panel = EventiComponent.objects.all().get(restaurant=restaurant)
                except EventiComponent.DoesNotExist:
                    return Response(status=status.HTTP_404_NOT_FOUND)
            elif type == 'contattaci':
                try:
                    panel = ContattaciComponent.objects.all().get(restaurant=restaurant)
                except ContattaciComponent.DoesNotExist:
                    return Response(status=status.HTTP_404_NOT_FOUND)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)

            if panel:
                panel.show = True
                panel.save()
                return Response({type: 'attivato'}, status=status.HTTP_200_OK)

        return Response(status=status.HTTP_400_BAD_REQUEST)


class DeactivateComponent(APIView):
    permission_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated, IsBusiness]

    @transaction.atomic()
    def post(self, request, id, type):
        # controllo se gli oggetti esistono
        try:
            restaurant = Restaurant.objects.get(id=id)
        except Restaurant.DoesNotExist:
            return Response({'error': 'Ristorante non trovato'}, status=status.HTTP_404_NOT_FOUND)

        try:
            token = Token.objects.all().get(user=restaurant.owner.user).key
        except Token.DoesNotExist:
            return Response({'error': 'Token non valido'}, status.HTTP_401_UNAUTHORIZED)

        if request.user.auth_token.key != token:
            return Response({'error': 'Token non valido'}, status.HTTP_401_UNAUTHORIZED)

        if request.user == restaurant.owner.user:
            # autorizzato
            panel = None
            type = type.lower()
            if type == 'home':
                try:
                    panel = HomeComponent.objects.all().get(restaurant=restaurant)
                except HomeComponent.DoesNotExist:
                    return Response(status=status.HTTP_404_NOT_FOUND)
            elif type == 'vetrina':
                try:
                    panel = VetrinaComponent.objects.all().get(restaurant=restaurant)
                except VetrinaComponent.DoesNotExist:
                    return Response(status=status.HTTP_404_NOT_FOUND)
            elif type == 'menu':
                try:
                    panel = MenuComponent.objects.all().get(restaurant=restaurant)
                except MenuComponent.DoesNotExist:
                    return Response(status=status.HTTP_404_NOT_FOUND)
            elif type == 'galleria':
                try:
                    panel = GalleriaComponent.objects.all().get(restaurant=restaurant)
                except GalleriaComponent.DoesNotExist:
                    return Response(status=status.HTTP_404_NOT_FOUND)
            elif type == 'eventi':
                try:
                    panel = EventiComponent.objects.all().get(restaurant=restaurant)
                except EventiComponent.DoesNotExist:
                    return Response(status=status.HTTP_404_NOT_FOUND)
            elif type == 'contattaci':
                try:
                    panel = ContattaciComponent.objects.all().get(restaurant=restaurant)
                except ContattaciComponent.DoesNotExist:
                    return Response(status=status.HTTP_404_NOT_FOUND)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)

            if panel:
                panel.show = False
                panel.save()
                return Response({type: 'disattivato'}, status=status.HTTP_200_OK)

        return Response(status=status.HTTP_400_BAD_REQUEST)


class UpdateHomeComponent(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsBusiness, IsAuthenticated]

    @transaction.atomic()
    def post(self, request, id):
        restaurant = action_authorized(request, id)
        if restaurant:
            try:
                home = HomeComponent.objects.all().get(restaurant=restaurant)
            except HomeComponent.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)

            try:
                data = json.loads(request.data['data'])
            except KeyError:
                return Response(status=status.HTTP_400_BAD_REQUEST)

            try:
                image = request.data['image']
            except KeyError:
                image = None

            try:
                del data['name']
            except KeyError:
                pass

            for key in data:
                setattr(home, key, data[key])

            if image == '':
                home.image = None
            elif image:
                home.image = image
                
            home.save()

            serializer = HomeSerializer(home)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class UpdateGalleriaComponent(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsBusiness, IsAuthenticated]

    @transaction.atomic()
    def post(self, request, id):
        restaurant = action_authorized(request, id)
        if restaurant:
            try:
                galleria = GalleriaComponent.objects.all().get(restaurant=restaurant)
            except GalleriaComponent.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)

            serializer = GalleriaSerializer(data=request.data)
            if serializer.is_valid():
                data = request.data
                try:
                    images = data.pop('immagini', None)
                except KeyError:
                    pass

                if images:

                    galleria.immagini.clear()
                    for i in images:
                        try:
                            img = Picture.objects.all().filter(restaurant=restaurant).get(id=i)
                            galleria.immagini.add(img)
                        except Picture.DoesNotExist:
                            pass

                try:
                    del data['name']
                except KeyError:
                    pass

                for key in data:
                    setattr(galleria, key, data[key])

                galleria.save()
                return Response(status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class UpdateVetrinaComponent(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsBusiness, IsAuthenticated]

    @transaction.atomic()
    def post(self, request, id):
        restaurant = action_authorized(request, id)
        if restaurant:
            try:
                vetrina = VetrinaComponent.objects.all().get(restaurant=restaurant)
            except VetrinaComponent.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)

            serializer = VetrinaSerializer(data=request.data)
            if serializer.is_valid():
                data = request.data
                try:
                    menu_id = data.pop('menu_giorno', None)
                except KeyError:
                    return Response(status=status.HTTP_400_BAD_REQUEST)

                if menu_id == "":
                    # remove menu
                    vetrina.menu_giorno = None
                elif menu_id:
                    try:
                        menu = Menu.objects.all().filter(restaurant=restaurant).get(id=menu_id)
                        vetrina.menu_giorno = menu
                    except Menu.DoesNotExist:
                        return Response(status=status.HTTP_404_NOT_FOUND)
                try:
                    del data['name']
                except KeyError:
                    pass

                for key in data:
                    setattr(vetrina, key, data[key])

                vetrina.save()
                model_data = VetrinaSerializer(vetrina)
                return Response(model_data.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class UpdateEventiComponent(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsBusiness, IsAuthenticated]

    @transaction.atomic()
    def post(self, request, id):
        pass


class UpdateContattaciComponent(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsBusiness, IsAuthenticated]

    @transaction.atomic()
    def post(self, request, id):
        pass


class UpdateMenuComponent(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsBusiness, IsAuthenticated]

    @transaction.atomic()
    def post(self, request, id):
        pass


class GalleryAddImage(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsBusiness, IsAuthenticated]

    @transaction.atomic()
    def post(self, request, id):

        restaurant = action_authorized(request, id)
        if restaurant:

            try:
                data = json.loads(request.data['data'])
            except KeyError:
                return Response(status=status.HTTP_400_BAD_REQUEST)

            try:
                image = request.data['image']
                data.update({'image': image})
            except KeyError:
                return Response(status=status.HTTP_400_BAD_REQUEST)

            serializer = PictureSerializer(data=data)
            if serializer.is_valid():
                img = serializer.save(restaurant)
                data = serializer.validated_data
                data.update({'id': img.id})
                data.update({'restaurant': img.restaurant.id})
                data.update({'image': img.get_image()})
                return Response(serializer.validated_data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


class GalleryEditImage(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsBusiness, IsAuthenticated]

    @transaction.atomic()
    def post(self, request, id, i_id):

        try:
            picture = Picture.objects.all().get(id=i_id)
        except Picture.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        restaurant = action_authorized(request, id)

        if restaurant:

            try:
                data = json.loads(request.data['data'])
            except KeyError:
                return Response(status=status.HTTP_400_BAD_REQUEST)

            try:
                image = request.data['image']
                data.update({'image': image})
            except KeyError:
                return Response(status=status.HTTP_400_BAD_REQUEST)

            serializer = PictureSerializer(data=data)
            if serializer.is_valid():

                for key in data:
                    setattr(picture, key, data[key])

                picture.save()

                data = serializer.validated_data
                data.update({'id': picture.id})
                data.update({'restaurant': picture.restaurant.id})
                data.update({'image': picture.get_image()})
                return Response(serializer.validated_data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


class GalleryDeleteImage(APIView):

    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsBusiness, IsAuthenticated]

    @transaction.atomic()
    def post(self, request, id, i_id):

        try:
            picture = Picture.objects.all().get(id=i_id)
        except Picture.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        restaurant = action_authorized(request, id)

        if restaurant:
            picture.delete()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


def action_authorized(request, id):
    # controllo se gli oggetti esistono
    try:
        restaurant = Restaurant.objects.get(id=id)
    except Restaurant.DoesNotExist:
        return Response({'error': 'Ristorante non trovato'}, status=status.HTTP_404_NOT_FOUND)

    try:
        token = Token.objects.all().get(user=restaurant.owner.user).key
    except Token.DoesNotExist:
        return Response({'error': 'Token non valido'}, status.HTTP_401_UNAUTHORIZED)

    if request.user.auth_token.key != token:
        return Response({'error': 'Token non valido'}, status.HTTP_401_UNAUTHORIZED)

    if request.user == restaurant.owner.user:
        return restaurant

    return False