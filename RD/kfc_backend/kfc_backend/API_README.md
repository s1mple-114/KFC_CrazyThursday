# KFC后端API使用说明

## 基础信息
- 后端地址：`http://192.168.x.x:8000/api/`
 认证方式：Session认证（登录后自动保存cookie）  ----组长留言：孩子们报错401就是这个Session干的，我已经改成Token认证了
-          Token认证（登陆后返回Token）

### 注意事项：
1. 支付方式字段使用大写：ALIPAY, WECHAT, CARD
2. 订单状态使用大写：PENDING, PAID, COMPLETED
3. Token认证：需要在Header中添加 Authorization: Token {token}


## 快速开始
#KFC后端API完整接口列表
### 1. 用户注册
POST http://localhost:8000/api/auth/users/register/
Content-Type: application/json

{
  "username": "testuser123",
  "password": "test123456",
  "email": "test123@example.com",
  "phone": "13812345678",
  "role": "customer"
}

### 2. 用户登录
POST http://localhost:8000/api/auth/users/login/
Content-Type: application/json

{
  "username": "frontend",
  "password": "test123456"
}

### 3.用户登出

POST http://localhost:8000/api/auth/users/logout/
认证 ：需要Token认证

### 4.获取用户列表（管理员）
GET http://localhost:8000/api/auth/users/

### 5. 获取所有产品
GET http://localhost:8000/api/products/products/
认证 ：需要Token认证

### 6. 按分类筛选产品
GET http://localhost:8000/api/products/products/?category=burger
参数 ：category=burger（URL查询参数） 
认证 ：需要Token认证

### 7. 创建产品（员工/管理员）
POST http://localhost:8000/api/products/products/
Content-Type: application/json

{
  "name": "新奥尔良烤鸡腿堡",
  "description": "美味的新奥尔良风味",
  "price": "28.00",
  "category": "burger",
  "is_available": true
}

### 8. 更新产品（员工/管理员）
PUT http://localhost:8000/api/products/products/1/
Content-Type: application/json

{
  "name": "香辣鸡腿堡",
  "price": "26.00",
  "is_available": true
}

### 9. 删除产品（员工/管理员）
DELETE http://localhost:8000/api/products/products/1/

### 10.获取我的订单
GET http://localhost:8000/api/orders/orders/
认证 ：需要Token认证

### 11.创建订单
POST http://localhost:8000/api/orders/orders/
Content-Type: application/json
认证 ：需要Token认证

{
    "payment_method": "ALIPAY",
    "total_amount": 199.99,
    "shipping_address": "测试收货地址"
    
}

### 12.获取订单详情
GET http://localhost:8000/api/orders/orders/2/
认证 ：需要Token认证

### 13.更新订单状态
POST http://localhost:8000/api/orders/orders/2/update_status/
Content-Type: application/json
认证 ：需要Token认证

{
  "status": "PAID"  
}

### 14.获取所有订单（员工/管理员）
GET http://localhost:8000/api/orders/orders/

### 15. 获取订单项
GET http://localhost:8000/api/order-items/order-items/

### 16.获取特定订单项
GET http://localhost:8000/api/order-items/order-items/1/

### 17.创建订单项
POST http://localhost:8000/api/order-items/order-items/
Content-Type: application/json
认证 ：需要Token认证

{
  "order": 4,
  "product": 1,
  "quantity": 2,
  "price": "25.00"
}

🎯 接口权限说明
## 公开接口（无需登录）
用户注册 POST /auth/users/register/

用户登录 POST /auth/users/login/

获取产品 GET /products/products/

## 需要登录的接口
用户登出 POST /auth/users/logout/

创建订单 POST /orders/orders/

获取我的订单 GET /orders/orders/

订单项相关接口

## 管理员/员工接口
用户管理 GET /auth/users/

产品管理 POST/PUT/DELETE /products/products/

所有订单管理 GET /orders/orders/

### 完整使用流程
## 顾客流程：
注册/登录 → 2. 浏览产品 → 3. 创建订单 → 4. 查看我的订单

## 员工流程：
登录 → 2. 管理产品 → 3. 查看所有订单 → 4. 更新订单状态

### 测试信息
## 测试账号
{
  "顾客账号": {"username": "frontend", "password": "test123456", "role": "customer"},
  "员工账号": {"username": "staff", "password": "staff123456", "role": "staff"},
  "管理员账号": {"username": "admin", "password": "admin123456", "role": "admin"}
}
-----------------------------------------------------------------------

我已经测试了KFC后端的主要接口，结果如下：

## 测试通过的接口
### 认证相关接口
- ✅ 用户注册 POST /api/auth/users/register/
- ✅ 用户登录 POST /api/auth/users/login/
- ✅ 用户登出 POST /api/auth/users/logout/
### 产品相关接口
- ✅ 获取所有产品 GET /api/products/products/
- ✅ 按分类筛选产品 GET /api/products/products/?category=DRINK
### 订单相关接口
- ✅ 获取我的订单 GET /api/orders/orders/
- ✅ 创建订单 POST /api/orders/orders/
- ✅ 获取订单详情 GET /api/orders/orders/{id}/
- ✅ 更新订单状态 POST /api/orders/orders/{id}/update_status/
### 订单项相关接口
- ✅ 获取订单项列表 GET /api/order-items/order-items/
- ✅ 创建订单项 POST /api/order-items/order-items/
## 未测试的接口（需要管理员/员工权限）
- 获取用户列表 GET /api/auth/users/
- 创建产品 POST /api/products/products/
- 更新产品 PUT /api/products/products/{id}/
- 删除产品 DELETE /api/products/products/{id}/
- 获取所有订单 GET /api/orders/orders/ （管理员视角）
## 结论
所有测试的接口都工作正常，返回了正确的状态码和数据。注意，获取产品列表接口需要认证，这与API文档中描述的公开接口不一致。其他接口如登录、注册、订单操作等核心功能都运行良好。