from django.shortcuts import render
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly ,IsAuthenticated
from rest_framework.permissions import AllowAny
from user.permissions import IsStaffUser  # 导入“仅店员”权限类
from .models import Product
from .serializers import ProductSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'category']
    ordering_fields = ['price', 'created_at']
    
    def get_queryset(self):
        queryset = Product.objects.filter(is_available=True)
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category=category)
        return queryset
    def get_permissions(self):
        # 场景：商品上架/下架/修改（只有店员能操作）
        if self.action in ['create', 'update', 'destroy']:
            return [IsStaffUser()]
        # 场景：浏览商品（公开接口，无需登录）
        return [AllowAny()]
# Create your views here.
