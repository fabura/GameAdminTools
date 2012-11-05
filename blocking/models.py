__author__ = 'bulat.fattahov'
from django.db import models

class BlockingLog(models.Model):
    ticket_id = models.IntegerField()
    email = models.EmailField()
    deskpro_account_created = models.BooleanField()
    message = models.ForeignKey(to=BlockingMessage)
    account_name = models.CharField(max_length=20)
    char_name = models.CharField(max_length=20)
    server = models.IntegerField()
    duration = models.IntegerField()
    date = models.DateTimeField(unique=True, auto_now_add=True, blank=True)


class BlockingMessage(models.Model):
    title = models.CharField()
    modified = models.BooleanField()
    text = models.TextField()

