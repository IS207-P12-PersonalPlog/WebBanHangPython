from django import forms
from django.forms import ModelForm
from django.forms import ChoiceField

from mystore.models import *

NUOCSX_CHOICES = [
        ('Vietnam', 'Vietnam'),
        ('China', 'China'),
        ('USA', 'USA'),
    ]

DVT_CHOICES = [
    (1, 1),
]

class AddProductForm(ModelForm):
    class Meta:
        model = sp
        fields = ['tensp', 'dvt', 'nuocsx', 'gia', 'brand_id', 'category_id', 'hinhanh']

    widgets = {
        'hinhanh': forms.FileInput(),
    }
    dvt = ChoiceField(choices= DVT_CHOICES)
    nuocsx = ChoiceField(choices= NUOCSX_CHOICES)

class EditProductForm(ModelForm):
    class Meta:
        model = sp
        fields = ['tensp', 'dvt', 'nuocsx', 'gia', 'brand_id', 'category_id', 'hinhanh']

    widgets = {
        'hinhanh': forms.FileInput(),
    }
    dvt = ChoiceField(choices= DVT_CHOICES)
    nuocsx = ChoiceField(choices= NUOCSX_CHOICES)