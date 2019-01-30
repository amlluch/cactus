from rest_framework.permissions import BasePermission
from usermodel.models import User
from rest_framework import status

class IsGet(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        return False
    
class IsPost(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST':
            return True
        return False
    
class IsPut(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'PUT':
            return True
        return False
      
class IsDelete(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'DELETE':
            return True
        return False

class ResponseException(Exception):
    def __init__(self, mensaje, status):
        self.mensaje = mensaje
        self.status = status

class Permiso():
    def __init__(self, request, usr):
        self.request = request
        self.usr = usr
           
    def get_usuario(self):
        current_user = self.request.user
        usr = self.usr
        if usr:     # El admin puede acceder a cualquier usuario
            if usr!=current_user.username and not current_user.is_superuser:
                # Si no es administrador solo puede acceder a su propio perfil
                raise ResponseException('No autorizado', status.HTTP_401_UNAUTHORIZED)

            try:
                usuario = User.objects.get(username = usr)
                return usuario
            except User.DoesNotExist:
                raise ResponseException('Usuario inexistente', status.HTTP_404_NOT_FOUND)

        else:
            return current_user