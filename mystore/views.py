from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from mystore.models import brands
from mystore.models import sp


def test(request):
    brand = brands.objects.all().values()
    Sp = sp.objects.all().values()
    template = loader.get_template('index.html')
    context = {
        'brand': brand,
        'sp': Sp,
    }
    return HttpResponse(template.render(context, request))