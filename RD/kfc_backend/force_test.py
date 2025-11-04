import requests
import time

def test_without_cache():
    """不带任何缓存的测试"""
    print("🧪 强制测试API权限...")
    
    # 使用新的session，不带任何cookie
    session = requests.Session()
    
    # 测试产品接口
    try:
        response = session.get('http://localhost:8000/api/products/products/')
        print(f"产品接口状态: {response.status_code}")
        if response.status_code == 200:
            print("✅ 产品接口正常（无缓存）")
        else:
            print(f"❌ 产品接口失败: {response.text}")
    except Exception as e:
        print(f"❌ 请求异常: {e}")

if __name__ == "__main__":
    test_without_cache()