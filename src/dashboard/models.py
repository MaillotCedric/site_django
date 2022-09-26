from turtle import title
from django.db import models

# Create your models here.

class Members(models.Model):
  title = models.CharField(max_length=255)
  content = models.CharField(max_length=255)