import requests
import json

# 1. 普通用户登录
def test_normal_user_login():
    print("测试普通用户登录...")
    url = "http://localhost:8000/api/auth/users/login/"
    data = {"username": "frontend", "password": "test123456"}
    response = requests.post(url, json=data)
    print(f"登录状态码: {response.status_code}")
    if response.status_code == 200:
        token = response.json().get("token")
        print(f"获取到token: {token}")
        return token
    else:
        print(f"登录失败: {response.text}")
        return None

# 2. 测试普通用户访问管理员接口
def test_normal_user_access_admin_api(token):
    if not token:
        return
    
    print("\n测试普通用户访问管理员接口...")
    url = "http://localhost:8000/api/auth/users/"
    headers = {"Authorization": f"Token {token}"}
    response = requests.get(url, headers=headers)
    print(f"访问管理员接口状态码: {response.status_code}")
    print(f"响应内容: {response.text}")
    
    # 检查是否有权限错误
    if "permission" in response.text.lower() or "not allowed" in response.text.lower() or response.status_code == 403:
        print("✅ 权限控制正常: 普通用户无法访问管理员接口")
    else:
        print("❌ 权限控制可能有问题")

# 3. 测试管理员账号登录
def test_admin_login():
    print("\n测试管理员账号登录...")
    url = "http://localhost:8000/api/auth/users/login/"
    data = {"username": "admin", "password": "admin123456"}
    response = requests.post(url, json=data)
    print(f"管理员登录状态码: {response.status_code}")
    print(f"管理员登录响应: {response.text}")
    return response.status_code

if __name__ == "__main__":
    print("===== 管理员权限接口测试 =====")
    
    # 测试普通用户权限
    token = test_normal_user_login()
    test_normal_user_access_admin_api(token)
    
    # 尝试管理员登录
    admin_login_status = test_admin_login()
    
    print("\n===== 测试完成 =====")