from django.db import models

__author__ = 'bulat.fattahov'

class Settings(models.Model):
    name = models.CharField(max_length=20, unique=True)
    value = models.TextField()