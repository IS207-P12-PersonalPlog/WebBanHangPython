from django.contrib.admin.filters import FacetsMixin
from django.db import models
from django.contrib.auth.models import User
import uuid

# # Create your models here.
class brands(models.Model):
    brand_id = models.CharField(max_length=100, primary_key=True)
    brand_title = models.CharField(max_length=100)
    def __str__(self):
        return self.brand_title

class categories(models.Model):
    category_id = models.CharField(max_length=100, primary_key=True)
    category_title = models.CharField(max_length=100)
    def __str__(self):
        return self.category_title

class sp(models.Model):
    masp = models.AutoField(primary_key=True)
    tensp = models.CharField(max_length=100, unique=True)
    dvt = models.CharField(max_length=30, default=1)
    nuocsx = models.CharField(max_length=70, default="China")
    gia = models.IntegerField(default=0)#
    brand_id = models.ForeignKey(brands, on_delete=models.CASCADE, null=True)#
    category_id = models.ForeignKey(categories, on_delete=models.CASCADE, null=True)#
    hinhanh = models.ImageField(blank=True, null=True)

    def __str__(self):
        return f'{self.category_id} - {self.tensp}'

class hoadon(models.Model):
    sohd = models.AutoField(primary_key=True)
    nghd = models.DateTimeField(auto_now_add=True)
    # user_id = models.ForeignKey(useraccount, on_delete=models.CASCADE)#
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    trigia = models.IntegerField()#
    def __str__(self):
        return f'{self.sohd} - {self.user}'

class cthd(models.Model):
    sohd = models.ForeignKey(hoadon, on_delete=models.CASCADE)#
    masp = models.ForeignKey(sp, on_delete=models.CASCADE) #
    sl = models.SmallIntegerField()
    def __str__(self):
        return f'{self.sohd} - {self.masp} - {self.sl}'

