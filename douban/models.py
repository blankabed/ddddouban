from django.db import models

# Create your models here.
class movie(models.Model):
    movieurl=models.CharField(max_length=150)
    movieimg=models.CharField(max_length=150)
    moviename = models.CharField(max_length=30)
    actoranddirector = models.CharField(max_length=150)
    grade = models.CharField(max_length=30)
    type=models.CharField(max_length=30)
class user(models.Model):
    user=models.CharField(max_length=30)
    password=models.CharField(max_length=30)