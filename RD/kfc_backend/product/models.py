from django.db import models

class Product(models.Model):
    # 商品分类选项
    CATEGORY_CHOICES = (
        ('BURGER', '汉堡'),
        ('SNACK', '小食'),
        ('DRINK', '饮料'),
        ('COMBO', '套餐'),
    )
    
    name = models.CharField(max_length=100)  # 商品名称
    price = models.DecimalField(max_digits=8, decimal_places=2)  # 价格（小数点后2位）
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)  # 分类
    description = models.TextField(blank=True)  # 描述（可选）
    image_url = models.CharField(max_length=200, blank=True)  # 图片链接（可选）
    is_available = models.BooleanField(default=True)  # 是否上架
    created_time = models.DateTimeField(auto_now_add=True)  # 创建时间

    # 后台显示商品名和价格
    def __str__(self):
        return f"{self.name} - ¥{self.price}"