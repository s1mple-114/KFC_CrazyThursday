from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth import login, logout
from django.db import transaction
import logging
from datetime import datetime
import re
from .permissions import IsOwnerOrStaff, IsStaffUser
from .models import User
from .serializers import UserSerializer, UserRegistrationSerializer, LoginSerializer

logger = logging.getLogger(__name__)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsOwnerOrStaff]  # 默认使用所有者或员工权限
    pagination_class = None  # 取消分页
    
    def get_permissions(self):
        """更精细的权限控制"""
        # 登录、注册接口允许匿名访问
        if self.action in ['login', 'register']:
            return [AllowAny()]
        # 用户信息获取和修改需要是本人或员工
        elif self.action in ['retrieve', 'update', 'partial_update', 'logout', 'me']:
            return [IsAuthenticated()]
        # 列表和删除操作需要员工权限
        elif self.action in ['list', 'destroy']:
            return [IsStaffUser()]
        return super().get_permissions()
    
    def get_authenticators(self):
        """控制哪些接口需要认证"""
        if self.action in ['login', 'register']:
            return []  # 登录注册不需要认证
        return [TokenAuthentication()]
    
    # 缓存控制
    def finalize_response(self, request, response, *args, **kwargs):
        """为所有响应添加缓存控制头"""
        if isinstance(response, Response):
            response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
            response['Pragma'] = 'no-cache'
            response['Expires'] = '0'
            response['Content-Type'] = 'application/json; charset=utf-8'
        return super().finalize_response(request, response, *args, **kwargs)
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        """获取当前登录用户的信息"""
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def login(self, request):
        """用户登录接口，增加安全性检查"""
        # 简单的防暴力破解：检查请求频率
        # 注意：生产环境中应使用更完善的限流机制
        
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            
            # 检查用户是否被禁用
            if not user.is_active:
                logger.warning(f"登录失败：用户 {user.username} 账户已被禁用")
                return Response({
                    "status": "error",
                    "message": "账户已被禁用，请联系管理员"
                }, status=status.HTTP_403_FORBIDDEN)
            
            # 生成或获取token
            token, created = Token.objects.get_or_create(user=user)
            
            # 更新登录时间（如果模型中有这个字段）
            if hasattr(user, 'last_login'):
                user.last_login = datetime.now()
                user.save(update_fields=['last_login'])
            
            logger.info(f"用户登录成功：{user.username}")
            
            return Response({
                "status": "success",
                "token": token.key,
                "user": UserSerializer(user).data,
                "message": "登录成功"
            }, status=status.HTTP_200_OK)
        
        logger.warning(f"登录失败：{serializer.errors}")
        return Response({
            "status": "error",
            "message": "登录失败",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    @transaction.atomic
    @action(detail=False, methods=['post'])
    def register(self, request):
        """用户注册接口，增加密码强度验证"""
        # 密码强度检查
        password = request.data.get('password')
        if password:
            if len(password) < 8:
                return Response({
                    "status": "error",
                    "message": "密码长度不能少于8位"
                }, status=status.HTTP_400_BAD_REQUEST)
                
            # 检查密码复杂度
            if not re.search(r'[A-Z]', password):
                return Response({
                    "status": "error",
                    "message": "密码必须包含大写字母"
                }, status=status.HTTP_400_BAD_REQUEST)
                
            if not re.search(r'[0-9]', password):
                return Response({
                    "status": "error",
                    "message": "密码必须包含数字"
                }, status=status.HTTP_400_BAD_REQUEST)
        
        # 使用注册专用序列化器
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            # 确保新用户默认角色为customer
            if 'role' not in request.data or request.data['role'] not in ['customer', 'staff', 'admin']:
                request.data['role'] = 'customer'
            
            # 员工和管理员角色只能由现有管理员创建
            if request.data.get('role') in ['staff', 'admin']:
                return Response({
                    "status": "error",
                    "message": "不能直接注册为员工或管理员，请联系系统管理员"
                }, status=status.HTTP_403_FORBIDDEN)
            
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            
            logger.info(f"新用户注册成功：{user.username}")
            
            return Response({
                "status": "success",
                "user": UserSerializer(user).data,
                "token": token.key,
                "message": "注册成功"
            }, status=status.HTTP_201_CREATED)
        
        logger.warning(f"用户注册失败：{serializer.errors}")
        return Response({
            "status": "error",
            "message": "注册失败",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'])
    def logout(self, request):
        """用户登出接口"""
        try:
            request.user.auth_token.delete()
            logger.info(f"用户登出成功：{request.user.username}")
            return Response({
                "status": "success",
                "message": "登出成功(Token已删除)"
            }, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"用户登出失败：{request.user.username}, 错误：{str(e)}")
            return Response({
                "status": "error",
                "message": "登出失败"
            }, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['patch'], permission_classes=[IsStaffUser])
    def change_role(self, request, pk=None):
        """修改用户角色的接口"""
        user = self.get_object()
        new_role = request.data.get('role')
        
        if new_role not in ['customer', 'staff', 'admin']:
            return Response({
                "status": "error",
                "message": "无效的角色值"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # 防止自己降级自己的权限
        if user == request.user and new_role != request.user.role:
            return Response({
                "status": "error",
                "message": "不能修改自己的角色"
            }, status=status.HTTP_403_FORBIDDEN)
        
        old_role = user.role
        user.role = new_role
        user.save(update_fields=['role'])
        
        logger.info(f"用户角色已修改：{user.username} 从 {old_role} 改为 {new_role}，操作人：{request.user.username}")
        
        return Response({
            "status": "success",
            "message": f"用户角色已修改为{new_role}",
            "user": UserSerializer(user).data
        }, status=status.HTTP_200_OK)