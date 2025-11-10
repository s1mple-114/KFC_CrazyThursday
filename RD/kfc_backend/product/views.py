from django.shortcuts import render
from rest_framework import viewsets, filters, mixins
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from django.db.models import Q
import logging
from user.permissions import IsStaffUser
from .models import Product
from .serializers import ProductSerializer

logger = logging.getLogger(__name__)

class BaseViewSetWithCacheControl(viewsets.GenericViewSet):
    """基础视图集，提供通用的缓存控制和响应处理"""
    
    def finalize_response(self, request, response, *args, **kwargs):
        """为所有响应添加缓存控制头"""
        if isinstance(response, Response):
            response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
            response['Pragma'] = 'no-cache'
            response['Expires'] = '0'
            response['Content-Type'] = 'application/json; charset=utf-8'
        return super().finalize_response(request, response, *args, **kwargs)

class ProductViewSet(mixins.ListModelMixin,  # 获取商品列表
                    mixins.RetrieveModelMixin, # 获取单个商品详情
                    mixins.CreateModelMixin,   # 创建商品
                    mixins.UpdateModelMixin,   # 更新商品
                    mixins.DestroyModelMixin,  # 删除商品
                    BaseViewSetWithCacheControl):
    
    # 默认查询集使用select_related优化
    queryset = Product.objects.select_related().filter(is_available=True)
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'category']
    ordering_fields = ['price', 'created_time']
    ordering = ['-created_time']  # 默认按创建时间倒序
    
    def get_queryset(self):
        # 管理员和员工可以看到所有商品（包括下架的）
        if hasattr(self.request.user, 'role') and self.request.user.role in ['staff', 'admin']:
            queryset = Product.objects.select_related()
        else:
            # 普通用户只能看到上架的商品
            queryset = Product.objects.select_related().filter(is_available=True)
            
        # 多条件过滤
        filters = Q()
        
        # 分类过滤
        category = self.request.query_params.get('category')
        if category:
            filters &= Q(category=category)
        
        # 可用性过滤
        is_available = self.request.query_params.get('is_available')
        if is_available is not None:
            is_available = is_available.lower() == 'true'
            filters &= Q(is_available=is_available)
            
        # 名称搜索（支持模糊搜索）
        name = self.request.query_params.get('name')
        if name:
            filters &= Q(name__icontains=name)
        
        # 价格区间过滤
        min_price = self.request.query_params.get('min_price')
        if min_price:
            try:
                filters &= Q(price__gte=float(min_price))
            except ValueError:
                logger.warning(f"Invalid min_price value: {min_price}")
                
        max_price = self.request.query_params.get('max_price')
        if max_price:
            try:
                filters &= Q(price__lte=float(max_price))
            except ValueError:
                logger.warning(f"Invalid max_price value: {max_price}")
        
        if filters:
            queryset = queryset.filter(filters)
            
        # 添加日志
        if self.request.query_params:
            logger.info(f"Product query with filters: {self.request.query_params}")
            
        return queryset
    
    def get_permissions(self):
        # 权限控制更精确
        if self.action in ['create', 'update', 'destroy']:
            return [IsStaffUser()]  # 增删改需要员工权限
        # 列表和详情页公开访问
        return [AllowAny()]
    
    def perform_create(self, serializer):
        """创建商品时记录日志"""
        product = serializer.save()
        logger.info(f"Product created: {product.name} by user: {self.request.user.username}")
        return product
    
    @action(detail=True, methods=['patch'], permission_classes=[IsStaffUser()])
    def toggle_availability(self, request, pk=None):
        """切换商品上下架状态的便捷接口"""
        try:
            product = self.get_object()
            product.is_available = not product.is_available
            product.save()
            status_text = "上架" if product.is_available else "下架"
            logger.info(f"Product {product.name} {status_text} by user: {request.user.username}")
            return Response({
                "status": "success",
                "message": f"商品{status_text}成功",
                "is_available": product.is_available
            }, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error toggling product availability: {str(e)}")
            return Response({
                "status": "error",
                "message": "操作失败",
                "error": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def categories(self, request):
        """获取所有商品分类"""
        categories = Product.objects.values_list('category', flat=True).distinct()
        return Response({
            "categories": list(categories),
            "count": len(categories)
        })
# Create your views here.
