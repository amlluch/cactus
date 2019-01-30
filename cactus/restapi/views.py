from rest_framework.views import APIView
from .serializers import UserSerializer, ModifySerializer
from rest_framework.response import Response
from rest_framework import status
from rest_condition import ConditionalPermission, C, And, Or, Not
from .permissions import IsGet, IsPost, IsPut, IsDelete, Permiso, ResponseException
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.decorators import permission_classes, authentication_classes
from usermodel.models import User
import json

# Para desloguearse correctamente, el orden de las clases importa
@authentication_classes(( SessionAuthentication, BasicAuthentication, TokenAuthentication))
class UserRest(APIView):
    # Se pueden asignar permisos simplemente con el decorator pero con rest_condition hay mas claridad
    permission_classes = [Or(And(IsGet, IsAuthenticated),   #Any authenticated user
                             And(IsPut, IsAuthenticated),   #Any authenticated user
                             And(IsDelete, IsAuthenticated))]  
    # En realidad esto es necesario solo para la web de rest_framework 
    serializer_class = ModifySerializer

    def get(self, request, usr=None, format=None):  # Puede enviar el username en la peticion

        """
        Datos del usuario. Accede bien sin proporcionar usuario o con username para admins
        """

        rest_user = Permiso(request, usr)
        try:
            usuario = rest_user.get_usuario()
        except ResponseException as err:
            return Response(err.mensaje, status=err.status)

        serializer = UserSerializer(usuario, data=request.data)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response('Usuario no encontrado', status = status.HTTP_404_NOT_FOUND)

    def delete(self, request, usr=None, format=None):
        """
        Cualquier usuario se puede borrar a si mismo o el admin a cualquier usuario.
        """

        rest_user = Permiso(request, usr)
        try:
            usuario = rest_user.get_usuario()
        except ResponseException as err:
            return Response(err.mensaje, status=err.status)

        User.objects.filter(email = usuario.email).delete()
        return Response('Usuario borrado', status=status.HTTP_200_OK)

    def put(self, request, usr=None, format=None):
        """
        El admin puede modificar cualquier usuario. Un usuario solo se puede
        modificar a si mismo
        """

        rest_user = Permiso(request, usr)
        try:
            usuario = rest_user.get_usuario()
        except ResponseException as err:
            return Response(err.mensaje, status=err.status)

        context = {'request':request}
        serializer = self.serializer_class(usuario, data=request.data, context=context)
        if serializer.is_valid():
            dato = serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@authentication_classes(( SessionAuthentication, BasicAuthentication, TokenAuthentication))
@permission_classes((IsAdminUser,))
class NewUser(APIView):

# Se crea nuevo usuario asi: http://url/restapi/user/<nombre_usuario_nuevo>/new

    serializer_class = ModifySerializer
    # Este get no es necesario pero para la web queda mas claro para el usuario.
    def get(self, request, usr=None, format=None):

        try:
            usuario = User.objects.get(username=usr)
            return Response('Usuario ya existente, no puede crearlo', status=status.HTTP_400_BAD_REQUEST )
        except User.DoesNotExist:
            return Response('Creando nuevo usuario: ' + usr)

    def post(self, request, usr=None, format=None):

        try:
            usuario = User.objects.get(username=usr)
            return Response('Usuario ya existente, no puede crearlo', status=status.HTTP_400_BAD_REQUEST )
        except User.DoesNotExist:
            pass
        context = {"user":usr, 'request':request}
        serializer = self.serializer_class(data=request.data, context = context)
        if serializer.is_valid():
            dato = serializer.save()
            return Response (serializer.data, status=status.HTTP_200_OK)
        else:
            return Response (serializer.errors, status=status.HTTP_400_BAD_REQUEST)
