from django.contrib import admin
from .models import Order
# Register your models here.


class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'user', 'total_amount', 'status', 'created_at')
    list_filter = (
        'status',
        ('created_at', admin.DateFieldListFilter),  # 按日期过滤
    )
    search_fields = ('order_number', 'user__username')
    date_hierarchy = 'created_at' 

admin.site.register(Order, OrderAdmin)

