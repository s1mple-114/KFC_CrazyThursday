from django.db import models

class User(models.Model):
    # 角色选项：顾客/店员
    ROLE_CHOICES = (
        ('ROLE_CUSTOMER', '顾客'),
        ('ROLE_STAFF', '店员'),
    )
    username = models.CharField(max_length=50, unique=True)  # 用户名（不重复）
    password = models.CharField(max_length=128)  # 密码（Django自动加密）
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)  # 角色
    created_time = models.DateTimeField(auto_now_add=True)  # 创建时间（自动填）

    # 后台显示用户名，方便查看
    def __str__(self):
        return self.username