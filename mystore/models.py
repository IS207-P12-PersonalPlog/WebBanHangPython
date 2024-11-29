from django.db import models

# Create your models here.
class brands(models.Model):
    brand_id = models.CharField(max_length=100, primary_key=True)
    brand_title = models.CharField(max_length=100)