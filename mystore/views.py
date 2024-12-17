from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, Http404
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required, user_passes_test

from mystore.forms import *
from mystore.models import *

CART_SESSION_ID = 'cart'

class Cart:
    def __init__(self, request):
        """Giỏ hàng dùng sesssion"""
        self.session = request.session
        cart = self.session.get(CART_SESSION_ID)
        if not cart:
            cart = self.session[CART_SESSION_ID] = {}
        self.cart = cart

    def __iter__(self):
        product_ids = self.cart.keys()
        cart = []
        for product_id in product_ids:
            cart.append(self.cart[product_id])
        return iter(cart)
    
    def add(self, masp, quantity):
        """Thêm sản phẩm vào giỏ hàng"""
        product = get_object_or_404(sp,pk=masp)
        masp = str(masp)
        if masp not in self.cart:
            self.cart[masp] = {'quantity': 0, 'tensp': product.tensp, 'gia': product.gia, 'hinhanh' : product.hinhanh.path, 'masp': masp}
        self.cart[masp]['quantity'] += int(quantity)
        self.save()

    def modify_cart(self, masp, order):
        """Tăng giảm số lượng giỏ hàng"""
        masp = str(masp)
        if masp not in self.cart: pass
        if order == 'minus':
            self.cart[masp]['quantity'] -= 1
            if self.cart[masp]['quantity'] == 0: del self.cart[masp]
        elif order == 'plus':
            self.cart[masp]['quantity'] += 1
        elif order == 'delete':
            del self.cart[masp]
        self.save()

    def get_total_price(self):
        """Tổng tiền giỏ hàng"""
        return sum(cart_item['gia']*cart_item['quantity'] for cart_item in self)

    def save(self):
        self.session.modified = True

    def clear(self):
        """Xóa toàn bộ giỏ hàng"""
        self.session['cart'] = {}

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
    cart = Cart(request)
    tongtien = cart.get_total_price()
    return render(request, 'giohang.html', {'cart': cart, 'tongtien': tongtien})

def add_to_cart(request):
    if request.method != 'POST': return redirect('product_detail')
    masp = request.POST.get('masp')
    quantity = request.POST.get('quantity')
    cart = Cart(request)
    cart.add(masp=masp, quantity=quantity)
    return redirect('giohang')

def modify_cart(request):
    if request.method != 'POST': return redirect('giohang')
    masp, order = request.POST.get('order').split('-')
    cart = Cart(request)
    cart.modify_cart(masp, order)
    return redirect('giohang')

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

def search_product(request):
    """Tìm kiếm sản phẩm"""
    ds_sp = sp
    if request.method == "POST":
        ch = request.POST.get('searched')
        ds_sp = sp.objects.filter(tensp__contains=ch)
    context = {'ds_sp': ds_sp}
    return render(request, 'product_searched.html', context)

def thanhtoan(request, user_id):
    """Thêm hóa đơn và chi tiêt hóa đơn vào database"""
    user = User.objects.get(pk=user_id)
    cart = Cart(request)
    tongtien = cart.get_total_price()
    #Lưu hóa đơn
    invoice = hoadon.objects.create(user=user, trigia=tongtien)

    #Lưu chi tiêt hóa đơn
    for cart_item in cart:
        product_id = cart_item['masp']
        product = sp.objects.get(pk=product_id)
        quantity = cart_item['quantity']
        invoice_detail = cthd.objects.create(sohd=invoice, masp=product, sl=quantity)

    cart.clear()
    return redirect('index')