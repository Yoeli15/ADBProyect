import jwt
from rest_framework.views import APIView
from rest_framework import permissions, status
from users.serializers import (UserSignupSerializer, UserLoginSerializer, 
                               UserSerializer, ChangePasswordSerializer)
from users.models import UserModel
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from users.utils import Util
from rest_framework.response import Response
from django.conf import settings
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import make_password

# Generates tokens manually.
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'access': str(refresh.access_token),
    }

# Create your views here.
class UserSignupView(APIView):
    permission_classes = (permissions.AllowAny,)
    def post(self, request):#Registrar
        data = request.data
        usuario = UserModel.objects.filter(email = self.request.user)

        serializer = UserSignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class UserListView(APIView):
    permission_classes = (permissions.IsAdminUser,)

    def get(self,request):#Listar
        users = UserModel.objects.filter(is_staff = False).order_by("created_at")
        serializer = UserSignupSerializer(users, many=True)
        return Response(serializer.data)

class UserLoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserLoginSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)#Método de validación
        email = serializer.data["email"]
        password = serializer.data["password"]
        
        # Authentication method. If user exists, returns an user instance.
        user = authenticate(username=email, password=password)
  
        if not user:
            try:
                account = UserModel.objects.filter(email = email, status_delete = False).exists()
            except:
                raise AuthenticationFailed('Credenciales inválidas, intenta otra vez')

            if account:
                account = UserModel.objects.filter(email = email, status_delete = False)
                for i in range(0,3):
                    try:
                        intento = account.get(attempt = i)
                        #print(intento)
                    except:
                        pass
                #print(account)
                if intento.attempt == 2:
                    intento.is_active = False
                    intento.save()
                    raise AuthenticationFailed('Cuenta deshabilitada, contacta al administrador')
                else:
                    intento.attempt = intento.attempt+1
                    #print(intento.attempt)
                intento.save()

            raise AuthenticationFailed('Credenciales inválidas, intenta otra vez')
        if not user.is_active:    
            raise AuthenticationFailed('Cuenta deshabilitada, contacta al administrador')
        if user.status_delete:
            raise AuthenticationFailed('Credenciales inválidas, intenta otra vez')

        if user is not None:        
            tokens = get_tokens_for_user(user)
            usuario = UserModel.objects.filter(email = email)
            user_obj = get_object_or_404(UserModel.objects.filter(email = email, status_delete = False))
            #reiniciar intentos
            user_obj.attempt = 0
            user_obj.save()
            
            data = {
                'msg':'Successfully logged in.',
                'tokens':tokens,
            }

        return Response(data, status=status.HTTP_200_OK)

class ConfigureUserView(APIView):
    permission_classes = (permissions.IsAuthenticate,)

    def put(self, request):
        correo = request.GET.get('email')#obtener el email
        user_obj = get_object_or_404(UserModel.objects.filter(status_delete = False, is_verified = True), email = correo)
        if user_obj.is_staff:
            data = {'You can\'t update yourself'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = UserSerializer(instance=user_obj, data=request.data, partial = True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request):
        correo = request.GET.get('email')#obtener el email
        user_obj = get_object_or_404(UserModel.objects.filter(status_delete = False), email = correo)
        if user_obj.is_staff:
            data = {'You can\'t erase yourself'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        else:
            user_obj.status_delete = True
            user_obj.save()
        return Response({'message':'Usuario Eliminado.'}, status = status.HTTP_204_NO_CONTENT)
    
class ChangePasswordView(APIView):
    permission_classes = (permissions.IsAuthenticate,)

    def put(self, request):
        correo = request.GET.get('email')#obtener el email
        data = request.data
        new_password = data["password"]
        try:
            user = UserModel.objects.get(email = correo)#obtener el email
        except:
            data = {'Este correo electrónico no está registrado.'}
            return Response(data, status=status.HTTP_404_NOT_FOUND)

        if user.is_staff:
            data = {'No puedes cambiar tu contraseña aquí.'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        elif user.status_delete:
            data = {'Este correo electrónico está deshabilitado.'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = ChangePasswordSerializer(instance = user, data=request.data, partial = True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            user.password = make_password(new_password)
            user.save()
            if not user.is_active:
                user.is_active = True
                user.attempt = 0
                user.save()
            return Response({'message':'Cambio de contraseña con éxito.'}, status = status.HTTP_200_OK)