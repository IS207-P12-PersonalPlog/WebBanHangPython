from django.contrib import admin
from .models import *
# Register your models here.
class UserAccountAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'user_name', 'ho_ten', 'so_dt')
    search_fields = ('ho_ten',)
admin.site.register(brands)
admin.site.register(categories)
admin.site.register(sp)
admin.site.register(hoadon)
admin.site.register(cthd)