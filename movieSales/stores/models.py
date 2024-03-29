from django.db import models
from users.models import UserModel
from movies.models import MovieModel

# Create your models here.
class StoreModel(models.Model):
    SUCURSALES =[
        ('INSURGENTES', 'insurgentes'),
        ('CUATRO CAMINOS', 'cuatro caminos'),
        ('LOMAS ESTRELLA', 'lomas estrella'),
        ('SANTA FE', 'santa fe'),
        ('UNIVERSIDAD', 'universidad')
    ]

    user_id = models.ManyToManyField(UserModel)
    movies_id = models.ManyToManyField(MovieModel)
    name = models.CharField(choices=SUCURSALES, unique=True)
    location = models.CharField(max_length=100, unique=True)
    store_hours = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)#auto_now_add se genera cuando se invoca, auto_now cuando se crea
    updated_at = models.DateTimeField(auto_now=True)
    status_delete = models.BooleanField(default=False)

    def __str__(self):#cada vez que se invoque la película me muestre su nombre
        return self.name

    class Meta:
        db_table = 'stores'