from django.db import models

class KeyValue(models.Model):
    key = models.CharField(primary_key=True, max_length=1024)
    value = models.IntegerField(default=0)