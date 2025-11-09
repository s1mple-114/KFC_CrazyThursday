from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = (
        ('customer', '顾客'),
        ('staff', '员工'),
        ('admin', '管理员'),
    )
    phone = models.CharField(max_length=15, blank=True, null=True, db_index=True)  # 手机号，添加索引便于查找
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='customer', db_index=True)  # 角色，添加索引用于权限过滤
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)  # 创建时间，添加索引用于排序

    # 修复Meta类缩进
    class Meta:
        db_table = 'user' # 数据库表名
        verbose_name = '用户' # 单数显示名称
        verbose_name_plural = '用户' # 复数显示名称

     # 方便后续权限判断的快捷方法
    @property
    def is_staff_user(self):
        """判断是否为店员"""
        return self.role == 'staff'

    @property
    def is_customer(self):
        """判断是否为顾客"""
        return self.role == 'customer'

    # 后台显示用户名，方便查看
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"