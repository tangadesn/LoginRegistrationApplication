from django.db import models
# Create your models here.


class Employee(models.Model):

    email_id = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    mobile_number = models.IntegerField(max_length=10)
    user_otp = models.IntegerField(max_length=10)