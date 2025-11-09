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
    
    def can_update_to(self, new_status):
        """验证状态更新是否合法（比如"待支付"才能转"已支付"）"""
        valid_transitions = {
            'PENDING': ['PAID'],
            'PAID': ['COMPLETED'],
        }
        return new_status in valid_transitions.get(self.status, [])
    
    # 支付方式选项
    PAYMENT_CHOICES = (
        ('CASH', '现金'),
        ('ALIPAY', '支付宝'),
        ('WECHAT', '微信支付'),
        ('CARD', '银行卡'),
    )
    
    order_number = models.CharField(max_length=20, unique=True, db_index=True)  # 订单号（唯一），添加索引用于查询
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='orders', db_index=True)  # 关联用户，添加索引用于按用户查询订单
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, db_index=True)  # 订单总金额，添加索引用于排序
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING', db_index=True)  # 订单状态，添加索引用于筛选
    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES, db_index=True)  # 支付方式，添加索引用于统计
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)  # 创建时间，添加索引用于排序
    completed_time = models.DateTimeField(null=True, blank=True, db_index=True)  # 完成时间，添加索引用于统计
    
    class Meta:
        db_table = 'order'
    # 后台显示订单号和状态
    def __str__(self):
        return f"订单 {self.order_number} - {self.get_status_display()}"