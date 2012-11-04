__author__ = 'bulat.fattahov'
from django.db import models

class UserProfile(models.Model):
    date = models.DateTimeField(unique=true, auto_now=true)
    value = models.IntegerField(max_length=15)




