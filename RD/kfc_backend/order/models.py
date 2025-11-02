from django.db import models
from user.models import User  # 导入用户模型
from product.models import Product  # 导入商品模型

class Order(models.Model):
    # 订单状态选项
    STATUS_CHOICES = (
        ('PENDING', '待支付'),
        ('PAID', '已支付'),
        ('PREPARING', '制作中'),
        ('READY', '待取餐'),
        ('COMPLETED', '已完成'),
        ('CANCELLED', '已取消'),
    )
    
    # 支付方式选项
    PAYMENT_CHOICES = (
        ('CASH', '现金'),
        ('ALIPAY', '支付宝'),
        ('WECHAT', '微信支付'),
        ('CARD', '银行卡'),
    )
    
    order_number = models.CharField(max_length=20, unique=True)  # 订单号（唯一）
    user = models.ForeignKey('user.User', on_delete=models.CASCADE,related_name='orders')  # 关联用户（用户删除时订单也删除）
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)  # 订单总金额
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')  # 订单状态
    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES)  # 支付方式
    created_at = models.DateTimeField(auto_now_add=True)  # 创建时间
    completed_time = models.DateTimeField(null=True, blank=True)  # 完成时间（可选）
    
    class Meta:
        db_table = 'order'
    # 后台显示订单号和状态
    def __str__(self):
        return f"订单 {self.order_number} - {self.get_status_display()}"