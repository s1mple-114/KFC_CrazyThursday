from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
import random
import string

# from kfc_backend import order
from user import permissions
from .models import Order
from .serializers import OrderSerializer
from user.permissions import IsStaffUser,IsCustomerUser,IsOwnerOrStaff #导入自定义权限

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    # permission_classes = [IsAuthenticated] 注释掉原本内容
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'customer':
            return Order.objects.filter(user=user)
        return Order.objects.all()
    
    def perform_create(self, serializer):
        # 生成订单号
        order_number = 'KFC' + ''.join(random.choices(string.digits, k=10))
        serializer.save(user=self.request.user, order_number=order_number)
    
    # 关键：重写get_permissions，为不同操作分配不同权限
    def get_permissions(self):
        if self.action == 'create':
            # 【只有顾客能“创建订单”】
            return [IsCustomerUser()]
        elif self.action in ['list', 'retrieve']:
            # 【顾客只能看自己的订单，店员能看所有订单】
            return [IsOwnerOrStaff()]
        elif self.action == 'update_status':
            # 【只有店员能“更新订单状态”】
            return [IsStaffUser()]
        # 其他操作（如destroy等），可根据需求补充权限
        return [permissions.IsAuthenticated()]  # 默认要求“登录”
    
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
# Create your views here.
