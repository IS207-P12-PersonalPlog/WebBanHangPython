from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.template import loader
from django.template.loader import get_template
from django.urls import reverse
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required, user_passes_test

from mystore.forms import *
from mystore.models import *


def product_detail(request, tensp):
    product = sp.objects.get(tensp=tensp)
    return render(request, 'product_detail.html', {'product': product})

def product_card(request):
    """Load sản phẩm theo giá hoặc loại sản phẩm"""
    sort_by = request.GET.get('sort_by', None)
    category = request.GET.get('category', None)

    products = sp.objects.all()

    if category != 'None' and category:
        #products = filter(lambda x: x.category_id == category, products)
        products = products.filter(category_id = category)
    if sort_by == 'asc':
        products = sorted(products, key=(lambda x: x.gia))
    elif sort_by == 'desc':
        products = sorted(products, key=(lambda x: x.gia), reverse=True)

    context = {
        'products': products,
        'category': category,
    }
    template = loader.get_template('index.html')
    return HttpResponse(template.render(context, request))


def user_login(request):
    """Đăng nhập tài khoản người dùng"""
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')  # Chuyển hướng sau khi đăng nhập thành công
    else:
        form = AuthenticationForm()

    context = {
        'form': form,
    }
    template = get_template('login.html')
    return HttpResponse(template.render(context, request))

def user_register(request):
    """Đăng ký tài khoản người dùng"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    context = {'title': 'Register', 'form': form}
    return render(request, 'register.html', context)

def user_logout(request):
    logout(request)
    return redirect('login')

def admin_page(request):

    return render(request, 'admin.html')

def is_manager(useraccount):
    try:
        if not useraccount.is_superuser:
            raise Http404
        return True
    except:
        raise Http404

@user_passes_test(is_manager)
@login_required
def add_product(request):
    if request.method == 'POST':
        form = AddProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product added Successfuly!')
            return redirect('add_product')
    else:
        form = AddProductForm()
    context = {'title':'Add Product', 'form':form}
    return render(request, 'add_product.html', context)
