# KFC后端API文档

## 1. 基础信息

- **基础URL**: `http://localhost:8000/api/`
- **认证方式**: Token认证（登录后返回Token）
- **请求格式**: JSON
- **响应格式**: JSON

### 认证方式
需要在Header中添加以下认证信息：
```
Authorization: Token {token}
```

### 数据格式规范
1. **支付方式**: 必须使用大写字母
   - ALIPAY (支付宝)
   - WECHAT (微信支付)
   - CARD (银行卡)

2. **订单状态**: 必须使用大写字母
   - PENDING (待支付)
   - PAID (已支付)
   - COMPLETED (已完成)

## 2. 接口详情

### 2.1 用户相关接口

#### 2.1.1 用户注册
**URL**: `/auth/users/register/`
**方法**: `POST`
**认证**: 无需认证
**描述**: 创建新用户账号

**请求参数**:
| 字段名 | 类型 | 必填 | 描述 | 示例 |
|--------|------|------|------|------|
| username | string | 是 | 用户名，唯一 | `testuser123` |
| password | string | 是 | 密码，至少6位 | `Test123456` |
| email | string | 否 | 电子邮箱 | `test@example.com` |
| phone | string | 是 | 手机号码 | `13812345678` |
| role | string | 否 | 用户角色，默认customer | `customer`/`staff`/`admin` |

**请求示例**:
```json
{
  "username": "testuser123",
  "password": "Test123456",
  "email": "test123@example.com",
  "phone": "13812345678",
  "role": "customer"
}
```

**成功响应**:
- **状态码**: `201 Created`
```json
{
  "id": 1,
  "username": "testuser123",
  "email": "test123@example.com",
  "phone": "13812345678",
  "role": "customer",
  "created_at": "2024-01-01T12:00:00Z"
}
```

**失败响应**:
- **状态码**: `400 Bad Request` (参数错误)
```json
{
  "username": ["该用户名已存在"],
  "phone": ["请输入有效的手机号码"]
}
```

#### 2.1.2 用户登录
**URL**: `/auth/users/login/`
**方法**: `POST`
**认证**: 无需认证
**描述**: 用户登录并获取认证Token

**请求参数**:
| 字段名 | 类型 | 必填 | 描述 | 示例 |
|--------|------|------|------|------|
| username | string | 是 | 用户名 | `frontend` |
| password | string | 是 | 密码 | `test123456` |

**请求示例**:
```json
{
  "username": "frontend",
  "password": "test123456"
}
```

**成功响应**:
- **状态码**: `200 OK`
```json
{
  "token": "39e0ca0b459a58f90e5e883b7b3f22f7d954e6f1",
  "user": {
    "id": 1,
    "username": "frontend",
    "role": "customer"
  }
}
```

**失败响应**:
- **状态码**: `401 Unauthorized` (认证失败)
```json
{
  "detail": "用户名或密码错误"
}
```

#### 2.1.3 用户登出
**URL**: `/auth/users/logout/`
**方法**: `POST`
**认证**: 需要Token认证
**描述**: 用户登出并使Token失效

**请求示例**:
```
POST /auth/users/logout/
Authorization: Token 39e0ca0b459a58f90e5e883b7b3f22f7d954e6f1
```

**成功响应**:
- **状态码**: `200 OK`
```json
{
  "message": "登出成功"
}
```

**失败响应**:
- **状态码**: `401 Unauthorized` (Token无效或已过期)
```json
{
  "detail": "Token已过期或无效"
}
```

#### 2.1.4 获取用户列表（管理员）
**URL**: `/auth/users/`
**方法**: `GET`
**认证**: 需要Token认证，仅管理员和员工可访问
**描述**: 获取系统中所有用户列表

**请求示例**:
```
GET /auth/users/
Authorization: Token 39e0ca0b459a58f90e5e883b7b3f22f7d954e6f1
```

**成功响应**:
- **状态码**: `200 OK`
```json
{
  "count": 5,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "username": "admin",
      "email": "admin@example.com",
      "phone": "13800138000",
      "role": "admin",
      "created_at": "2024-01-01T00:00:00Z"
    },
    {
      "id": 2,
      "username": "frontend",
      "email": "frontend@example.com",
      "phone": "13800138001",
      "role": "customer",
      "created_at": "2024-01-01T00:00:00Z"
    }
  ]
}
```

**失败响应**:
- **状态码**: `403 Forbidden` (权限不足)
```json
{
  "detail": "您没有权限执行此操作"
}
```

### 2.2 产品相关接口

#### 2.2.1 获取所有产品
**URL**: `/products/products/`
**方法**: `GET`
**认证**: 无需认证
**描述**: 获取系统中所有可用产品列表

**查询参数**:
| 字段名 | 类型 | 必填 | 描述 | 示例 |
|--------|------|------|------|------|
| page | integer | 否 | 页码，默认1 | `1` |
| page_size | integer | 否 | 每页数量，默认10 | `20` |

**请求示例**:
```
GET /products/products/
```

**成功响应**:
- **状态码**: `200 OK`
```json
{
  "count": 20,
  "next": "http://localhost:8000/api/products/products/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "香辣鸡腿堡",
      "description": "经典香辣口味，配以新鲜生菜和特制酱料",
      "price": "26.00",
      "category": "burger",
      "is_available": true,
      "created_at": "2024-01-01T00:00:00Z"
    },
    {
      "id": 2,
      "name": "新奥尔良烤鸡腿堡",
      "description": "新奥尔良风味烤制，鲜嫩多汁",
      "price": "28.00",
      "category": "burger",
      "is_available": true,
      "created_at": "2024-01-01T00:00:00Z"
    }
  ]
}
```

#### 2.2.2 按分类筛选产品
**URL**: `/products/products/`
**方法**: `GET`
**认证**: 无需认证
**描述**: 根据分类筛选产品

**查询参数**:
| 字段名 | 类型 | 必填 | 描述 | 示例 |
|--------|------|------|------|------|
| category | string | 是 | 产品分类 | `burger`/`food`/`drink` |
| page | integer | 否 | 页码，默认1 | `1` |
| page_size | integer | 否 | 每页数量，默认10 | `20` |

**请求示例**:
```
GET /products/products/?category=burger
```

**成功响应**:
- **状态码**: `200 OK`
```json
{
  "count": 5,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "香辣鸡腿堡",
      "description": "经典香辣口味",
      "price": "26.00",
      "category": "burger",
      "is_available": true
    }
  ]
}
```

#### 2.2.3 创建产品（员工/管理员）
**URL**: `/products/products/`
**方法**: `POST`
**认证**: 需要Token认证，仅管理员和员工可访问
**描述**: 创建新的产品

**请求参数**:
| 字段名 | 类型 | 必填 | 描述 | 示例 |
|--------|------|------|------|------|
| name | string | 是 | 产品名称 | `香辣鸡腿堡` |
| description | string | 否 | 产品描述 | `经典香辣口味` |
| price | string | 是 | 产品价格（保留两位小数） | `26.00` |
| category | string | 是 | 产品分类 | `burger`/`food`/`drink` |
| is_available | boolean | 否 | 是否可用，默认true | `true` |

**请求示例**:
```json
{
  "name": "新奥尔良烤鸡腿堡",
  "description": "美味的新奥尔良风味",
  "price": "28.00",
  "category": "burger",
  "is_available": true
}
```

**成功响应**:
- **状态码**: `201 Created`
```json
{
  "id": 5,
  "name": "新奥尔良烤鸡腿堡",
  "description": "美味的新奥尔良风味",
  "price": "28.00",
  "category": "burger",
  "is_available": true,
  "created_at": "2024-01-01T12:00:00Z"
}
```

**失败响应**:
- **状态码**: `400 Bad Request` (参数错误)
```json
{
  "price": ["价格格式错误，请使用两位小数"]
}
```
- **状态码**: `403 Forbidden` (权限不足)
```json
{
  "detail": "您没有权限执行此操作"
}
```

#### 2.2.4 更新产品（员工/管理员）
**URL**: `/products/products/{id}/`
**方法**: `PUT`
**认证**: 需要Token认证，仅管理员和员工可访问
**描述**: 更新指定产品信息

**路径参数**:
| 字段名 | 类型 | 必填 | 描述 | 示例 |
|--------|------|------|------|------|
| id | integer | 是 | 产品ID | `1` |

**请求参数**:
| 字段名 | 类型 | 必填 | 描述 | 示例 |
|--------|------|------|------|------|
| name | string | 否 | 产品名称 | `香辣鸡腿堡` |
| description | string | 否 | 产品描述 | `经典香辣口味` |
| price | string | 否 | 产品价格 | `26.00` |
| category | string | 否 | 产品分类 | `burger` |
| is_available | boolean | 否 | 是否可用 | `true` |

**请求示例**:
```json
{
  "name": "香辣鸡腿堡",
  "price": "26.00",
  "is_available": true
}
```

**成功响应**:
- **状态码**: `200 OK`
```json
{
  "id": 1,
  "name": "香辣鸡腿堡",
  "description": "经典香辣口味",
  "price": "26.00",
  "category": "burger",
  "is_available": true,
  "updated_at": "2024-01-01T12:30:00Z"
}
```

**失败响应**:
- **状态码**: `404 Not Found` (产品不存在)
```json
{
  "detail": "产品不存在"
}
```

#### 2.2.5 删除产品（员工/管理员）
**URL**: `/products/products/{id}/`
**方法**: `DELETE`
**认证**: 需要Token认证，仅管理员和员工可访问
**描述**: 删除指定产品

**路径参数**:
| 字段名 | 类型 | 必填 | 描述 | 示例 |
|--------|------|------|------|------|
| id | integer | 是 | 产品ID | `1` |

**请求示例**:
```
DELETE /products/products/1/
Authorization: Token 39e0ca0b459a58f90e5e883b7b3f22f7d954e6f1
```

**成功响应**:
- **状态码**: `204 No Content`

**失败响应**:
- **状态码**: `404 Not Found` (产品不存在)
```json
{
  "detail": "产品不存在"
}
```

### 2.3 订单相关接口

#### 2.3.1 获取我的订单
**URL**: `/orders/orders/`
**方法**: `GET`
**认证**: 需要Token认证
**描述**: 获取当前用户的订单列表

**查询参数**:
| 字段名 | 类型 | 必填 | 描述 | 示例 |
|--------|------|------|------|------|
| page | integer | 否 | 页码，默认1 | `1` |
| page_size | integer | 否 | 每页数量，默认10 | `20` |
| status | string | 否 | 订单状态筛选 | `PAID` |

**请求示例**:
```
GET /orders/orders/
Authorization: Token 39e0ca0b459a58f90e5e883b7b3f22f7d954e6f1
```

**成功响应**:
- **状态码**: `200 OK`
```json
{
  "count": 3,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "order_number": "ORD202401010001",
      "user": {
        "id": 1,
        "username": "frontend"
      },
      "status": "PAID",
      "payment_method": "ALIPAY",
      "total_amount": "199.99",
      "shipping_address": "测试地址",
      "created_at": "2024-01-01T10:00:00Z",
      "updated_at": "2024-01-01T10:05:00Z"
    }
  ]
}
```

#### 2.3.2 创建订单
**URL**: `/orders/orders/`
**方法**: `POST`
**认证**: 需要Token认证
**描述**: 创建新订单

**请求参数**:
| 字段名 | 类型 | 必填 | 描述 | 示例 |
|--------|------|------|------|------|
| payment_method | string | 是 | 支付方式（大写） | `ALIPAY`/`WECHAT`/`CARD` |
| total_amount | string | 是 | 订单总金额（保留两位小数） | `199.99` |
| shipping_address | string | 是 | 收货地址 | `北京市朝阳区XX街道` |

**请求示例**:
```json
{
  "payment_method": "ALIPAY",
  "total_amount": "199.99",
  "shipping_address": "测试收货地址"
}
```

**成功响应**:
- **状态码**: `201 Created`
```json
{
  "id": 2,
  "order_number": "ORD202401010002",
  "user": {
    "id": 1,
    "username": "frontend"
  },
  "status": "PENDING",
  "payment_method": "ALIPAY",
  "total_amount": "199.99",
  "shipping_address": "测试收货地址",
  "created_at": "2024-01-01T11:00:00Z",
  "updated_at": "2024-01-01T11:00:00Z"
}
```

**失败响应**:
- **状态码**: `400 Bad Request` (参数错误)
```json
{
  "payment_method": ["支付方式必须是ALIPAY、WECHAT或CARD"]
}
```

#### 2.3.3 获取订单详情
**URL**: `/orders/orders/{id}/`
**方法**: `GET`
**认证**: 需要Token认证
**描述**: 获取指定订单的详细信息

**路径参数**:
| 字段名 | 类型 | 必填 | 描述 | 示例 |
|--------|------|------|------|------|
| id | integer | 是 | 订单ID | `2` |

**请求示例**:
```
GET /orders/orders/2/
Authorization: Token 39e0ca0b459a58f90e5e883b7b3f22f7d954e6f1
```

**成功响应**:
- **状态码**: `200 OK`
```json
{
  "id": 2,
  "order_number": "ORD202401010002",
  "user": {
    "id": 1,
    "username": "frontend"
  },
  "status": "PENDING",
  "payment_method": "ALIPAY",
  "total_amount": "199.99",
  "shipping_address": "测试收货地址",
  "order_items": [
    {
      "id": 1,
      "product": {
        "id": 1,
        "name": "香辣鸡腿堡"
      },
      "quantity": 2,
      "price": "26.00"
    }
  ],
  "created_at": "2024-01-01T11:00:00Z",
  "updated_at": "2024-01-01T11:00:00Z"
}
```

**失败响应**:
- **状态码**: `404 Not Found` (订单不存在)
```json
{
  "detail": "订单不存在"
}
```
- **状态码**: `403 Forbidden` (无权访问其他用户的订单)
```json
{
  "detail": "您无权访问此订单"
}
```

#### 2.3.4 更新订单状态
**URL**: `/orders/orders/{id}/update_status/`
**方法**: `POST`
**认证**: 需要Token认证
**描述**: 更新指定订单的状态

**路径参数**:
| 字段名 | 类型 | 必填 | 描述 | 示例 |
|--------|------|------|------|------|
| id | integer | 是 | 订单ID | `2` |

**请求参数**:
| 字段名 | 类型 | 必填 | 描述 | 示例 |
|--------|------|------|------|------|
| status | string | 是 | 订单状态（大写） | `PAID`/`COMPLETED` |

**请求示例**:
```json
{
  "status": "PAID"
}
```

**成功响应**:
- **状态码**: `200 OK`
```json
{
  "id": 2,
  "order_number": "ORD202401010002",
  "status": "PAID",
  "updated_at": "2024-01-01T11:30:00Z"
}
```

**失败响应**:
- **状态码**: `400 Bad Request` (参数错误)
```json
{
  "status": ["订单状态必须是PAID或COMPLETED"]
}
```
- **状态码**: `403 Forbidden` (无权限更新)
```json
{
  "detail": "您没有权限更新此订单状态"
}
```

### 2.4 订单项相关接口

#### 2.4.1 获取订单项
**URL**: `/order-items/order-items/`
**方法**: `GET`
**认证**: 需要Token认证
**描述**: 获取当前用户的所有订单项

**查询参数**:
| 字段名 | 类型 | 必填 | 描述 | 示例 |
|--------|------|------|------|------|
| page | integer | 否 | 页码，默认1 | `1` |
| page_size | integer | 否 | 每页数量，默认10 | `20` |
| order_id | integer | 否 | 按订单ID筛选 | `1` |

**请求示例**:
```
GET /order-items/order-items/
Authorization: Token 39e0ca0b459a58f90e5e883b7b3f22f7d954e6f1
```

**成功响应**:
- **状态码**: `200 OK`
```json
{
  "count": 5,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "order": {
        "id": 1,
        "order_number": "ORD202401010001"
      },
      "product": {
        "id": 1,
        "name": "香辣鸡腿堡",
        "price": "26.00"
      },
      "quantity": 2,
      "price": "26.00",
      "created_at": "2024-01-01T10:00:00Z"
    }
  ]
}
```

#### 2.4.2 获取特定订单项
**URL**: `/order-items/order-items/{id}/`
**方法**: `GET`
**认证**: 需要Token认证
**描述**: 获取指定的订单项详情

**路径参数**:
| 字段名 | 类型 | 必填 | 描述 | 示例 |
|--------|------|------|------|------|
| id | integer | 是 | 订单项ID | `1` |

**请求示例**:
```
GET /order-items/order-items/1/
Authorization: Token 39e0ca0b459a58f90e5e883b7b3f22f7d954e6f1
```

**成功响应**:
- **状态码**: `200 OK`
```json
{
  "id": 1,
  "order": {
    "id": 1,
    "order_number": "ORD202401010001",
    "user": {
      "id": 1,
      "username": "frontend"
    }
  },
  "product": {
    "id": 1,
    "name": "香辣鸡腿堡",
    "description": "经典香辣口味",
    "price": "26.00",
    "category": "burger"
  },
  "quantity": 2,
  "price": "26.00",
  "created_at": "2024-01-01T10:00:00Z"
}
```

**失败响应**:
- **状态码**: `404 Not Found` (订单项不存在)
```json
{
  "detail": "订单项不存在"
}
```
- **状态码**: `403 Forbidden` (无权访问)
```json
{
  "detail": "您无权访问此订单项"
}
```

#### 2.4.3 创建订单项
**URL**: `/order-items/order-items/`
**方法**: `POST`
**认证**: 需要Token认证
**描述**: 为订单添加订单项

**请求参数**:
| 字段名 | 类型 | 必填 | 描述 | 示例 |
|--------|------|------|------|------|
| order | integer | 是 | 订单ID | `4` |
| product | integer | 是 | 产品ID | `1` |
| quantity | integer | 是 | 数量，大于0 | `2` |
| price | string | 是 | 单价（保留两位小数） | `25.00` |

**请求示例**:
```json
{
  "order": 4,
  "product": 1,
  "quantity": 2,
  "price": "25.00"
}
```

**成功响应**:
- **状态码**: `201 Created`
```json
{
  "id": 5,
  "order": {
    "id": 4,
    "order_number": "ORD202401010004"
  },
  "product": {
    "id": 1,
    "name": "香辣鸡腿堡"
  },
  "quantity": 2,
  "price": "25.00",
  "created_at": "2024-01-01T12:00:00Z"
}
```

**失败响应**:
- **状态码**: `400 Bad Request` (参数错误)
```json
{
  "quantity": ["数量必须大于0"]
}
```
- **状态码**: `404 Not Found` (订单或产品不存在)
```json
{
  "detail": "订单不存在"
}
```

## 3. 常见错误码说明

| 状态码 | 描述 | 常见原因 |
|--------|------|----------|
| 400 | 错误请求 | 请求参数格式错误或缺失必选字段 |
| 401 | 未授权 | Token缺失、无效或已过期 |
| 403 | 禁止访问 | 用户权限不足，无法执行操作 |
| 404 | 未找到 | 请求的资源（如订单、产品）不存在 |
| 405 | 方法不允许 | 使用了不支持的HTTP方法 |
| 500 | 服务器错误 | 服务器内部错误，请联系管理员 |

## 4. 使用流程示例

### 4.1 顾客购物流程
1. **浏览产品** (GET `/products/products/`)
2. **注册账号** (POST `/auth/users/register/`)
3. **登录获取Token** (POST `/auth/users/login/`)
4. **创建订单** (POST `/orders/orders/`)
5. **添加订单项** (POST `/order-items/order-items/`)
6. **查看订单详情** (GET `/orders/orders/{id}/`)

### 4.2 员工管理流程
1. **登录获取Token** (POST `/auth/users/login/`)
2. **管理产品** (POST/PUT/DELETE `/products/products/`)
3. **查看所有订单** (GET `/orders/orders/`)
4. **更新订单状态** (POST `/orders/orders/{id}/update_status/`)

## 5. 测试账号

```json
{
  "顾客账号": {
    "username": "frontend",
    "password": "test123456",
    "role": "customer"
  },
  "员工账号": {
    "username": "staff",
    "password": "staff123456",
    "role": "staff"
  },
  "管理员账号": {
    "username": "admin",
    "password": "admin123456",
    "role": "admin"
  }
}
```

## 6. 注意事项

1. 所有需要认证的接口都必须在Header中携带有效的Token
2. 支付方式和订单状态必须使用大写字母
3. 价格相关字段应使用字符串格式，并保留两位小数
4. 用户只能访问自己的订单和订单项数据
5. 敏感操作（如创建/更新产品、查看所有用户）需要管理员或员工权限
6. 接口返回的时间戳格式为ISO 8601格式（如：2024-01-01T12:00:00Z）