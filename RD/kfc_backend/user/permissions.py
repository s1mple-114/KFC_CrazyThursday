from rest_framework import permissions

class IsStaffUser(permissions.BasePermission):
    """
    仅允许员工或管理员访问的权限类
    """
    def has_permission(self, request, view):
        # 已登录且角色为员工或管理员
        return request.user.is_authenticated and request.user.role in ['staff', 'admin']

class IsCustomerUser(permissions.BasePermission):
    """
    仅允许顾客访问的权限类
    """
    def has_permission(self, request, view):
        # 已登录且角色为顾客
        return request.user.is_authenticated and request.user.role == 'customer'

class IsOwnerOrStaff(permissions.BasePermission):
    """
    权限类：列表视图仅允许员工/管理员访问，对象操作允许所有者或员工/管理员
    """
    def has_permission(self, request, view):
        # 确保用户已登录
        if not request.user.is_authenticated:
            return False
        
        # 对于列表视图(list)，仅允许员工或管理员访问
        if view.action == 'list':
            return request.user.role in ['staff', 'admin']
        
        # 对于其他视图，只要登录即可（会在对象级权限中进一步控制）
        return True
        
    def has_object_permission(self, request, view, obj):
        # 员工或管理员拥有所有操作权限
        if request.user.role in ['staff', 'admin']:
            return True
        
        # 普通用户只能访问自己的信息
        return obj == request.user