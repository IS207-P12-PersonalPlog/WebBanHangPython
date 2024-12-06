from django.db import models

# Create your models here.
#Chua biet dat the ngoai
class useraccount(models.Model):
    user_id = models.CharField(auto_created=True, max_length=4)
    user_password = models.CharField(max_length=40)
    ho_ten = models.CharField(max_length=40, default="Nguyen Van A")
    so_dt = models.CharField(max_length=10, default=None)

class brands(models.Model):
    brand_id = models.CharField(max_length=100, primary_key=True)
    brand_title = models.CharField(max_length=100)

class categories(models.Model):
    category_id = models.CharField(max_length=100, primary_key=True)
    category_title = models.CharField(max_length=100)

class sp(models.Model):
    MASP = models.CharField(max_length=4, primary_key=True, auto_created=True)
    TENSP = models.CharField(max_length=100)
    DVT = models.CharField(max_length=30, default=1)
    NUOCSX = models.CharField(max_length=100, default="China")
    GIA = models.IntegerField(default=0)#Chua biet co kieu money hay ko
    brand_id = models.CharField(max_length=100)#
    category_id = models.CharField(max_length=100)#
    HINHANH = models.CharField(max_length=100)

class hoadon(models.Model):
    SOHD = models.IntegerField(primary_key=True, auto_created=True)
    NGHD = models.DateTimeField()
    user_id = models.CharField(max_length=4)#
    TRIGIA = models.IntegerField()#Chua biet co kieu money hay ko

class cthd(models.Model):
    SOHD = models.IntegerField()#
    MASP = models.CharField(max_length=4) #
    SL = models.SmallIntegerField()