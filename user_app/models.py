from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class Departments(models.Model):
    department = models.CharField(max_length=100)
    
    def __str__(self):
       return self.department

class Roles(models.Model):
    role = models.CharField(max_length=30)
    levels = models.IntegerField()

    def __str__(self):
       return self.role

class User(AbstractUser):
    email = models.EmailField(verbose_name='email address',max_length=255,unique=True,)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    department = models.ForeignKey(Departments, on_delete=models.CASCADE , null=True , default=None)
    role = models.ForeignKey(Roles, on_delete=models.CASCADE)
    rolename = models.CharField(max_length=30)
    
class LeftPanel(models.Model):
    component = models.CharField(max_length = 50)
    icon = models.CharField(max_length =50 , default = None)
    text = models.CharField(max_length =50)
    route = models.CharField(max_length = 50)
    allow = models.SmallIntegerField()# 0 = all , 1 = AO, 2 = Hod , 3 = Employee 
    props = models.JSONField(default = None)
