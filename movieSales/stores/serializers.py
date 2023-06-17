from rest_framework import serializers
from stores.models import StoreModel
from django.core.exceptions import ValidationError
from users.serializers import EmployeeSerializer
from movies.serializers import MovieRegisterSerializer

class StoreRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreModel
        fields = "__all__"
    
    def validate(self, attrs):
        # get the name from the data
        name = attrs.get('name')

        if len(name) < 5:
            ValidationError("El nombre de la sucursal debe contener al menos 5 caracteres.")
        
        # get the location from the data
        location = attrs.get("location")

        if len(location) < 15:
            ValidationError("La ubicación debe contener al menos 15 caracteres.")

        # get the store_hours from the data
        store_hours = attrs.get("store_hours")

        if len(store_hours) < 20:
            ValidationError("El horario de tienda debe contener al menos 20 caracteres.")

        return super(StoreRegisterSerializer, self).validate(attrs)
    
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['user_id'] = EmployeeSerializer(instance.user_id).data
        response['movies_id'] = MovieRegisterSerializer(instance.movies_id).data
        return response

class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreModel
        exclude = ('user_id')
    
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['movies_id'] = MovieRegisterSerializer(instance.movies_id).data
        return response