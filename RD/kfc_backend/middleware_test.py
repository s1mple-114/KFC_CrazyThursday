import os
import sys
import django

# 添加项目路径到 Python 路径
project_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kfc_management.settings')

try:
    django.setup()
    
    from django.conf import settings
    print("=== 中间件诊断 ===")
    print("MIDDLEWARE配置:")
    for i, middleware in enumerate(settings.MIDDLEWARE):
        print(f"  {i+1}. {middleware}")
    
    print(f"\nDEBUG模式: {settings.DEBUG}")
    print(f"ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}")
    
    # 检查 REST_FRAMEWORK 配置
    print(f"\nREST_FRAMEWORK配置:")
    rf_config = getattr(settings, 'REST_FRAMEWORK', {})
    print(f"  DEFAULT_PERMISSION_CLASSES: {rf_config.get('DEFAULT_PERMISSION_CLASSES', '未设置')}")
    print(f"  DEFAULT_AUTHENTICATION_CLASSES: {rf_config.get('DEFAULT_AUTHENTICATION_CLASSES', '未设置')}")
    
except Exception as e:
    print(f"诊断失败: {e}")