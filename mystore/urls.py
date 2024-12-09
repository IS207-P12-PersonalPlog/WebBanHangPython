from django.urls import path
from . import views
#load image
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.product_card, name='index'),
    path('product/<str:tensp>/', views.product_detail, name='product_detail'),
]

#load image
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)