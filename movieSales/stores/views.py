from rest_framework.views import APIView
from rest_framework import permissions, status
from users.models import UserModel
from rest_framework.exceptions import AuthenticationFailed
from stores.serializers import StoreRegisterSerializer, StoreSerializer
from rest_framework.response import Response
from stores.models import StoreModel
from django.shortcuts import get_object_or_404

# Create your views here.
class StoreView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        if UserModel.objects.filter(email = self.request.user, is_superuser = False, status_delete = False).exists():
            raise AuthenticationFailed('This user does not have permission to use this feature')
        else:
            data = request.data
            sucursal = data['name']
            ids = []

            if UserModel.objects.filter(email = self.request.user, is_staff = True, status_delete = False).exists():
                employee = UserModel.objects.filter(typeUser = 'EMPLEADO', status_delete = False)
                for b in employee:
                    if b.branch == sucursal:
                        ids.append(b.pk)

                data['user_id'] = ids

            else:
                usuario = UserModel.objects.filter(email = self.request.user)
                for b in usuario:
                    branch = b.branch

                employee = UserModel.objects.filter(typeUser = 'EMPLEADO', branch = branch, status_delete = False)
                for b in employee:
                    if b.branch == sucursal:
                        ids.append(b.pk)

                data['user_id'] = ids

            serializer = StoreRegisterSerializer(data = request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request):
        if UserModel.objects.filter(email = self.request.user, is_superuser = False, status_delete = False).exists():
            raise AuthenticationFailed('This user does not have permission to use this feature')
        else:
            if UserModel.objects.filter(email = self.request.user, is_staff = True, status_delete = False).exists():
                stores = StoreModel.objects.filter(user_id__status_delete = False, movies_id__status_delete = False, status_delete = False).order_by("created_at")
            else:
                users = UserModel.objects.filter(email = self.request.user)

                for b in users:
                    sucursal = b.branch

                stores = StoreModel.objects.filter(user_id__branch = sucursal, user_id__status_delete = False, movies_id__status_delete = False, status_delete = False).order_by("created_at")

            serializer = StoreRegisterSerializer(stores, many = True)
            return Response(serializer.data, status = status.HTTP_200_OK)

class ConfigureStoreView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def put(self, request):
        id = request.GET.get('id')#obtener el id de la sucursal a modificar

        if UserModel.objects.filter(email = self.request.user, is_superuser = False, status_delete = False).exists():
            raise AuthenticationFailed('This user does not have permission to use this feature')
        else:
            if UserModel.objects.filter(email = self.request.user, is_staff = True, status_delete = False).exists():
                store_obj = get_object_or_404(StoreModel.objects.filter(status_delete = False), pk = id)
            else:
                usuario = UserModel.objects.filter(email = self.request.user, status_delete = False)
                for b in usuario:
                    sucursal = b.branch
                store_obj = get_object_or_404(StoreModel.objects.filter(user_id__branch = sucursal, status_delete = False), pk = id)

            serializer = StoreRegisterSerializer(instance=store_obj, data=request.data, partial = True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request):
        id = request.GET.get('id')#obtener el id de la sucursal a modificar

        if UserModel.objects.filter(email = self.request.user, is_staff = False, status_delete = False).exists():
            raise AuthenticationFailed('This user does not have permission to use this feature')
        else:
            store_obj = get_object_or_404(StoreModel.objects.filter(status_delete = False), pk = id)
            store_obj.status_delete = True
            store_obj.save()
            return Response({'message':'Sucursal Eliminada.'}, status = status.HTTP_204_NO_CONTENT)

class ListStoresView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        store = request.GET.get('store')#obtener el id de la sucursal a modificar
        stores = StoreModel.objects.filter(movies_id__status_delete = False, store = store, status_delete = False).order_by("created_at")
        serializer = StoreSerializer(stores, many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)