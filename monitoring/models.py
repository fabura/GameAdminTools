__author__ = 'bulat.fattahov'
from django.db import models

class AdenaLog(models.Model):
    date = models.DateTimeField(unique=True, auto_now_add=True, blank=True)
    server = models.IntegerField()
    value = models.BigIntegerField(max_length=15)




