__author__ = 'bulat.fattahov'
from django.db import models

class Support(models.Model):
    name = models.CharField(max_length=20)


class Server(models.Model):
    name = models.CharField(max_length=20)
    id = models.IntegerField(primary_key=True)
    support = models.ForeignKey(to=Support)


class AdenaLog(models.Model):
    date = models.DateTimeField(auto_now_add=True, blank=True)
    server = models.ForeignKey(to=Server)
    value = models.BigIntegerField(max_length=15)

    class Meta:
        unique_together = ('server', 'date')


