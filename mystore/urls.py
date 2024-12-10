from django.urls import path
from . import views
#load image
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('index/', views.product_card, name='index'),
    path('product_detail/<str:tensp>/', views.product_detail, name='product_detail'),
    path('login/', views.user_login, name='login'),
    path('register/', views.user_register, name='register'),
    path('logout/', views.user_logout, name='logout'),
    path('add_product/', views.add_product, name='add_product'),
]

#load image
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)