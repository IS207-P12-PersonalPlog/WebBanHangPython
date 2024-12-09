from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.urls import reverse

from mystore.models import brands
from mystore.models import sp


def product_detail(request, tensp):
    product = sp.objects.get(tensp=tensp)
    return render(request, 'product_detail.html', {'product': product})

def product_card(request):
    sort_by = request.GET.get('sort_by', None)

    if sort_by == 'asc':
        products = sp.objects.order_by('gia')
    elif sort_by == 'desc':
        products = sp.objects.order_by('-gia')
    else:
        products = sp.objects.all()
    products_per_page = 9
    current_page = int(request.GET.get('page', 1))
    offset = (current_page - 1) * products_per_page

    total_products = sp.objects.count()
    total_pages = (total_products + products_per_page - 1) // products_per_page

    context = {
        'products': products,
        'current_page': current_page,
        'total_pages': total_pages,
    }
    template = loader.get_template('index.html')
    return HttpResponse(template.render(context, request))