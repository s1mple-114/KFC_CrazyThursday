from rest_framework import permissions
from .models import User #导入自定义User模块

class IsStaffUser(permissions.BasePermission):
    """
    仅允许店员访问的权限类
    用于商品管理、所有订单查看等店员专属接口
    """
    def has_permission(self, request, view):
        # 已登录且角色为店员
        return request.user.is_authenticated and request.user.is_staff_user

class IsCustomerUser(permissions.BasePermission):
    """
    仅允许顾客访问的权限类
    用于顾客的购物车、个人订单管理等接口
    """
    def has_permission(self, request, view):
        # 已登录且角色为顾客
        return request.user.is_authenticated and request.user.is_customer

class IsOwnerOrStaff(permissions.BasePermission):
    """
    对象级权限：仅允许订单所有者（顾客）或店员操作
    用于订单详情、更新订单状态等接口
    """
    def has_object_permission(self, request, view, obj):
        # 店员拥有所有订单的操作权限
        if request.user.is_staff_user:
            return True
        # 顾客仅能操作自己的订单（假设订单模型有user字段关联用户）
        return obj.user == request.user