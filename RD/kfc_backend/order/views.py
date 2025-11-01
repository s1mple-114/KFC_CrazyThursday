from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
import random
import string
from .models import Order
from .serializers import OrderSerializer
from OrderItem.serializers import OrderItemSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'customer':
            return Order.objects.filter(user=user)
        return Order.objects.all()
    
    def perform_create(self, serializer):
        # 生成订单号
        order_number = 'KFC' + ''.join(random.choices(string.digits, k=10))
        serializer.save(user=self.request.user, order_number=order_number)
    
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
