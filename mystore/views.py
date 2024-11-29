from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from mystore.models import brands


def test(request):
    brand = brands.objects.all().values()
    template = loader.get_template('index.html')
    context = {
        'brand': brand,
    }
    return HttpResponse(template.render(context, request))