import requests
from test_token import test_get_token
# 步骤1：获取Token
token,u,p=test_get_token()
token_url = "http://localhost:8000/api/token/"
auth_data = {
    "username": u,
    "password": p
}
token_response = requests.post(token_url, data=auth_data)
if token_response.status_code != 200:
    print(f"Token获取失败:{token_response.text}")
else:
    print(f"获取到Token:{token}")

    # 步骤2：访问产品接口（替换为实际路径）
    product_url = "http://localhost:8000/api/products/products/"
    headers = {"Authorization": f"Token {token}"}
    product_response = requests.get(product_url, headers=headers)
    print(f"产品接口状态码：{product_response.status_code}")
    print(f"产品接口响应：{product_response.text}")