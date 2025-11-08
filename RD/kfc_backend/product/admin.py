from django.contrib import admin
from .models import Product
# Register your models here.



@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category')
    list_filter = ('category',)
    search_fields = ('name', 'description')

    # 明确指定字段集
    fieldsets = (
        ('基本信息', {
            'fields': ('name', 'description', 'price', 'category')
        }),
        ('其他信息', {
            'fields': ('image',),
            'classes': ('collapse',)
        }),
    )
    

    