from django.db import models
from order.models import Order
from product.models import Product

class OrderItem(models.Model):
    order = models.ForeignKey('order.Order', on_delete=models.CASCADE, related_name='items', verbose_name='订单', db_index=True)
    product = models.ForeignKey('product.Product', on_delete=models.CASCADE, verbose_name='产品', db_index=True)
    quantity = models.PositiveIntegerField(default=1, verbose_name='数量', db_index=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='单价', db_index=True)
    
    class Meta:
        db_table = 'order_item'
        indexes = [
            # 复合索引，优化按订单和商品的联合查询
            models.Index(fields=['order', 'product']),
            # 复合索引，优化价格区间查询
            models.Index(fields=['price', 'quantity']),
        ]

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

    @property
    def subtotal(self):
        return self.quantity * self.price