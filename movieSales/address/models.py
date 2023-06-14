from django.db import models
from users.models import UserModel

# Create your models here.

class AddressModel(models.Model):
    user_id = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    street = models.CharField(max_length=20)
    number_ext = models.CharField(max_length=10)
    number_int = models.IntegerField()
    neighborhood = models.CharField(max_length=20)
    zip_code = models.IntegerField()
    city = models.CharField(max_length=20)
    state = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status_delete = models.BooleanField(default=False)

    class Meta:
        db_table = 'addresses'