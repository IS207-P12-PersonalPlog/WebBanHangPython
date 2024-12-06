from django.db import models
import uuid

# Create your models here.
#Chua biet dat the ngoai
class useraccount(models.Model):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_password = models.CharField(max_length=40)
    ho_ten = models.CharField(max_length=40, default="Nguyen Van A")
    so_dt = models.CharField(max_length=10, default=None, blank=True)
    allow_edit = models.BooleanField(default=False)

class brands(models.Model):
    brand_id = models.CharField(max_length=100, primary_key=True)
    brand_title = models.CharField(max_length=100)

# categories(models.Model):
    #category_id = models.CharField(max_length=100, primary_key=True)
    #category_title = models.CharField(max_length=100)

class sp(models.Model):
    masp = models.CharField(max_length=4, primary_key=True, auto_created=True)
    tensp = models.CharField(max_length=100)
    dvt = models.CharField(max_length=30, default=1)
    nuocsx = models.CharField(max_length=100, default="China")
    gia = models.IntegerField(default=0)#Chua biet co kieu money hay ko
    brand_id = models.ForeignKey(brands, on_delete=models.CASCADE)#
    #category_id = models.CharField(max_length=100)#
    hinhanh = models.ImageField(upload_to='images/')

class hoadon(models.Model):
    sohd = models.IntegerField(primary_key=True, auto_created=True)
    nghd = models.DateTimeField(auto_now_add=True)
    user_id = models.ForeignKey(useraccount, on_delete=models.CASCADE)#
    trigia = models.IntegerField()#Chua biet co kieu money hay ko

class cthd(models.Model):
    sohd = models.ForeignKey(hoadon, on_delete=models.CASCADE)#
    masp = models.ForeignKey(sp, on_delete=models.CASCADE) #
    sl = models.SmallIntegerField()