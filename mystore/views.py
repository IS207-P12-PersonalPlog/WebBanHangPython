from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, Http404
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required, user_passes_test
from unicodedata import category

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
            self.cart[masp] = {'quantity': 0, 'tensp': product.tensp, 'gia': product.gia,
            # 'hinhanh' : product.hinhanh.path,
            'masp': masp}
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

def init_data(request):
    """Khởi tạo dữ liệu cho brands, categories và sp"""
    if not User.objects.filter(username='admin').exists():
        superuser = User.objects.create_superuser(username='admin', email='admin@example.com', password='admin')

        brands.objects.bulk_create([
            brands(brand_id='acer', brand_title='Acer'),
            brands(brand_id='apple', brand_title='Apple'),
            brands(brand_id='asus', brand_title='Asus'),
            brands(brand_id='dell', brand_title='Dell'),
            brands(brand_id='havit', brand_title='Havit'),
            brands(brand_id='hp', brand_title='HP'),
            brands(brand_id='lenovo', brand_title='Lenovo'),
            brands(brand_id='msi', brand_title='MSI'),
            brands(brand_id='nokia', brand_title='Nokia'),
            brands(brand_id='oppo', brand_title='Oppo'),
            brands(brand_id='samsung', brand_title='Samsung'),
            brands(brand_id='sony', brand_title='Sony'),
            brands(brand_id='xiaomi', brand_title='Xiaomi')
        ])
        acer_brand = brands.objects.get(brand_id='acer')
        apple_brand = brands.objects.get(brand_id='apple')
        asus_brand = brands.objects.get(brand_id='asus')
        dell_brand = brands.objects.get(brand_id='dell')
        havit_brand = brands.objects.get(brand_id='havit')
        hp_brand = brands.objects.get(brand_id='hp')
        lenovo_brand = brands.objects.get(brand_id='lenovo')
        msi_brand = brands.objects.get(brand_id='msi')
        nokia_brand = brands.objects.get(brand_id='nokia')
        oppo_brand = brands.objects.get(brand_id='oppo')
        samsung_brand = brands.objects.get(brand_id='samsung')
        sony_brand = brands.objects.get(brand_id='sony')
        xiaomi_brand = brands.objects.get(brand_id='xiaomi')

        categories.objects.bulk_create([
            categories(category_id='headphone', category_title='Headphone'),
            categories(category_id='laptop', category_title='Laptop'),
            categories(category_id='phone', category_title='Phone'),
            categories(category_id='tivi', category_title='Tivi')
        ])
        headphone_category = categories.objects.get(category_id='headphone')
        laptop_category = categories.objects.get(category_id='laptop')
        phone_category = categories.objects.get(category_id='phone')
        tivi_category = categories.objects.get(category_id='tivi')

        sp.objects.bulk_create([
            sp(tensp='iPhone 16 Pro Max', dvt='vnd', nuocsx='China', gia=34290000, brand_id=apple_brand,
               category_id=phone_category),
            sp(tensp='Samsung Galaxy S24 Ultra', dvt='vnd', nuocsx='China', gia=27990000, brand_id=samsung_brand,
               category_id=phone_category),
            sp(tensp='iPhone 13', dvt='vnd', nuocsx='China', gia=13450000, brand_id=apple_brand, category_id=phone_category),
            sp(tensp='Laptop MSI Modern 14 C13M-607VN', dvt='vnd', nuocsx='China', gia=14990000, brand_id=msi_brand,
               category_id=laptop_category),
            sp(tensp='Laptop MSI Gaming GF63 Thin 11UC-1228VN', dvt='vnd', nuocsx='China', gia=16990000,
               brand_id=msi_brand,
               category_id=laptop_category),
            sp(tensp='Tai nghe Bluetooth True Wireless Havit TW948', dvt='vnd', nuocsx='China', gia=190000,
               brand_id=havit_brand, category_id=headphone_category),
            sp(tensp='Samsung Galaxy A16 5G', dvt='vnd', nuocsx='China', gia=6090000, brand_id=samsung_brand,
               category_id=phone_category),
            sp(tensp='Samsung Galaxy A15', dvt='vnd', nuocsx='China', gia=4990000, brand_id=samsung_brand,
               category_id=phone_category),
            sp(tensp='Samsung Galaxy Z Fold6', dvt='vnd', nuocsx='China', gia=43990000, brand_id=samsung_brand,
               category_id=phone_category),
            sp(tensp='Xiaomi Redmi 14C', dvt='Cai', nuocsx='China', gia=3290000, brand_id=xiaomi_brand,
               category_id=phone_category),
            sp(tensp='Xiaomi 14T', dvt='Cai', nuocsx='China', gia=13990000, brand_id=xiaomi_brand,
               category_id=phone_category),
            sp(tensp='Xiaomi POCO X6 Pro', dvt='Cai', nuocsx='China', gia=9990000, brand_id=xiaomi_brand,
               category_id=phone_category),
            sp(tensp='Xiaomi Redmi Note 13 Pro Plus', dvt='Cai', nuocsx='China', gia=10990000, brand_id=xiaomi_brand,
               category_id=phone_category),
            sp(tensp='OPPO Find X8', dvt='Cai', nuocsx='China', gia=22990000, brand_id=oppo_brand,
               category_id=phone_category),
            sp(tensp='OPPO A3', dvt='Cai', nuocsx='China', gia=4990000, brand_id=oppo_brand,
               category_id=phone_category),
            sp(tensp='OPPO Reno12 5G', dvt='Cai', nuocsx='China', gia=12990000, brand_id=oppo_brand,
               category_id=phone_category),
            sp(tensp='OPPO Reno12 F 5G', dvt='Cai', nuocsx='China', gia=9490000, brand_id=oppo_brand,
               category_id=phone_category),
            sp(tensp='Nokia 110 4G Pro', dvt='Cai', nuocsx='China', gia=750000, brand_id=nokia_brand,
               category_id=phone_category),
            sp(tensp='Nokia 220 4G', dvt='Cai', nuocsx='China', gia=990000, brand_id=nokia_brand,
               category_id=phone_category),
            sp(tensp='Nokia HMD 105 4G', dvt='Cai', nuocsx='China', gia=650000, brand_id=nokia_brand,
               category_id=phone_category),
            sp(tensp='Nokia 3210 4G', dvt='Cai', nuocsx='China', gia=1550000, brand_id=nokia_brand,
               category_id=phone_category),
            sp(tensp='Laptop Acer Aspire 3 Spin 14', dvt='Cai', nuocsx='China', gia=14990000, brand_id=acer_brand,
               category_id=laptop_category),
            sp(tensp='Laptop Gaming Acer Nitro 5 Tiger', dvt='Cai', nuocsx='China', gia=27990000, brand_id=acer_brand,
               category_id=laptop_category),
            sp(tensp='Laptop Acer Gaming Aspire 7', dvt='Cai', nuocsx='China', gia=23990000, brand_id=acer_brand,
               category_id=laptop_category),
            sp(tensp='Laptop Acer Gaming Aspire 5', dvt='Cai', nuocsx='China', gia=20490000, brand_id=acer_brand,
               category_id=laptop_category),
            sp(tensp='Apple MacBook Air M2 2024 8CPU', dvt='Cai', nuocsx='China', gia=24990000, brand_id=apple_brand,
               category_id=laptop_category),
            sp(tensp='Apple MacBook Air M1', dvt='Cai', nuocsx='China', gia=22990000, brand_id=apple_brand,
               category_id=laptop_category),
            sp(tensp='MacBook Air M3 13 inch 2024', dvt='Cai', nuocsx='China', gia=27990000, brand_id=apple_brand,
               category_id=laptop_category),
            sp(tensp='MacBook Pro 14 M3', dvt='Cai', nuocsx='China', gia=39990000, brand_id=apple_brand,
               category_id=laptop_category),
            sp(tensp='Laptop ASUS Vivobook 15', dvt='Cai', nuocsx='China', gia=16490000, brand_id=asus_brand,
               category_id=laptop_category),
            sp(tensp='Laptop ASUS Vivobook 14', dvt='Cai', nuocsx='China', gia=20490000, brand_id=asus_brand,
               category_id=laptop_category),
            sp(tensp='Laptop ASUS Vivobook GO 15', dvt='Cai', nuocsx='China', gia=14490000, brand_id=asus_brand,
               category_id=laptop_category),
            sp(tensp='Laptop ASUS Gaming VivoBook', dvt='Cai', nuocsx='China', gia=25290000, brand_id=asus_brand,
               category_id=laptop_category),
            sp(tensp='Laptop Dell Inspiron 15 3520', dvt='Cai', nuocsx='China', gia=13990000, brand_id=dell_brand,
               category_id=laptop_category),
            sp(tensp='Laptop Dell Vostro 3520', dvt='Cai', nuocsx='China', gia=11990000, brand_id=dell_brand,
               category_id=laptop_category),
            sp(tensp='Laptop Dell Latitude 3540', dvt='Cai', nuocsx='China', gia=18990000, brand_id=dell_brand,
               category_id=laptop_category),
            sp(tensp='Laptop Dell Inspiron 15 3530', dvt='Cai', nuocsx='China', gia=22990000, brand_id=dell_brand,
               category_id=laptop_category),
            sp(tensp='Laptop HP 15S-FQ5231TU', dvt='Cai', nuocsx='China', gia=11990000, brand_id=hp_brand,
               category_id=laptop_category),
            sp(tensp='Laptop HP Pavilion 15-EG2083TU', dvt='Cai', nuocsx='China', gia=19790000, brand_id=hp_brand,
               category_id=laptop_category),
            sp(tensp='Laptop HP Pavilion X360 14-EK2017TU', dvt='Cai', nuocsx='China', gia=24990000, brand_id=hp_brand,
               category_id=laptop_category),
            sp(tensp='Laptop HP Envy X360 2IN1 14-FC0162TU', dvt='Cai', nuocsx='China', gia=29890000, brand_id=hp_brand,
               category_id=laptop_category),
            sp(tensp='Laptop Lenovo LOQ 15IAX9', dvt='Cai', nuocsx='China', gia=23990000, brand_id=lenovo_brand,
               category_id=laptop_category),
            sp(tensp='Laptop Lenovo IdeaPad Slim 5 14Q8X9', dvt='Cai', nuocsx='China', gia=24990000,
               brand_id=lenovo_brand,
               category_id=laptop_category),
            sp(tensp='Laptop Lenovo IdeaPad Slim 3 14IAH8', dvt='Cai', nuocsx='China', gia=15490000,
               brand_id=lenovo_brand,
               category_id=laptop_category),
            sp(tensp='Laptop Lenovo Legion 5 15IRX9', dvt='Cai', nuocsx='China', gia=37990000, brand_id=lenovo_brand,
               category_id=laptop_category),
            sp(tensp='Laptop MSI Gaming Thin 15 B12UCX', dvt='Cai', nuocsx='China', gia=17990000, brand_id=msi_brand,
               category_id=laptop_category),
            sp(tensp='Laptop MSI Gaming GF63 Thin 11UC', dvt='Cai', nuocsx='China', gia=20990000, brand_id=msi_brand,
               category_id=laptop_category),
            sp(tensp='Laptop MSI Katana 15 B13VFK', dvt='Cai', nuocsx='China', gia=36990000, brand_id=msi_brand,
               category_id=laptop_category),
            sp(tensp='Laptop MSI Gaming Thin 15 B13UC', dvt='Cai', nuocsx='China', gia=21990000, brand_id=msi_brand,
               category_id=laptop_category),
            sp(tensp='Tai nghe Bluetooth chụp tai Sony WH-1000XM5', dvt='Cai', nuocsx='China', gia=7990000,
               brand_id=sony_brand,
               category_id=headphone_category),
            sp(tensp='Tai nghe Bluetooth chụp tai Sony WH-CH520', dvt='Cai', nuocsx='China', gia=1290000,
               brand_id=sony_brand,
               category_id=headphone_category),
            sp(tensp='Tai nghe Bluetooth chụp tai Sony WH-1000XM4', dvt='Cai', nuocsx='China', gia=6690000,
               brand_id=sony_brand,
               category_id=headphone_category),
            sp(tensp='Tai nghe Bluetooth chụp tai Sony WH-CH720N', dvt='Cai', nuocsx='China', gia=2990000,
               brand_id=sony_brand,
               category_id=headphone_category),
            sp(tensp='Tai nghe Bluetooth Apple AirPods 4', dvt='Cai', nuocsx='China', gia=3350000, brand_id=apple_brand,
               category_id=headphone_category),
            sp(tensp='Tai nghe Bluetooth Apple AirPods 2', dvt='Cai', nuocsx='China', gia=2990000, brand_id=apple_brand,
               category_id=headphone_category),
            sp(tensp='Tai nghe Bluetooth Apple AirPods 3 2022', dvt='Cai', nuocsx='China', gia=3590000,
               brand_id=apple_brand,
               category_id=headphone_category),
            sp(tensp='Tai nghe Bluetooth True Wireless Samsung Galaxy Buds2 Pro', dvt='Cai', nuocsx='China',
               gia=2590000, brand_id=samsung_brand,
               category_id=headphone_category),
            sp(tensp='Tai nghe Bluetooth True Wireless Samsung Galaxy Buds 3 Pro', dvt='Cai', nuocsx='China',
               gia=5090000, brand_id=samsung_brand,
               category_id=headphone_category),
            sp(tensp='Tai nghe Bluetooth True Wireless Samsung Galaxy Buds FE', dvt='Cai', nuocsx='China', gia=1390000,
               brand_id=samsung_brand,
               category_id=headphone_category),
            sp(tensp='Tai nghe Bluetooth True Wireless Xiaomi Redmi Buds 6 Active', dvt='Cai', nuocsx='China',
               gia=490000, brand_id=xiaomi_brand,
               category_id=headphone_category),
            sp(tensp='Tai nghe Bluetooth True Wireless Redmi Buds 4 Lite', dvt='Cai', nuocsx='China', gia=390000,
               brand_id=xiaomi_brand,
               category_id=headphone_category),
            sp(tensp='Tai nghe Bluetooth True Wireless Xiaomi Redmi Buds 5', dvt='Cai', nuocsx='China', gia=990000,
               brand_id=xiaomi_brand,
               category_id=headphone_category),
            sp(tensp='Tai nghe Bluetooth True Wireless Gaming ROG Cetra', dvt='Cai', nuocsx='China', gia=1590000,
               brand_id=asus_brand,
               category_id=headphone_category),
            sp(tensp='Tai nghe có dây Gaming ASUS ROG Cetra II Core', dvt='Cai', nuocsx='China', gia=840000,
               brand_id=asus_brand,
               category_id=headphone_category),
            sp(tensp='Tai nghe chụp tai Gaming Asus TUF H1', dvt='Cai', nuocsx='China', gia=740000, brand_id=asus_brand,
               category_id=headphone_category),
            sp(tensp='Tai nghe Bluetooth chụp tai Havit H630BT', dvt='Cai', nuocsx='China', gia=390000,
               brand_id=havit_brand,
               category_id=headphone_category),
            sp(tensp='Tai nghe Bluetooth True Wireless Havit TW981', dvt='Cai', nuocsx='China', gia=190000,
               brand_id=havit_brand,
               category_id=headphone_category),
            sp(tensp='Tai nghe Bluetooth True Wireless Havit TW969', dvt='Cai', nuocsx='China', gia=199000,
               brand_id=havit_brand,
               category_id=headphone_category),
            sp(tensp='Smart Tivi Samsung QLED 4K 50 inch 2024 (50Q60D)', dvt='Cai', nuocsx='China', gia=11490000,
               brand_id=samsung_brand,
               category_id=tivi_category),
            sp(tensp='Smart Tivi Samsung UHD 4K 43 inch UA43AU7002', dvt='Cai', nuocsx='China', gia=6690000,
               brand_id=samsung_brand,
               category_id=tivi_category),
            sp(tensp='Smart Tivi Samsung UHD 4K 55 INCH 2024 (55DU8000)', dvt='Cai', nuocsx='China', gia=10490000,
               brand_id=samsung_brand,
               category_id=tivi_category),
            sp(tensp='Tivi Xiaomi A Pro 4K 43 inch QLED 2025', dvt='Cai', nuocsx='China', gia=6490000,
               brand_id=xiaomi_brand,
               category_id=tivi_category),
            sp(tensp='Tivi Xiaomi A 4K 2025 55 inch', dvt='Cai', nuocsx='China', gia=8490000, brand_id=xiaomi_brand,
               category_id=tivi_category),
            sp(tensp='Tivi Xiaomi A Pro 4K 55 inch QLED 2025', dvt='Cai', nuocsx='China', gia=9490000,
               brand_id=xiaomi_brand,
               category_id=tivi_category),
            sp(tensp='Smart Tivi Sony 4K 55 inch KD-55X75K', dvt='Cai', nuocsx='China', gia=12890000, brand_id=sony_brand,
               category_id=tivi_category),
            sp(tensp='Smart Tivi Sony 4K 65 inch KD-65X75K', dvt='Cai', nuocsx='China', gia=15490000, brand_id=sony_brand,
               category_id=tivi_category),
            sp(tensp='Google Tivi Sony 4K 50 inch (K-50S30)', dvt='Cai', nuocsx='China', gia=15690000, brand_id=sony_brand,
               category_id=tivi_category),
        ])
    return redirect('index')

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
    """Yêu cầu đăng nhập để dùng giỏ hàng"""
    if request.user.is_authenticated:
        cart = Cart(request)
        tongtien = cart.get_total_price()
        return render(request, 'giohang.html', {'cart': cart, 'tongtien': tongtien})
    return redirect('login')

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

def brand_product(request):
    """Liệt kê các sản phẩm theo brand"""
    brand_id = request.GET.get('brand_id', None)
    category_id = request.GET.get('category_id', None)
    sort_by = request.GET.get('sort_by', None)
    products = sp.objects.all()

    if category_id != 'None' and category_id:
        products = products.filter(category_id=category_id)
    if brand_id != 'None' and brand_id:
        products = products.filter(brand_id=brand_id)
    if sort_by == 'asc':
        products = sorted(products, key=(lambda x: x.gia))
    elif sort_by == 'desc':
        products = sorted(products, key=(lambda x: x.gia), reverse=True)

    context = {
        'products': products,
        'brand_id': brand_id,
        'category_id': category_id,
    }
    return render(request, 'brand_product.html', context)