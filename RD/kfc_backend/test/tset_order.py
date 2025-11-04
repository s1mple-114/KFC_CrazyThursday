import pytest
import requests

# 全局配置
BASE_URL = "http://127.0.0.1:8000"
CUSTOMER_TOKEN = "顾客的Token"  # 从/api/token/获取
STAFF_TOKEN = "店员的Token"    # 从/api/token/获取

def test_get_orders_unauthorized():
    """未登录用户访问订单列表,预期401"""
    response = requests.get(f"{BASE_URL}/api/orders/")
    assert response.status_code == 401

def test_get_orders_customer():
    """顾客访问自己的订单列表,预期200"""
    headers = {"Authorization": f"Token {CUSTOMER_TOKEN}"}
    response = requests.get(f"{BASE_URL}/api/orders/", headers=headers)
    assert response.status_code == 200
    assert len(response.json()) > 0

def test_update_order_status_staff():
    """店员更新订单状态,预期200"""
    headers = {"Authorization": f"Token {STAFF_TOKEN}"}
    data = {"status": "已完成"}
    response = requests.post(
        f"{BASE_URL}/api/orders/1/update_status/",
        json=data,
        headers=headers
    )
    assert response.status_code == 200
    assert response.json()["status"] == "已完成"