import requests
def test_get_token():
    # 替换为你的Token接口URL（通常是/api/token/）
    url = "http://localhost:8000/api/token/"  
    u=input('输入账号')
    p=input('输入密码')
    # 替换为测试账号的用户名和密码
    data = {
        "username": u,  
        "password": p     
    }
    response = requests.post(url, data=data)
    print(f"🔑 Token接口响应:{response.json()}")
    # 新增：返回获取到的Token
    return response.json()["token"],u,p

if __name__ == "__main__":
    test_get_token()