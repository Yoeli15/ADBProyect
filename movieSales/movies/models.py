from django.db import models

# Create your models here.
class MovieModel(models.Model):
    name = models.CharField(max_length=30)
    genre = models.CharField(max_length=20)
    classification = models.CharField(max_length=2)
    release_year = models.IntegerField()
    movies_available = models.IntegerField()
    languages = models.CharField(max_length=15)
    duration = models.CharField(max_length=15)
    cinema_studio = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)#auto_now_add se genera cuando se invoca, auto_now cuando se crea
    updated_at = models.DateTimeField(auto_now=True)
    status_delete = models.BooleanField(default=False)

    def __str__(self):#cada vez que se invoque la película me muestre su nombre
        return self.name

    class Meta:
        db_table = 'movies'