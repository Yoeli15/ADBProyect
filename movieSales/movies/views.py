from rest_framework.views import APIView
from rest_framework import permissions, status
from users.models import UserModel
from rest_framework.exceptions import AuthenticationFailed
from movies.serializers import MovieRegisterSerializer
from rest_framework.response import Response
from movies.models import MovieModel
from django.shortcuts import get_object_or_404

# Create your views here.
class MovieView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        if UserModel.objects.filter(email = self.request.user, is_superuser = False, status_delete = False).exists():
            raise AuthenticationFailed('This user does not have permission to use this feature')
        else:
            serializer = MovieRegisterSerializer(data = request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request):
        if UserModel.objects.filter(email = self.request.user, is_superuser = False, status_delete = False).exists():
            raise AuthenticationFailed('This user does not have permission to use this feature')
        else:
            movies = MovieModel.objects.filter(status_delete = False).order_by("created_at")
            serializer = MovieRegisterSerializer(movies, many = True)
            return Response(serializer.data, status = status.HTTP_200_OK)

class ConfigureMovieView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def put(self, request):
        id = request.GET.get('id')#obtener el id de la película a modificar

        if UserModel.objects.filter(email = self.request.user, is_superuser = False, status_delete = False).exists():
            raise AuthenticationFailed('This user does not have permission to use this feature')
        else:
            movie_obj = get_object_or_404(MovieModel.objects.filter(status_delete = False), pk = id)
            serializer = MovieRegisterSerializer(instance=movie_obj, data=request.data, partial = True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request):
        id = request.GET.get('id')#obtener el id de la dirección a modificar

        if UserModel.objects.filter(email = self.request.user, is_superuser = False, status_delete = False).exists():
            raise AuthenticationFailed('This user does not have permission to use this feature')
        else:
            movie_obj = get_object_or_404(MovieModel.objects.filter(status_delete = False), pk = id)
            movie_obj.status_delete = True
            movie_obj.save()
            return Response({'message':'Película Eliminada.'}, status = status.HTTP_204_NO_CONTENT)