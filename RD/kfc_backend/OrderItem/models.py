from django.db import models

from order.models import Order
from produce.models import Product

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name='订单')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='产品')
    quantity = models.PositiveIntegerField(default=1, verbose_name='数量')
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='单价')
    
    class Meta:
        db_table = 'order_item'
        verbose_name = '订单项'
        verbose_name_plural = '订单项'

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

    @property
    def subtotal(self):
        return self.quantity * self.price

# Create your models here.
