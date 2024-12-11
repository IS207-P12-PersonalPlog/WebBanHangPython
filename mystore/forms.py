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

class registerForm(ModelForm):
    class Meta:
        model = useraccount
        fields = ['user_name', 'user_password', 'ho_ten', 'so_dt']

    def __init__(self, *args, **kwargs):
        super(registerForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    user_name = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'username'}
        )
    )
    user_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'password'}
        )
    )
    ho_ten = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'ho ten'}
        )
    )
    so_dt = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'sdt'}
        )
    )