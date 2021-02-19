from django.db import models


class Dataset(models.Model):
    uid = models.CharField(max_length=200, primary_key=True)
    name = models.CharField(max_length=500)
    parent = models.CharField(max_length=500)
    info = models.TextField()
    content = models.TextField()

