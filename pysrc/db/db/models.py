from django.db import models


class Dataset(models.Model):
    name = models.CharField(max_length=500)
    parent = models.CharField(max_length=500)
    info = models.TextField()
    content = models.TextField()  # JSON


class Model(models.Model):
    name = models.CharField(max_length=500, primary_key=True)
    content = models.TextField()  # JSON


class Fit(models.Model):
    name = models.CharField(max_length=500, primary_key=True)
    content = models.TextField()  # JSON

