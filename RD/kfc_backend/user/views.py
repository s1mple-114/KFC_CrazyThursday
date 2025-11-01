from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import login, logout
from .models import User
from .serializers import UserSerializer, UserRegistrationSerializer, LoginSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()  # 数据查询集
    serializer_class = UserSerializer  # 默认序列化器
    
    def get_permissions(self):
        if self.action in ['register', 'login']:
            return [AllowAny()]  # 注册和登录不需要认证
        return [IsAuthenticated()]  # 其他操作需要登录
    
    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def register(self, request):
        # 使用专门的注册序列化器
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save() # 创建用户
            return Response({
                'user': UserSerializer(user).data, # 返回用户信息
                'message': '用户注册成功'
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def login(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user'] # 获取验证后的用户
            login(request, user) # Django 会话登录
            return Response({
                'user': UserSerializer(user).data,
                'message': '登录成功'
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'])
    def logout(self, request):
        logout(request) # 结束会话
        return Response({'message': '登出成功'})
# Create your views here.
