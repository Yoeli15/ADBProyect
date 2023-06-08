from rest_framework import serializers
from users.models import UserModel
from django.core.exceptions import ValidationError

class UserSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = '__all__'
        extra_kwargs = {
            'password':{'write_only': True},'attempt': {'required': False},
        }

    def validate(self, data):
        user = UserModel(**data)
        special_characters = "[~\!@#\$%\^&\*\(\)_\+{}\":;'\[\]]"
        
        # get the name from the data
        name = data.get('name')        
        
        # check for digit
        if any(char.isdigit() for char in name):
            raise ValidationError('El nombre del usuario no debe contener números.')
        # check for special character
        if any(char in special_characters for char in name):
            raise ValidationError('El nombre del usuario no debe contener caracteres especiales.')
        #check for length
        if len(name) < 5:
            raise ValidationError('El nombre del usuario debe contener al menos 5 caracteres.')

        # get the password from the data
        password = data.get('password')
        
        # check for digit
        if not any(char.isdigit() for char in password):
            raise ValidationError('La contraseña debe contener al menos 1 dígito.')

        # check for letter
        if not any(char.isalpha() for char in password):
            raise ValidationError('La contraseña debe contener al menos 1 letra.')

        # check for special character
        if not any(char in special_characters for char in password):
            raise ValidationError('La contraseña debe contener al menos 1 caracter especial.')
        
        #check for uppercase letter
        if not any(x.isupper() for x in password):
            raise ValidationError('La contraseña debe contener al menos 1 letra mayúscula.')
        
        #check for lowercase letter
        if not any(x.islower() for x in password):
            raise ValidationError('La contraseña debe contener al menos 1 letra minúscula.')
        #check for length
        if len(password) < 8 or len(password) > 12:
            raise ValidationError('La contraseña debe contener un mínimo de 8 caracteres y un máximo de 12 caracteres de longitud.')

        return super(UserSignupSerializer, self).validate(data)
    
    def create(self, validated_data):
        user = UserModel.objects.create_user(**validated_data)
        user.save()
        return user

class UserLoginSerializer(serializers.ModelSerializer):
    #Necesarios para el inicio de sesión
    email = serializers.EmailField(max_length=50)
    password = serializers.CharField(max_length=100)

    class  Meta:
        model = UserModel
        fields = [
            'email',
            'password',
        ]

#Para cuando se edita un usuario
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        exclude = ('email','password','attempt',)

    def validate(self, data):
        special_characters = "[~\!@#\$%\^&\*\(\)_\+{}\":;'\[\]]"
        
        # get the name from the data
        name = data.get('name')        
        
        # check for digit
        if any(char.isdigit() for char in name):
            raise ValidationError('El nombre del usuario no debe contener números.')
        # check for special character
        if any(char in special_characters for char in name):
            raise ValidationError('El nombre del usuario no debe contener caracteres especiales.')
        #check for length
        if len(name) < 5:
            raise ValidationError('El nombre del usuario debe contener al menos 5 caracteres.')

        return super(UserSerializer, self).validate(data)
    
#Para camvbiar contraseña
class ChangePasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ['password']
        extra_kwargs = {
            'password':{'write_only': True},
        }

    def validate(self, data):
        special_characters = "[~\!@#\$%\^&\*\(\)_\+{}\":;'\[\]]"
        
        # get the password from the data
        password = data.get('password')
        
        # check for digit
        if not any(char.isdigit() for char in password):
            raise ValidationError('La contraseña debe contener al menos 1 dígito.')

        # check for letter
        if not any(char.isalpha() for char in password):
            raise ValidationError('La contraseña debe contener al menos 1 letra.')

        # check for special character
        if not any(char in special_characters for char in password):
            raise ValidationError('La contraseña debe contener al menos 1 caracter especial.')
        
        #check for uppercase letter
        if not any(x.isupper() for x in password):
            raise ValidationError('La contraseña debe contener al menos 1 letra mayúscula.')
        
        #check for lowercase letter
        if not any(x.islower() for x in password):
            raise ValidationError('La contraseña debe contener al menos 1 letra minúscula.')
        #check for length
        if len(password) < 8 or len(password) > 12:
            raise ValidationError('La contraseña debe contener un mínimo de 8 caracteres y un máximo de 12 caracteres de longitud.')

        return super(ChangePasswordSerializer, self).validate(data)