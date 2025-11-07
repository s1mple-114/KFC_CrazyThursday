import requests
import json

print("===== 验证权限修复 =====")

# 1. 普通用户登录
print("\n1. 普通用户登录...")
login_url = "http://localhost:8000/api/auth/users/login/"
login_data = {"username": "frontend", "password": "test123456"}
login_response = requests.post(login_url, json=login_data)
print(f"登录状态码: {login_response.status_code}")

if login_response.status_code == 200:
    token = login_response.json().get("token")
    print(f"获取到token: {token}")
    
    # 2. 测试普通用户访问用户列表接口（应该被拒绝）
    print("\n2. 测试普通用户访问用户列表接口...")
    user_list_url = "http://localhost:8000/api/auth/users/"
    headers = {"Authorization": f"Token {token}"}
    user_list_response = requests.get(user_list_url, headers=headers)
    
    print(f"访问状态码: {user_list_response.status_code}")
    print(f"响应内容: {user_list_response.text}")
    
    # 3. 验证修复是否成功
    if user_list_response.status_code == 403:
        print("\n✅ 修复成功！普通用户现在无法访问用户列表接口")
    else:
        print("\n❌ 修复失败！普通用户仍然可以访问用户列表接口")
    
    # 4. 测试普通用户访问自己的信息（应该成功）
    print("\n3. 测试普通用户访问自己的信息...")
    user_id = login_response.json().get("user", {}).get("id")
    if user_id:
        own_info_url = f"http://localhost:8000/api/auth/users/{user_id}/"
        own_info_response = requests.get(own_info_url, headers=headers)
        print(f"访问状态码: {own_info_response.status_code}")
        if own_info_response.status_code == 200:
            print("✅ 普通用户可以正常访问自己的信息")
        else:
            print("❌ 普通用户无法访问自己的信息")
else:
    print("登录失败，无法继续测试")

print("\n===== 验证完成 =====")