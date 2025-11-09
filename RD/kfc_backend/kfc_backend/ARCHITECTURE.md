# KFC Crazy Thursday 项目架构文档

## 项目概述

KFC Crazy Thursday 是一个基于前后端分离架构的在线点餐系统，提供商品浏览、购物车管理、订单创建等功能。

## 技术栈

### 前端技术
- **框架**: Vue 3 + Composition API
- **构建工具**: Vite
- **UI组件库**: Element Plus
- **状态管理**: Pinia
- **路由**: Vue Router
- **HTTP请求**: Axios

### 后端技术
- **框架**: Django 5.2.7
- **API框架**: Django REST Framework 3.16.1
- **数据库**: SQLite（默认）
- **认证**: Token认证 + Session认证
- **跨域处理**: django-cors-headers

## 项目结构

### 前端项目结构

```
FE/kfc_frontend/
├── src/
│   ├── components/      # 公共组件
│   │   ├── HelloWorld.vue
│   │   └── Navbar.vue
│   ├── views/          # 页面视图
│   │   ├── customer/   # 顾客相关页面
│   │   └── staff/      # 员工相关页面
│   ├── utils/          # 工具函数
│   │   ├── auth.js     # 认证相关
│   │   └── request.js  # Axios请求封装
│   ├── store/          # Pinia状态管理
│   │   └── cartstore.js # 购物车状态
│   ├── router/         # 路由配置
│   │   └── index.js
│   ├── App.vue         # 根组件
│   └── main.js         # 入口文件
├── public/             # 静态资源
├── index.html          # HTML模板
├── package.json        # 项目依赖
└── vite.config.js      # Vite配置
```

### 后端项目结构

```
RD/kfc_backend/
├── kfc_backend/       # 项目配置
│   ├── settings.py    # Django设置
│   ├── urls.py        # 主路由配置
│   └── wsgi.py        # WSGI配置
├── product/           # 产品模块
│   ├── models.py      # 产品模型
│   ├── views.py       # 产品视图
│   ├── serializers.py # 产品序列化器
│   └── urls.py        # 产品路由
├── order/             # 订单模块
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   └── urls.py
├── orderitem/         # 订单项模块
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   └── urls.py
├── user/              # 用户模块
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   ├── urls.py
│   └── permissions.py # 权限类
├── manage.py          # Django管理脚本
└── requirements.txt   # Python依赖
```

## 核心功能模块

### 1. 用户模块
- 用户注册、登录、登出
- 用户角色管理（顾客、员工、管理员）
- Token认证机制

### 2. 产品模块
- 产品分类管理（汉堡、小食、饮料、套餐）
- 产品列表展示与筛选
- 产品CRUD操作（员工/管理员）

### 3. 订单模块
- 创建订单
- 订单状态管理
- 订单列表查询

### 4. 订单项模块
- 购物车功能
- 订单项管理

## 数据流设计

### 前端数据流
1. **用户交互** → 组件状态更新 → Pinia Store更新
2. **API请求** → Axios拦截器 → 响应处理 → 组件更新
3. **路由跳转** → 权限验证 → 组件加载

### 后端数据流
1. **HTTP请求** → URL路由 → View处理
2. **权限验证** → 业务逻辑 → 数据库操作
3. **数据序列化** → HTTP响应

## 认证与权限

### 认证机制
- **Token认证**: 使用DRF的Token认证，在请求头添加`Authorization: Token {token}`
- **Session认证**: 登录后自动保存cookie

### 权限层级
- **公开接口**: 产品列表、用户注册、用户登录
- **需登录接口**: 购物车操作、订单创建、个人订单查询
- **员工/管理员接口**: 产品管理、用户管理、所有订单管理

## 部署说明

### 开发环境
1. **后端启动**:
   ```bash
   cd RD/kfc_backend
   pip install -r requirements.txt
   python manage.py runserver
   ```

2. **前端启动**:
   ```bash
   cd FE/kfc_frontend
   npm install
   npm run dev
   ```

### 生产环境（建议）
- **后端**: 使用Gunicorn/uWSGI + Nginx
- **前端**: 构建静态文件并部署到Nginx
- **数据库**: 迁移到PostgreSQL/MySQL
- **缓存**: 使用Redis提高性能

## 性能优化建议

1. **数据库索引**: 为常用查询字段添加索引
2. **API缓存**: 对产品列表等高频访问接口添加缓存
3. **图片优化**: 产品图片使用CDN加速
4. **前端懒加载**: 路由和组件懒加载
5. **请求节流**: 对搜索等操作添加节流处理

## 安全考虑

1. **输入验证**: 前后端双重验证
2. **CSRF保护**: 启用Django的CSRF保护
3. **XSS防护**: 使用Vue的模板自动转义
4. **密码加密**: 使用Django的密码哈希机制
5. **权限控制**: 严格的基于角色的访问控制

## 扩展规划

1. **支付集成**: 接入支付宝、微信支付
2. **实时通知**: WebSocket实现订单状态更新
3. **数据分析**: 销售统计和用户行为分析
4. **多语言支持**: 国际化功能
5. **移动端适配**: 响应式设计优化