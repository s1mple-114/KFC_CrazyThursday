from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = (
        ('customer', '顾客'),
        ('staff', '员工'),
        ('admin', '管理员'),
    )
    phone = models.CharField(max_length=15, blank=True, null=True)  # 手机号，可选
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='customer')
    created_at = models.DateTimeField(auto_now_add=True)  # 创建时间，自动设置

     # 方便后续权限判断的快捷方法
    @property
    def is_staff_user(self):
        """判断是否为店员"""
        return self.role == 'staff'

    @property
    def is_customer(self):
        """判断是否为顾客"""
        return self.role == 'customer'

class Meta:
    db_table = 'user' # 数据库表名
    verbose_name = '用户' # 单数显示名称
    verbose_name_plural = '用户' # 复数显示名称


    # 后台显示用户名，方便查看
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"