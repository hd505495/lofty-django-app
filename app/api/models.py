from django.db import models

class KeyValue(models.Model):
    key = models.CharField(primary_key=True, max_length=1024)
    value = models.IntegerField(default=0)

class DogImage(models.Model):
    image = models.ImageField(upload_to ='dogs/')
    filename = models.CharField(blank=False, max_length=128)
    height = models.PositiveIntegerField()
    width = models.PositiveIntegerField()
    format = models.CharField(max_length=8, blank=True, null=True)
    mode = models.CharField(max_length=8, blank=True, null=True)
    frames = models.PositiveIntegerField(blank=True, null=True)
    bits = models.PositiveIntegerField(blank=True, null=True)
    layers = models.PositiveIntegerField(blank=True, null=True)

