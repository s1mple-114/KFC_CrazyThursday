from django.shortcuts import render
from rest_framework import viewsets, permissions, mixins
from rest_framework.response import Response
from user.permissions import IsOwnerOrStaff  # 导入“所有者或店员”权限类
from .models import OrderItem  # 保持类名为驼峰命名
from .serializers import OrderItemSerializer  # 保持类名为驼峰命名

class OrderItemViewSet(mixins.ListModelMixin,  # 获取订单项列表
                      mixins.RetrieveModelMixin,  # 获取单个订单项详情
                      mixins.CreateModelMixin,  # 创建订单项
                      mixins.UpdateModelMixin,  # 更新订单项
                      mixins.DestroyModelMixin,  # 删除订单项
                      viewsets.GenericViewSet):  # 保持类名为驼峰命名
    queryset = OrderItem.objects.all()  # 默认查询所有订单项
    serializer_class = OrderItemSerializer   # 使用订单项序列化器
    pagination_class = None  # 禁用分页，返回所有数据
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        # 支持按订单ID筛选
        order_id = request.query_params.get('order_id')
        if order_id:
            queryset = queryset.filter(order_id=order_id)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    def get_queryset(self):
        # 数据隔离：用户只能看自己的订单项，店员能看所有
        user = self.request.user
        if user.is_authenticated and user.role == "customer":
            # 顾客只能看到自己订单中的订单项
            return OrderItem.objects.filter(order__user=user)
        # 员工或管理员可以看到所有订单项
        return OrderItem.objects.all()

    def get_permissions(self):
        # 所有订单项操作都需要认证
        return [permissions.IsAuthenticated()]
        # 权限检查将在get_queryset中通过数据过滤实现
