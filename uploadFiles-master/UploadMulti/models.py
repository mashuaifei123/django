from __future__ import unicode_literals

from django.db import models
# from .views import username_1
import os
# Create your models here.

class Photo(models.Model):
    title = models.CharField(max_length=255, blank=True)
    file = models.FileField(upload_to='input/')
    uploaded_at = models.DateTimeField(auto_now_add=True)


class tsmcode(models.Model):
    title = models.CharField(max_length=255, blank=True)
    file = models.FileField(upload_to='tsminput/')
    uploaded_at = models.DateTimeField(auto_now_add=True)


class spss(models.Model):
    title = models.CharField(max_length=255, blank=True)
    file = models.FileField(upload_to='spssinput/')
    uploaded_at = models.DateTimeField(auto_now_add=True)


class xzx(models.Model):
    title = models.CharField(max_length=255, blank=True)
    file = models.FileField(upload_to='xzxinput/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

class word(models.Model):
    title = models.CharField(max_length=255, blank=True)
    file = models.FileField(upload_to='wordinput/')
    uploaded_at = models.DateTimeField(auto_now_add=True)