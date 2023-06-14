from rest_framework import serializers
from .models import AddressModel
from django.core.exceptions import ValidationError

class AddressRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddressModel
        fields = "__all__"
    
    def validate(self, attrs):
        # get the street from the data
        calle = attrs.get('street')

        if len(calle) < 5:
            ValidationError("El nombre de la calle debe contener al menos 5 caracteres.")
        
        # get the neighborhood from the data
        colonia = attrs.get("neighborhood")

        if len(colonia) < 5:
            ValidationError("El nombre de la colonia debe contener al menos 5 caracteres.")

        # get the city from the data
        del_mun = attrs.get("city")

        if len(del_mun) < 5:
            ValidationError("El nombre de la delegación o municipio debe contener al menos 5 caracteres.")

        # get the state from the data
        estado = attrs.get("state")

        if len(estado) < 5:
            ValidationError("El nombre del estado debe contener al menos 5 caracteres.")

        return super(AddressRegisterSerializer, self).validate(attrs)