from django.db import models

class Product(models.Model):
    # 商品分类选项
    CATEGORY_CHOICES = (
        ('BURGER', '汉堡'),
        ('SNACK', '小食'),
        ('DRINK', '饮料'),
        ('COMBO', '套餐'),
    )
    
    name = models.CharField(max_length=100, db_index=True)  # 商品名称，添加索引用于搜索
    price = models.DecimalField(max_digits=8, decimal_places=2, db_index=True)  # 价格，添加索引用于排序
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, db_index=True)  # 分类，添加索引用于筛选
    description = models.TextField(blank=True)  # 描述（可选）
    image = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name='产品图片')
    created_time = models.DateTimeField(auto_now_add=True, db_index=True)  # 创建时间，添加索引用于排序

    # 后台显示商品名和价格
    def __str__(self):
        return f"{self.name} - ¥{self.price}"