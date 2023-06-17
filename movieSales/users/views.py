from rest_framework.views import APIView
from rest_framework import permissions, status
from users.serializers import (ClientSignupSerializer, EmployeeSignupSerializer,
                               UserLoginSerializer, ClientSerializer, EmployeeSerializer,
                               ChangePasswordSerializer)
from users.models import UserModel
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
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
class ClientSignupView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = ClientSignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class EmployeeSignupView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post (self, request):
        data = request.data
        if UserModel.objects.filter(email = self.request.user, is_superuser = False, status_delete = False).exists():
            raise AuthenticationFailed('This user does not have permission to use this feature')
        else:
            data['typeUser'] = 'EMPLEADO'
            usuario = UserModel.objects.filter(email = self.request.user)
            user = get_object_or_404(UserModel.objects.filter(email = self.request.user, status_delete = False))
            
            for b in usuario:
                nombre = b.name
                apellido =b.fathersLastName

            if user.is_staff == True:
                data['made_by'] = 'SUPERUSER'
                data['is_superuser'] = True
            else:
                data['made_by'] = nombre + " " + apellido
            
            serializer = EmployeeSignupSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class UserListView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self,request):#Listar
        if UserModel.objects.filter(email = self.request.user, is_superuser = False, status_delete = False).exists():
            raise AuthenticationFailed('This user does not have permission to use this feature')
        else:
            if UserModel.objects.filter(email = self.request.user, is_staff = True, status_delete = False).exists():
                users = UserModel.objects.filter(is_staff = False).order_by("branch")
            else:
                usuario = UserModel.objects.filter(email = self.request.user, status_delete = False)
                for b in usuario:
                    sucursal = b.branch
                
                users = UserModel.objects.filter(branch = sucursal, is_superuser = False, status_delete = False).order_by("branch")
        serializer = EmployeeSignupSerializer(users, many=True)
        return Response(serializer.data, status = status.HTTP_200_OK)

class UserLoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserLoginSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
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
                    except:
                        pass

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
    permission_classes = (permissions.IsAuthenticated,)

    def put(self, request):
        correo = request.GET.get('email')#obtener el email

        if UserModel.objects.filter(email = self.request.user, is_superuser = False, typeUser = 'CLIENTE', status_delete = False).exists():
            user_obj = get_object_or_404(UserModel.objects.filter(status_delete = False), email = self.request.user)
            serializer = ClientSerializer(instance=user_obj, data=request.data, partial = True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        else:
            if UserModel.objects.filter(email = self.request.user, is_staff = True, status_delete = False).exists():
                user_obj = get_object_or_404(UserModel.objects.filter(status_delete = False), email = correo)
                if user_obj.is_staff:
                    data = {'You can\'t update yourself here'}
                    return Response(data, status=status.HTTP_400_BAD_REQUEST)
            else:
                usuario = UserModel.objects.filter(email = self.request.user, status_delete = False)
                for b in usuario:
                    sucursal = b.branch
                user_obj = get_object_or_404(UserModel.objects.filter(branch = sucursal, status_delete = False), email = correo)

            serializer = EmployeeSerializer(instance=user_obj, data=request.data, partial = True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request):
        correo = request.GET.get('email')#obtener el email
        if UserModel.objects.filter(email = self.request.user, is_superuser = False, typeUser = 'CLIENTE', status_delete = False).exists():
            user_obj = get_object_or_404(UserModel.objects.filter(status_delete = False), email = self.request.user)
        else:
            if UserModel.objects.filter(email = self.request.user, is_staff = True, status_delete = False).exists():
                user_obj = get_object_or_404(UserModel.objects.filter(status_delete = False), email = correo)
                if user_obj.is_staff:
                    data = {'You can\'t erase yourself'}
                    return Response(data, status=status.HTTP_400_BAD_REQUEST)
            else:
                usuario = UserModel.objects.filter(email = self.request.user, status_delete = False)
                for b in usuario:
                    sucursal = b.branch
                user_obj = get_object_or_404(UserModel.objects.filter(branch = sucursal, status_delete = False), email = correo)

        user_obj.status_delete = True
        user_obj.save()

        return Response({'message':'Usuario Eliminado.'}, status = status.HTTP_204_NO_CONTENT)
    
class ChangePasswordView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

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