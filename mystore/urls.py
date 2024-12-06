from django.urls import path
from . import views
#load image
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.test, name='index'),
]

#load image
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)