from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin#mezcla de permisos

# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, name, email, password = None, **kwargs):
        if not name:
            raise TypeError("Users should have a name.")
        if not email:
            raise TypeError("Users should have a email.")
        if not password:
            raise TypeError("Password should not be none.")
        
        user = self.model(name = name, email=self.normalize_email(email),**kwargs)
        user.set_password(password)
        
        user.save()
        return user
    
    def create_superuser(self, email, password=None, **kwargs):
        if not email:
            raise TypeError("Users should have a email.")
        if not password:
            raise TypeError("Password should not be none.")

        user = self.model(email=self.normalize_email(email), **kwargs)
        user.is_active = True
        user.is_superuser=True
        user.is_staff = True
        user.email = email
        user.set_password(password)
        user.save()
        return user

class UserModel(AbstractBaseUser, PermissionsMixin):

    HORARIO =[
        ('MATUTINO', 'matutino'),
        ('VESPERTINO', 'vespertino')
    ]

    SUCURSALES =[
        ('INSURGENTES', 'insurgentes'),
        ('CUATRO CAMINOS', 'cuatro caminos'),
        ('LOMAS ESTRELLA', 'lomas estrella'),
        ('SANTA FE', 'santa fe'),
        ('UNIVERSIDAD', 'universidad')
    ]

    email = models.EmailField(max_length=50, unique = True)
    password = models.CharField(max_length=255)
    rfc = models.CharField(max_length=13, unique=True, blank=True, null=True)
    name = models.CharField(max_length=20)
    fathersLastName = models.CharField(max_length=20)
    mothersLastName = models.CharField(max_length=20)
    age = models.IntegerField(default=18)
    schedule = models.CharField(choices=HORARIO, blank=True, null=True)
    typeUser = models.CharField(max_length=10, default='CLIENTE')
    branch = models.CharField(choices=SUCURSALES, blank=True, null=True)
    attempt = models.IntegerField(default=0)
    made_by = models.CharField(max_length=20, blank=True, null=True)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)#auto_now_add se genera cuando se invoca, auto_now cuando se crea
    updated_at = models.DateTimeField(auto_now=True)
    status_delete = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    
    def __str__(self):#cada vez que se invoque el usuario me muestre su email
        return self.email

    class Meta:
        db_table = 'users'