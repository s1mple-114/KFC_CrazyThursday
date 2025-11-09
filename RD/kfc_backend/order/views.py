from django.shortcuts import render
from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
import random
import string
from .models import Order
from .serializers import OrderSerializer

class OrderViewSet(mixins.ListModelMixin,  # 获取订单列表
                   mixins.RetrieveModelMixin,  # 获取单个订单详情
                   mixins.CreateModelMixin,  # 创建新订单
                   mixins.UpdateModelMixin,  # 更新订单
                   mixins.DestroyModelMixin,  # 删除订单
                   viewsets.GenericViewSet):  # 基础视图集
    queryset = Order.objects.all()  # 默认查询集
    serializer_class = OrderSerializer  # 序列化器
    permission_classes = [IsAuthenticated]  # 需要认证才能访问
    pagination_class = None  # 禁用分页
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        # 添加缓存控制头，禁止浏览器缓存响应
        response = Response(serializer.data)
        response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        return response
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'customer':
            return Order.objects.filter(user=user)  # 客户只能看到自己的订单
        return Order.objects.all()  # 其他角色（如管理员）看到所有订单
    
    def perform_create(self, serializer):
        order_number = 'KFC' + ''.join(random.choices(string.digits, k=10))
        serializer.save(user=self.request.user, order_number=order_number)
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