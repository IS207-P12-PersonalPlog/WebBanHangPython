from django import forms
from django.forms import ModelForm

from mystore.models import *


class AddProductForm(ModelForm):
    class Meta:
        model = sp
        fields = ['tensp', 'dvt', 'nuocsx', 'gia', 'brand_id', 'category_id', 'hinhanh']

    widgets = {
        'hinhanh': forms.FileInput(),
    }

class EditProductForm(ModelForm):
    class Meta:
        model = sp
        fields = ['tensp', 'dvt', 'nuocsx', 'gia', 'brand_id', 'category_id', 'hinhanh']

    widgets = {
        'hinhanh': forms.FileInput(),
    }