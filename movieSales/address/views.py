from rest_framework.views import APIView
from rest_framework import permissions, status
from address.serializers import AddressRegisterSerializer
from rest_framework.response import Response
from users.models import UserModel
from address.models import AddressModel
from django.shortcuts import get_object_or_404

# Create your views here.
class AddressView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        if AddressModel.objects.filter(user_id = self.request.user, status_delete = False).exists():
            data = {'Sólo se permite añadir una dirección de domicilio por usuario'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = AddressRegisterSerializer(data = request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(user_id = self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def get(self, request):
        if UserModel.objects.filter(email = self.request.user, is_superuser = False, status_delete = False).exists():
            address = AddressModel.objects.filter(user_id = self.request.user)
        else:
            if UserModel.objects.filter(email = self.request.user, is_staff = True, status_delete = False).exists():
                address = AddressModel.objects.filter(status_delete = False).order_by("user_id")
            else:
                usuario = UserModel.objects.filter(email = self.request.user, status_delete = False)
                for b in usuario:
                    sucursal = b.branch
                
                address = AddressModel.objects.filter(user_id__branch = sucursal, status_delete = False).order_by("user_id")

        serializer = AddressRegisterSerializer(address, many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)

class ConfigureAddressView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def put(self, request):
        id = request.GET.get('id')#obtener el id de la dirección a modificar

        if UserModel.objects.filter(email = self.request.user, is_superuser = False, typeUser = 'CLIENTE', status_delete = False).exists():
            address_obj = get_object_or_404(AddressModel.objects.filter(status_delete = False), pk = id)
        else:
            if UserModel.objects.filter(email = self.request.user, is_staff = True, status_delete = False).exists():
                address_obj = get_object_or_404(AddressModel.objects.filter(status_delete = False), pk = id)
            else:
                usuario = UserModel.objects.filter(email = self.request.user, status_delete = False)
                for b in usuario:
                    sucursal = b.branch

                address_obj = get_object_or_404(AddressModel.objects.filter(user_id__branch = sucursal, status_delete = False), pk = id)

        serializer = AddressRegisterSerializer(instance=address_obj, data=request.data, partial = True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request):
        id = request.GET.get('id')#obtener el id de la dirección a modificar

        if UserModel.objects.filter(email = self.request.user, is_superuser = False, typeUser = 'CLIENTE', status_delete = False).exists():
            address_obj = get_object_or_404(AddressModel.objects.filter(status_delete = False), pk = id)
        else:
            if UserModel.objects.filter(email = self.request.user, is_staff = True, status_delete = False).exists():
                address_obj = get_object_or_404(AddressModel.objects.filter(status_delete = False), pk = id)
            else:
                usuario = UserModel.objects.filter(email = self.request.user, status_delete = False)
                for b in usuario:
                    sucursal = b.branch
                address_obj = get_object_or_404(AddressModel.objects.filter(user_id__branch = sucursal, status_delete = False), pk = id)

        address_obj.status_delete = True
        address_obj.save()

        return Response({'message':'Dirección Eliminada.'}, status = status.HTTP_204_NO_CONTENT)