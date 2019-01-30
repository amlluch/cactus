from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.reverse import reverse_lazy
from oauth2_provider.models import  Application

import requests
import os

from .serializers import CreateUserSerializer, CheckUserSerializer

CLIENT_ID = os.environ.get('CLIENT_ID', '')
CLIENT_SECRET = os.environ.get('CLIENT_SECRET', '')

@authentication_classes(( SessionAuthentication, BasicAuthentication, TokenAuthentication))
@permission_classes((IsAdminUser,))
class Register(APIView):
    serializer_class = CreateUserSerializer
    def post(self, request):
        '''
        Registra usuario en el servidor. El formato es el siguiente:
        {"username": "username", "email":"email", "password": "1234abcd"}
        '''
 
        serializer = CreateUserSerializer(data=request.data) 
        if serializer.is_valid():

            serializer.save() 
            # Obtenemos el token para crear usuario
            r = requests.post(reverse_lazy('oauth2_provider:token', request=request), 
                data={
                    'grant_type': 'password',
                    'username': request.data['email'], # El username en realidad es el email en nuestro usermodel
                    'password': request.data['password'],
                    'client_id': CLIENT_ID,
                    'client_secret': CLIENT_SECRET,
                }
            )
            return Response(r.json())
        return Response(serializer.errors)


@permission_classes([AllowAny])
class Token(APIView):
    serializer_class =  CheckUserSerializer
    
    def post(self, request):
        """
        Obtiene el Token. El formato es el siguiente:
        {"username": "username", "password": "1234abcd"}
        """     

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            r = requests.post(
            reverse_lazy('oauth2_provider:token', request=request), 
                data={
                    'grant_type': 'password',
                    'username': request.data['email'], # En realidad es el email. Visto en serializers
                    'password': request.data['password'],
                    'client_id': CLIENT_ID,
                    'client_secret': CLIENT_SECRET,
                },
            )
            return Response(r.json())
        return Response(serializer.errors)


@permission_classes([AllowAny])
class RefreshToken(APIView):
    def post(self, request):
        '''
        Registra usuario en el servidor. El formato debe ser:
        {"refresh_token": "<token>"}
        '''
        r = requests.post(
        str(reverse_lazy('oauth2_provider:token', request=request)), 
            data={
                'grant_type': 'refresh_token',
                'refresh_token': request.data['refresh_token'],
                'client_id': CLIENT_ID,
                'client_secret': CLIENT_SECRET,
            },
        )
        return Response(r.json())


@permission_classes([AllowAny])
class RevokeToken(APIView):
    def post(self, request):
        '''
        Metodo para revocar tokens.
        {"token": "<token>"}
        '''
        r = requests.post(
            str(reverse_lazy('oauth2_provider:revoke-token', request=request)), 
            data={
                'token': request.data['token'],
                'client_id': CLIENT_ID,
                'client_secret': CLIENT_SECRET,
            },
        )
        # Si va bien, mensaje de exito 
        if r.status_code == requests.codes.ok:
            return Response({'message': 'token revoked'}, r.status_code)
        # Devuelve error si la cosa va mal
        return Response(r.json(), r.status_code)
