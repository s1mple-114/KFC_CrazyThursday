from django.shortcuts import render
from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from django.db.models import F
import random
import string
import logging
from datetime import datetime
from product.views import BaseViewSetWithCacheControl
from user.permissions import IsStaffUser, IsOwnerOrStaff
from .models import Order
from .serializers import OrderSerializer

logger = logging.getLogger(__name__)

class OrderViewSet(mixins.ListModelMixin,  # 获取订单列表
                   mixins.RetrieveModelMixin,  # 获取单个订单详情
                   mixins.CreateModelMixin,  # 创建新订单
                   mixins.UpdateModelMixin,  # 更新订单
                   viewsets.GenericViewSet):  # 基础视图集
    # 继承缓存控制的基类
    queryset = Order.objects.select_related('user').prefetch_related('orderitem_set__product')
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]  # 默认需要认证
    filterset_fields = ['status', 'payment_method']  # 支持按状态和支付方式过滤
    ordering_fields = ['created_at', 'total_amount']  # 支持按创建时间和总金额排序
    ordering = ['-created_at']  # 默认按创建时间倒序
    
    # 使用事务确保订单创建的原子性
    @transaction.atomic
    def perform_create(self, serializer):
        # 生成更复杂的订单号，包含日期和随机数
        date_part = datetime.now().strftime('%Y%m%d')
        random_part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        order_number = f'KFC-{date_part}-{random_part}'
        
        try:
            # 创建订单并记录日志
            order = serializer.save(user=self.request.user, order_number=order_number)
            logger.info(f"Order created: {order.order_number} by user: {self.request.user.username}")
            return order
        except Exception as e:
            logger.error(f"Failed to create order for user {self.request.user.username}: {str(e)}")
            raise
    
    def get_queryset(self):
        user = self.request.user
        
        # 优化查询，使用select_related和prefetch_related减少数据库查询次数
        queryset = Order.objects.select_related('user').prefetch_related('orderitem_set__product')
        
        # 权限控制：客户只能看到自己的订单
        if user.role == 'customer':
            queryset = queryset.filter(user=user)
        
        # 支持日期范围查询
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        
        if start_date:
            try:
                queryset = queryset.filter(created_at__gte=datetime.fromisoformat(start_date))
            except ValueError:
                logger.warning(f"Invalid start_date format: {start_date}")
        
        if end_date:
            try:
                queryset = queryset.filter(created_at__lte=datetime.fromisoformat(end_date))
            except ValueError:
                logger.warning(f"Invalid end_date format: {end_date}")
                
        # 搜索订单号
        order_number = self.request.query_params.get('order_number')
        if order_number:
            queryset = queryset.filter(order_number__icontains=order_number)
            
        return queryset
    
    # 重写get_permissions，实现更细粒度的权限控制
    def get_permissions(self):
        # 订单删除需要管理员权限
        if self.action == 'destroy':
            return [IsStaffUser()]  # 只有员工或管理员可以删除订单
        # 其他操作使用通用权限
        return [IsOwnerOrStaff()]  # 自己的订单或员工可以访问
    
    @action(detail=True, methods=['patch'], permission_classes=[IsStaffUser()])
    def update_status(self, request, pk=None):
        """更新订单状态的专用接口"""
        order = self.get_object()
        new_status = request.data.get('status')
        
        # 验证状态值是否有效
        valid_statuses = dict(Order.STATUS_CHOICES).keys()
        if not new_status or new_status not in valid_statuses:
            return Response({
                "status": "error",
                "message": f"无效的状态值，请使用: {list(valid_statuses)}"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # 状态验证
        if not order.can_update_to(new_status):
            return Response({
                "status": "error",
                "message": "当前订单状态不允许更新为该状态"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # 更新订单状态
            order.status = new_status
            
            # 如果订单完成，记录完成时间
            if new_status == 'COMPLETED' and not order.completed_time:
                order.completed_time = datetime.now()
                
            order.save()
            logger.info(f"Order {order.order_number} status updated to {new_status} by {request.user.username}")
            
            return Response({
                "status": "success",
                "message": "订单状态更新成功",
                "order": OrderSerializer(order).data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Failed to update order {order.order_number} status: {str(e)}")
            return Response({
                "status": "error",
                "message": "订单状态更新失败",
                "error": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """获取订单统计信息的接口"""
        user = request.user
        
        # 普通用户只能看到自己的统计，管理员可以看到所有
        if user.role == 'customer':
            base_query = Order.objects.filter(user=user)
        else:
            base_query = Order.objects.all()
            
        # 计算各种统计数据
        total_orders = base_query.count()
        total_amount = base_query.aggregate(total=F('total_amount'))['total'] or 0
        pending_orders = base_query.filter(status='PENDING').count()
        completed_orders = base_query.filter(status='COMPLETED').count()
        
        return Response({
            "total_orders": total_orders,
            "total_amount": total_amount,
            "pending_orders": pending_orders,
            "completed_orders": completed_orders,
            "completion_rate": completed_orders / total_orders * 100 if total_orders > 0 else 0
        })
    
    # 继承缓存控制
    def finalize_response(self, request, response, *args, **kwargs):
        """为所有响应添加缓存控制头"""
        if isinstance(response, Response):
            response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
            response['Pragma'] = 'no-cache'
            response['Expires'] = '0'
            response['Content-Type'] = 'application/json; charset=utf-8'
        return super().finalize_response(request, response, *args, **kwargs)
    #功能：自动生成订单号（格式：KFC + 10位随机数字），并设置订单所属用户。
    @action(detail=True, methods=['post'])
    def update_status(self, request, pk=None):
        order = self.get_object()
        new_status = request.data.get('status')
        
        if new_status in dict(Order.STATUS_CHOICES):
            order.status = new_status
            order.save()
            return Response({'message': '订单状态更新成功'})
        return Response(
            {'error': '无效的状态'},
            status=status.HTTP_400_BAD_REQUEST
        )