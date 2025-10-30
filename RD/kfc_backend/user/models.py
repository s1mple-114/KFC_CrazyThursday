from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = (
        ('customer', '顾客'),
        ('staff', '员工'),
        ('admin', '管理员'),
    )
    phone = models.CharField(max_length=15, blank=True, null=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='customer')
    created_at = models.DateTimeField(auto_now_add=True)

class Meta:
    db_table = 'user'
    verbose_name = '用户'
    verbose_name_plural = '用户'


    # 后台显示用户名，方便查看
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"