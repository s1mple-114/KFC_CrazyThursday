from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import orderitem  # 保持类名为驼峰命名
from .serializers import orderitemSerializer  # 保持类名为驼峰命名

class orderitemViewSet(viewsets.ModelViewSet):  # 保持类名为驼峰命名
    queryset = orderitem.objects.all()
    serializer_class = orderitemSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return orderitem.objects.filter(order__user=self.request.user)
