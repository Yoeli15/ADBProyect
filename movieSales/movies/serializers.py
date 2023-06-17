from rest_framework import serializers
from movies.models import MovieModel
from django.core.exceptions import ValidationError

class MovieRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieModel
        fields = "__all__"
    
    def validate(self, attrs):
        # get the name from the data
        name = attrs.get('name')

        if len(name) <= 1:
            ValidationError("El nombre de la película debe contener más de 1 caracter.")
        
        # get the genre from the data
        genre = attrs.get("genre")

        if len(genre) < 5:
            ValidationError("El género debe contener al menos 5 caracteres.")

        # get the release_year from the data
        release_year = attrs.get("release_year")

        if release_year < 1890:
            ValidationError("No puedes colocar años menores a 1890.")

        # get the languages from the data
        languages = attrs.get("languages")

        if len(languages) < 5:
            ValidationError("El idioma debe contener al menos 5 caracteres.")
        
        # get the cinema_studio from the data
        cinema_studio = attrs.get("cinema_studio")

        if len(cinema_studio) < 5:
            ValidationError("El nombre del estudio de cine debe contener al menos 5 caracteres.")

        return super(MovieRegisterSerializer, self).validate(attrs)