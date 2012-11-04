from django.forms import ModelForm
from django import forms

__author__ = 'Bulat'
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    l2admin_login = models.CharField(max_length=20)
    l2admin_password = models.CharField(max_length=20)

    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)

    post_save.connect(create_user_profile, sender=User)


class UserProfileForm(ModelForm):
    user = forms.CharField(show_hidden_initial=True)
    class Meta:
        model = UserProfile