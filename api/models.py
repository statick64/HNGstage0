from django.db import models

# Create your models here.

class User(models.Model):
    email=models.EmailField(max_length=200)
    name = models.CharField(max_length=200)
    stack = models.CharField(max_length=200)
    
    