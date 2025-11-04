from rest_framework import permissions

class IsStaffUser(permissions.BasePermission):
    """
    仅允许员工访问的权限类
    """
    def has_permission(self, request, view):
        # 已登录且角色为员工
        return request.user.is_authenticated and request.user.role == 'staff'

class IsCustomerUser(permissions.BasePermission):
    """
    仅允许顾客访问的权限类
    """
    def has_permission(self, request, view):
        # 已登录且角色为顾客
        return request.user.is_authenticated and request.user.role == 'customer'

class IsOwnerOrStaff(permissions.BasePermission):
    """
    对象级权限：仅允许订单所有者（顾客）或员工操作
    """
    def has_object_permission(self, request, view, obj):
        # 员工拥有所有订单的操作权限
        if request.user.is_authenticated and request.user.role == 'staff':
            return True
        # 顾客仅能操作自己的订单
        return obj.user == request.user