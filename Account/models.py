from django.db import models
from django.core.validators import validate_email
import uuid

# Create your models here.


class Users(models.Model):
    name = models.CharField(max_length=255,null=False)
    email = models.CharField(max_length=255,null=False,unique=True,validators=[validate_email])
    password = models.CharField(max_length=255,null=False)
    phone = models.CharField(max_length=255,null=False)
    push_notification_id = models.IntegerField(max_length=32,null=False,unique=True)
    device_id = models.IntegerField(max_length=32,null=False,unique=True)
    created_on = models.DateTimeField(auto_now_add=True)


class ApiToken(models.Model):
#TODO: one user should have only one api_token

    user = models.ForeignKey(Users,on_delete=models.CASCADE,unique=True)
    api_token = models.CharField(max_length=255)
    is_valid = models.BooleanField(default=False)

    def create_token(self):
        self.api_token = uuid.uuid4()

