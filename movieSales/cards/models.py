from django.db import models
from users.models import UserModel

# Create your models here.
class CardRegisterModel(models.Model):
    user_id = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    cvv = models.CharField(max_length = 3)
    cardHolderName = models.CharField(max_length = 15)
    fathersLastName = models.CharField(max_length=20)
    mothersLastName = models.CharField(max_length=20)
    account_number = models.CharField(max_length= 30, null=True)    
    email = models.EmailField(max_length=50, unique = True)
    status_delete = models.BooleanField(default=False)

    class Meta:
        db_table = 'cards'