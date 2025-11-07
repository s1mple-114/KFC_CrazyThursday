from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import login, logout
# 导入DRF自带的Token模型
from rest_framework.authtoken.models import Token
from .permissions import IsOwnerOrStaff, IsStaffUser
from .models import User
from .serializers import UserSerializer, UserRegistrationSerializer, LoginSerializer
from rest_framework.authentication import TokenAuthentication  # 导入认证类（用于关闭接口认证）


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()  # 数据查询集
    serializer_class = UserSerializer  # 默认序列化器

    def get_permissions(self):
        if self.action in ['register', 'login']:
            return [AllowAny()]  # 注册和登录不需要认证
        elif self.action == "list":
            return [IsStaffUser()]  # 用户列表仅允许员工或管理员访问
        elif self.action in ["retrieve", "update", "partial_update"]:
            return [IsOwnerOrStaff()]  # 查看/修改用户信息需要是本人或员工/管理员
        elif self.action == "destroy":
            return [IsStaffUser()]  # 删除用户仅允许员工或管理员
        return [IsAuthenticated()]  # 其他操作需要登录

    # 【修改1：给login接口添加authentication_classes，关闭认证拦截】
    @action(
        detail=False, 
        methods=['post'], 
        permission_classes=[AllowAny],
        authentication_classes=[]  # 关闭当前接口的Token认证（匿名可访问）
    )
    def login(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                "token": token.key,
                "user": UserSerializer(user).data,
                "message": "登录成功"
            }, status=status.HTTP_200_OK)
        return Response({"message":"登录失败"},serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 【新增：补全register接口，并配置匿名访问】
    @action(
        detail=False, 
        methods=['post'], 
        permission_classes=[AllowAny],
        authentication_classes=[]  # 关闭认证拦截（注册接口无需Token）
    )
    def register(self, request):
        # 使用注册专用序列化器处理数据
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()  # 执行用户创建（需确保UserRegistrationSerializer有create方法）
            # 注册成功后生成Token，直接返回给前端
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                "user": UserSerializer(user).data,
                "token": token.key,
                "message": "注册成功"
            }, status=status.HTTP_201_CREATED)
        return Response({"message":"注册失败"},serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def logout(self, request):
        request.user.auth_token.delete()
        return Response({'message': '登出成功(Token已删除)'})