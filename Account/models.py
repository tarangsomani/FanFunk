from django.db import models
from django.core.validators import validate_email
import uuid

# Create your models here.


class Users(models.Model):

    name = models.CharField(max_length=255,null=False)
    email = models.CharField(max_length=255,null=False,unique=True,validators=[validate_email])
    password = models.CharField(max_length=255,null=False)
    phone = models.CharField(max_length=255,null=False)
    created_on = models.DateTimeField(auto_now_add=True)


class ApiToken(models.Model):

    user = models.ForeignKey(Users,on_delete=models.CASCADE,unique=True)
    api_token = models.CharField(max_length=255)
    is_valid = models.BooleanField(default=False)

    def create_token(self):
        self.api_token = uuid.uuid4()


class UserDevice(models.Model):

    user = models.ForeignKey(Users,on_delete=models.CASCADE,related_name='device_user')
    device_id = models.CharField(max_length=32,unique=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)


class PushNotification(models.Model):

    user = models.ForeignKey(Users,on_delete=models.CASCADE,related_name='notification')
    push_notification_id = models.CharField(max_length=32,unique=True)
    push_notification_token = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def create_notification_token(self):
        self.push_notification_token = uuid.uuid4()