from django.db import models


# user model

class User(models.Model):  
    email=models.EmailField(max_length=200)
    name = models.CharField(max_length=200)
    stack = models.CharField(max_length=200)
    
    