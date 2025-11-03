from django.contrib import admin
from .models import Product
# Register your models here.



@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'is_available')
    list_filter = ('category', 'is_available')
    search_fields = ('name', 'description')

    # 明确指定字段集
    fieldsets = (
        ('基本信息', {
            'fields': ('name', 'description', 'price', 'category')
        }),
        ('状态和图片', {
            'fields': ('is_available', 'image'),
            'classes': ('collapse',)
        }),
    )
    

    