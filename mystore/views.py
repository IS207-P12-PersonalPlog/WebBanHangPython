from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
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
    return render(request, 'index.html', context)

def giohang(request):
    cart_items = cartitem.objects.all()
    return render(request, 'giohang.html', {'cart_items': cart_items})

def add_to_cart(request):
    if request.method == 'POST':
        masp = request.POST.get('masp')
        quantity = request.POST.get('quantity')
        cart_item = cartitem.objects.get_or_create(sp=sp.objects.get(masp=masp), user=request.user)
        cart_item[0].sl += int(quantity)
        cart_item[0].save()
        return redirect('giohang')
    return redirect('product_detail')
    

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
    return render(request, 'login.html', context)

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
    """Đăng xuất tài khoản người dùng"""
    logout(request)
    return redirect('login')

def is_manager(useraccount):
    """Kiểm tra có phải admin"""
    try:
        if not useraccount.is_superuser:
            raise Http404
        return True
    except:
        raise Http404

@user_passes_test(is_manager)
def admin_page(request):
    """Trang dành riêng cho admin"""
    return render(request, 'admin.html')

@user_passes_test(is_manager)
def list_product(request):
    """Hiển thị danh sách sản phẩm cho admin"""
    products = sp.objects.all()
    return render(request, 'list_product.html', {'products': products})

@user_passes_test(is_manager)
def add_product(request):
    """Thêm sản phẩm mới chỉ admin có thể thực hiện"""
    if request.method == 'POST':
        form = AddProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('list_product')
    else:
        form = AddProductForm()
    context = {'title':'Add Product', 'form':form}
    return render(request, 'add_product.html', context)

@user_passes_test(is_manager)
def edit_product(request, masp):
    """Chỉnh sửa sản phẩm chỉ admin có thể thực hiện"""
    product = sp.objects.get(masp=masp)
    if request.method == 'POST':
        form = EditProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('list_product')
    else:
        form = EditProductForm(instance=product)
    context = {'title': 'Edit Product', 'form':form}
    return render(request, 'edit_product.html', context)

@user_passes_test(is_manager)
def delete_product(request, masp):
    """Xóa sản phẩm chỉ admin có thể thực hiện"""
    product = sp.objects.filter(masp=masp).delete()
    return redirect('list_product')