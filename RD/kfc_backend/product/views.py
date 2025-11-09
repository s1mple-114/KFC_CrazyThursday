from django.shortcuts import render
from rest_framework import viewsets, filters, mixins
from rest_framework.permissions import IsAuthenticatedOrReadOnly ,IsAuthenticated
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from user.permissions import IsStaffUser  # 导入“仅店员”权限类
from .models import Product
from .serializers import ProductSerializer

class ProductViewSet(mixins.ListModelMixin,  # 获取商品列表
                    mixins.RetrieveModelMixin, # 获取单个商品详情
                    mixins.CreateModelMixin,   # 创建商品
                    mixins.UpdateModelMixin,   # 更新商品
                    mixins.DestroyModelMixin,  # 删除商品
                    viewsets.GenericViewSet):
    queryset = Product.objects.all()  # 查询所有商品
    serializer_class = ProductSerializer  # 商品序列化器
    permission_classes = [AllowAny]  # 默认允许任何用户访问
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'category']  # 支持按名称和分类搜索
    ordering_fields = ['price', 'created_at']  # 支持按价格和创建时间排序
    pagination_class = None  # 取消分页
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        # 添加缓存控制头，禁止浏览器缓存响应
        # 添加Content-Type确保中文正确显示
        response = Response(serializer.data, content_type='application/json; charset=utf-8')
        response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        return response
    
    def get_queryset(self):
        queryset = Product.objects.all()
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category=category)
        
        # 支持按is_available字段过滤
        is_available = self.request.query_params.get('is_available')
        if is_available is not None:
            # 将字符串转换为布尔值
            is_available = is_available.lower() == 'true'
            queryset = queryset.filter(is_available=is_available)
            
        # 支持按商品名称搜索
        name = self.request.query_params.get('name')
        if name:
            queryset = queryset.filter(name__icontains=name)
            
        return queryset
    
    def get_permissions(self):
        # 场景：商品上架/下架/修改（只有店员能操作）
        if self.action in ['create', 'update', 'destroy']:
            return [IsStaffUser()]
        # 场景：浏览商品（公开接口，无需登录）
        return [AllowAny()]
# Create your views here.
