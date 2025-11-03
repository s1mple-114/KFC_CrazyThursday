# KFC后端API使用说明

## 基础信息
- 后端地址：`http://192.168.x.x:8000/api/`
- 认证方式：Session认证（登录后自动保存cookie）

## 快速开始

### 1. 用户登录
```http
POST http://192.168.x.x:8000/api/auth/users/login/
Content-Type: application/json

{
  "username": "frontend",
  "password": "test123456"
}
```

### 2. 获取所有产品
```http
GET http://192.168.x.x:8000/api/products/products/
```

### 3. 创建订单
```http
POST http://192.168.x.x:8000/api/orders/orders/
Content-Type: application/json

{
  "total_amount": "50.00",
  "items": [
    {
      "product": 1,
      "quantity": 2,
      "price": "25.00"
    }
  ]
}
```

### 4. 获取我的订单
```http
GET http://192.168.x.x:8000/api/orders/orders/
```

## 测试账号
- 用户名：`frontend`
- 密码：`test123456`