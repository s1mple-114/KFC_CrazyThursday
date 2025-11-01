from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import OrderItem  # 保持类名为驼峰命名
from .serializers import OrderItemSerializer  # 保持类名为驼峰命名

class OrderItemViewSet(viewsets.ModelViewSet):  # 保持类名为驼峰命名
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return OrderItem.objects.filter(order__user=self.request.user)