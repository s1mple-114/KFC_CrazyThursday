from django.shortcuts import render
from rest_framework import viewsets, permissions, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction
from django.db.models import Sum, F
import logging
from user.permissions import IsOwnerOrStaff, IsStaffUser  # 导入权限类
from .models import OrderItem  # 保持类名为驼峰命名
from .serializers import OrderItemSerializer, BatchOrderItemSerializer  # 添加批量序列化器

logger = logging.getLogger(__name__)

class OrderItemViewSet(mixins.ListModelMixin,  # 获取订单项列表
                      mixins.RetrieveModelMixin,  # 获取单个订单项详情
                      mixins.CreateModelMixin,  # 创建订单项
                      mixins.UpdateModelMixin,  # 更新订单项
                      mixins.DestroyModelMixin,  # 删除订单项
                      viewsets.GenericViewSet):  # 保持类名为驼峰命名
    queryset = OrderItem.objects.all().select_related('order', 'product')  # 预加载关联数据
    serializer_class = OrderItemSerializer   # 使用订单项序列化器
    pagination_class = None  # 禁用分页，返回所有数据
    
    def get_permissions(self):
        """更精细的权限控制"""
        if self.action in ['create', 'update', 'partial_update', 'destroy', 'batch_create']:
            # 创建、修改、删除订单项需要员工权限
            return [IsStaffUser()]
        elif self.action == 'list':
            # 查看所有订单项需要员工权限
            return [IsStaffUser()]
        elif self.action in ['retrieve', 'by_order', 'summary']:
            # 查看单个订单项或按订单查询需要是该订单的所有者或员工
            return [IsOwnerOrStaff()]
        # 所有订单项操作都需要认证
        return [permissions.IsAuthenticated()]
    
    def get_queryset(self):
        # 数据隔离：用户只能看自己的订单项，店员能看所有
        user = self.request.user
        queryset = OrderItem.objects.all()
        
        if user.is_authenticated and user.role == "customer":
            # 顾客只能看到自己订单中的订单项
            queryset = queryset.filter(order__user=user)
        
        # 添加查询过滤功能
        order_id = self.request.query_params.get('order_id')
        product_id = self.request.query_params.get('product_id')
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        
        if order_id:
            queryset = queryset.filter(order_id=order_id)
        if product_id:
            queryset = queryset.filter(product_id=product_id)
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        
        # 添加排序功能
        sort_by = self.request.query_params.get('sort_by', 'id')
        order = self.request.query_params.get('order', 'asc')
        
        if order == 'desc':
            sort_by = f'-{sort_by}'
        
        queryset = queryset.order_by(sort_by)
        
        return queryset
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        # 支持按订单ID筛选
        order_id = request.query_params.get('order_id')
        if order_id:
            queryset = queryset.filter(order_id=order_id)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    def finalize_response(self, request, response, *args, **kwargs):
        """为所有响应添加缓存控制头"""
        if isinstance(response, Response):
            response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
            response['Pragma'] = 'no-cache'
            response['Expires'] = '0'
            response['Content-Type'] = 'application/json; charset=utf-8'
        return super().finalize_response(request, response, *args, **kwargs)
    
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        """创建订单项，添加事务支持和数据验证"""
        try:
            # 验证订单是否存在且状态允许添加订单项
            order_id = request.data.get('order')
            if not order_id:
                return Response({
                    "status": "error",
                    "message": "订单ID不能为空"
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # 调用父类方法创建订单项
            response = super().create(request, *args, **kwargs)
            logger.info(f"创建订单项成功：订单ID={order_id}, 产品ID={request.data.get('product')}")
            return response
        except Exception as e:
            logger.error(f"创建订单项失败：{str(e)}")
            return Response({
                "status": "error",
                "message": f"创建订单项失败: {str(e)}"
            }, status=status.HTTP_400_BAD_REQUEST)
    
    @transaction.atomic
    def update(self, request, *args, **kwargs):
        """更新订单项，添加事务支持"""
        try:
            instance = self.get_object()
            # 确保价格不低于0
            if 'price' in request.data and float(request.data['price']) < 0:
                return Response({
                    "status": "error",
                    "message": "价格不能为负数"
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # 确保数量不低于1
            if 'quantity' in request.data and int(request.data['quantity']) < 1:
                return Response({
                    "status": "error",
                    "message": "数量不能少于1"
                }, status=status.HTTP_400_BAD_REQUEST)
            
            response = super().update(request, *args, **kwargs)
            logger.info(f"更新订单项成功：ID={kwargs.get('pk')}")
            return response
        except Exception as e:
            logger.error(f"更新订单项失败：ID={kwargs.get('pk')}, 错误：{str(e)}")
            return Response({
                "status": "error",
                "message": f"更新订单项失败: {str(e)}"
            }, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def by_order(self, request):
        """根据订单ID获取该订单的所有订单项，优化查询性能"""
        order_id = request.query_params.get('order_id')
        if not order_id:
            return Response({
                "status": "error",
                "message": "order_id is required"
            }, status=status.HTTP_400_BAD_REQUEST)

        user = request.user
        queryset = OrderItem.objects.filter(order_id=order_id).select_related('product')
        
        # 权限检查：普通用户只能查看自己订单的订单项
        if user.is_authenticated and user.role == "customer":
            queryset = queryset.filter(order__user=user)
        
        # 计算订单项总金额
        total_amount = queryset.aggregate(total=Sum(F('price') * F('quantity')))['total'] or 0
        
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "status": "success",
            "order_id": order_id,
            "total_amount": total_amount,
            "items_count": queryset.count(),
            "items": serializer.data
        })
    
    @action(detail=False, methods=['get'], permission_classes=[IsStaffUser])
    def summary(self, request):
        """获取订单项统计信息"""
        # 获取产品销售统计
        product_summary = OrderItem.objects.values('product__name', 'product__category')
            .annotate(
                total_quantity=Sum('quantity'),
                total_revenue=Sum(F('price') * F('quantity'))
            )
            .order_by('-total_quantity')[:10]  # 前10名热销产品
        
        # 获取类别销售统计
        category_summary = OrderItem.objects.values('product__category')
            .annotate(
                total_quantity=Sum('quantity'),
                total_revenue=Sum(F('price') * F('quantity'))
            )
            .order_by('-total_revenue')
        
        return Response({
            "status": "success",
            "product_summary": product_summary,
            "category_summary": category_summary
        })
    
    @transaction.atomic
    @action(detail=False, methods=['post'], permission_classes=[IsStaffUser])
    def batch_create(self, request):
        """批量创建订单项，提高效率"""
        serializer = BatchOrderItemSerializer(data=request.data)
        if serializer.is_valid():
            try:
                order_items = serializer.save()
                logger.info(f"批量创建订单项成功：共{len(order_items)}个订单项")
                return Response({
                    "status": "success",
                    "message": f"成功创建{len(order_items)}个订单项",
                    "items": OrderItemSerializer(order_items, many=True).data
                }, status=status.HTTP_201_CREATED)
            except Exception as e:
                logger.error(f"批量创建订单项失败：{str(e)}")
                return Response({
                    "status": "error",
                    "message": f"批量创建失败: {str(e)}"
                }, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({
            "status": "error",
            "message": "数据验证失败",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
