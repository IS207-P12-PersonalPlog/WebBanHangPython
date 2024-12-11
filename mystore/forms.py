from django import forms
from django.forms import ModelForm

from mystore.models import *


class AddProductForm(ModelForm):
    class Meta:
        model = sp
        fields = ['tensp', 'dvt', 'nuocsx', 'gia', 'brand_id', 'category_id']

    def __init__(self, *args, **kwargs):
        super(AddProductForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
