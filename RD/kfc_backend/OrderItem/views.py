from django.shortcuts import render
from rest_framework import viewsets,permissions
# from rest_framework.permissions import IsAuthenticated
from user.permissions import IsOwnerOrStaff  # 导入“所有者或店员”权限类
from .models import OrderItem  # 保持类名为驼峰命名
from .serializers import OrderItemSerializer  # 保持类名为驼峰命名

class OrderItemViewSet(viewsets.ModelViewSet):  # 保持类名为驼峰命名
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    # permission_classes = [IsAuthenticated]
    def get_queryset(self):
        # 数据隔离：用户只能看自己的购物车，店员能看所有
        user = self.request.user
        if user.role == "customer":
            return OrderItem.objects.filter(user=user)
        return OrderItem.objects.all()

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy", "list", "retrieve"]:
            # 购物车【所有操作】→ 用户自己可操作，店员可查看/管理
            return [IsOwnerOrStaff()]
        # 其他操作默认要求“登录”
        return [permissions.IsAuthenticated()]
    
    def get_queryset(self):
        return OrderItem.objects.filter(order__user=self.request.user)
