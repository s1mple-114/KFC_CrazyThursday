import requests
import json
import time

# 基础URL
BASE_URL = "http://localhost:8000/api"

def get_json_safely(response):
    """安全获取JSON响应"""
    try:
        return response.json()
    except:
        return {"error": "Non-JSON response", "content": response.text[:100]}

def register_and_login():
    """注册新用户并登录获取token"""
    print("=== 用户注册和登录 ===")
    
    # 生成唯一用户名以避免冲突
    username = f"test_user_{int(time.time())}"
    password = "Test@123456"
    
    # 注册用户
    register_data = {
        "username": username,
        "password": password,
        "email": f"{username}@example.com",
        "phone": "13812345678",
        "role": "customer"
    }
    register_response = requests.post(f"{BASE_URL}/auth/users/register/", json=register_data)
    print(f"注册用户 '{username}': 状态码 {register_response.status_code}")
    
    if register_response.status_code != 201:
        print(f"❌ 注册失败: {get_json_safely(register_response)}")
        return None
    
    # 登录获取token
    login_data = {"username": username, "password": password}
    login_response = requests.post(f"{BASE_URL}/auth/users/login/", json=login_data)
    print(f"登录用户: 状态码 {login_response.status_code}")
    
    if login_response.status_code != 200:
        print(f"❌ 登录失败: {get_json_safely(login_response)}")
        return None
    
    token = login_response.json().get("token")
    print(f"✅ 成功获取token: {token[:10]}...")
    return token

def test_public_endpoints():
    """测试公开接口"""
    print("\n=== 测试公开接口 ===")
    results = {"passed": [], "failed": []}
    
    # 1. 测试产品列表接口
    response = requests.get(f"{BASE_URL}/products/products/")
    print(f"1. 产品列表接口: 状态码 {response.status_code}")
    if response.status_code == 200:
        print("✅ 产品列表接口正常（公开访问）")
        results["passed"].append("产品列表接口")
    else:
        print(f"❌ 失败: {get_json_safely(response)}")
        results["failed"].append("产品列表接口")
    
    # 2. 测试产品筛选接口
    response = requests.get(f"{BASE_URL}/products/products/?category=food")
    print(f"2. 产品筛选接口: 状态码 {response.status_code}")
    if response.status_code == 200:
        print("✅ 产品筛选接口正常（公开访问）")
        results["passed"].append("产品筛选接口")
    else:
        print(f"❌ 失败: {get_json_safely(response)}")
        results["failed"].append("产品筛选接口")
    
    # 3. 测试注册接口
    test_username = f"temp_test_{int(time.time())}"
    register_data = {
        "username": test_username,
        "password": "Temp@123456",
        "email": f"{test_username}@example.com",
        "phone": "13812345679",
        "role": "customer"
    }
    response = requests.post(f"{BASE_URL}/auth/users/register/", json=register_data)
    print(f"3. 用户注册接口: 状态码 {response.status_code}")
    if response.status_code in [200, 201]:
        print("✅ 用户注册接口正常")
        results["passed"].append("用户注册接口")
    else:
        print(f"❌ 失败: {get_json_safely(response)}")
        results["failed"].append("用户注册接口")
    
    return results

def test_authenticated_endpoints(token):
    """测试需要认证的接口"""
    print("\n=== 测试需要认证的接口 ===")
    headers = {"Authorization": f"Token {token}"}
    results = {"passed": [], "failed": []}
    
    # 1. 测试获取订单列表
    response = requests.get(f"{BASE_URL}/orders/orders/", headers=headers)
    print(f"1. 获取订单列表: 状态码 {response.status_code}")
    if response.status_code == 200:
        print("✅ 订单列表接口正常")
        results["passed"].append("订单列表接口")
    else:
        print(f"❌ 失败: {get_json_safely(response)}")
        results["failed"].append("订单列表接口")
    
    # 2. 测试订单项接口（使用正确的URL）
    response = requests.get(f"{BASE_URL}/order-items/order-items/", headers=headers)
    print(f"2. 订单项接口: 状态码 {response.status_code}")
    if response.status_code == 200:
        print("✅ 订单项接口正常")
        results["passed"].append("订单项接口")
    else:
        print(f"❌ 失败: {get_json_safely(response)}")
        results["failed"].append("订单项接口")
    
    # 3. 测试创建订单
    order_data = {
        "total_amount": "29.90",
        "status": "PENDING",
        "payment_method": "CASH"
    }
    response = requests.post(f"{BASE_URL}/orders/orders/", json=order_data, headers=headers)
    print(f"3. 创建订单: 状态码 {response.status_code}")
    if response.status_code == 201:
        print("✅ 订单创建接口正常")
        results["passed"].append("订单创建接口")
    else:
        print(f"❌ 失败: {get_json_safely(response)}")
        results["failed"].append("订单创建接口")
    
    return results

def test_permission_control(token):
    """测试权限控制"""
    print("\n=== 测试权限控制 ===")
    headers = {"Authorization": f"Token {token}"}
    results = {"passed": [], "failed": []}
    
    # 测试普通用户访问用户列表接口（应该被拒绝）
    response = requests.get(f"{BASE_URL}/auth/users/", headers=headers)
    print(f"1. 用户列表接口（普通用户）: 状态码 {response.status_code}")
    if response.status_code == 403:
        print("✅ 权限控制正常，普通用户无法访问用户列表")
        results["passed"].append("用户列表接口权限控制")
    else:
        print(f"❌ 权限控制失败: {get_json_safely(response)}")
        results["failed"].append("用户列表接口权限控制")
    
    # 测试未认证访问需要权限的接口
    response = requests.get(f"{BASE_URL}/auth/users/")
    print(f"2. 用户列表接口（未认证）: 状态码 {response.status_code}")
    if response.status_code == 401:
        print("✅ 正确要求认证")
        results["passed"].append("认证要求")
    else:
        print(f"❌ 未正确要求认证: {get_json_safely(response)}")
        results["failed"].append("认证要求")
    
    return results

def main():
    print("开始全面测试所有接口...\n")
    
    # 测试公开接口
    public_results = test_public_endpoints()
    
    # 注册并登录获取token
    token = register_and_login()
    if not token:
        print("\n无法获取有效token，跳过需要认证的接口测试")
        authenticated_results = {"passed": [], "failed": []}
        permission_results = {"passed": [], "failed": []}
    else:
        # 测试需要认证的接口
        authenticated_results = test_authenticated_endpoints(token)
        
        # 测试权限控制
        permission_results = test_permission_control(token)
    
    # 汇总结果
    total_passed = len(public_results["passed"]) + len(authenticated_results["passed"]) + len(permission_results["passed"])
    total_failed = len(public_results["failed"]) + len(authenticated_results["failed"]) + len(permission_results["failed"])
    
    print("\n" + "="*50)
    print("接口测试总报告")
    print("="*50)
    print(f"\n✅ 通过的接口 ({total_passed}):")
    for item in public_results["passed"] + authenticated_results["passed"] + permission_results["passed"]:
        print(f"  - {item}")
    
    if total_failed > 0:
        print(f"\n❌ 失败的接口 ({total_failed}):")
        for item in public_results["failed"] + authenticated_results["failed"] + permission_results["failed"]:
            print(f"  - {item}")
    
    print("\n" + "="*50)
    print("测试完成！")

if __name__ == "__main__":
    main()