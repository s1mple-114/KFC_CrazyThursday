# KFC Crazy Thursday 部署与使用指南

## 环境要求

### 后端环境
- Python 3.8+
- pip 20.0+
- 数据库: SQLite（默认）/ PostgreSQL/MySQL（可选）

### 前端环境
- Node.js 16+
- npm 8+

## 后端部署步骤

### 1. 安装依赖

```bash
# 进入后端目录
cd d:\KFC_CrazyThursday\KFC_CrazyThursday\RD\kfc_backend

# 安装Python依赖
pip install -r requirements.txt
```

### 2. 数据库配置

Django默认使用SQLite数据库，无需额外配置。如需使用其他数据库，请修改`kfc_backend/settings.py`中的数据库配置：

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',  # 或 'django.db.backends.mysql'
        'NAME': 'kfc_db',
        'USER': 'db_user',
        'PASSWORD': 'db_password',
        'HOST': 'localhost',
        'PORT': '5432',  # MySQL默认3306
    }
}
```

### 3. 数据库迁移

```bash
# 执行数据库迁移
python manage.py migrate

# 创建超级用户（可选，用于管理后台）
python manage.py createsuperuser
```

### 4. 配置CORS

CORS配置已在`settings.py`中设置，默认允许所有来源：

```python
CORS_ALLOW_ALL_ORIGINS = True
```

如需限制特定来源，请修改为：

```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",  # Vue开发服务器
    "http://127.0.0.1:5173",
    # 生产环境域名
]
```

### 5. 启动后端服务

```bash
# 开发模式启动
python manage.py runserver

# 或指定端口
python manage.py runserver 8000
```

服务将在 http://127.0.0.1:8000/ 上运行

## 前端部署步骤

### 1. 安装依赖

```bash
# 进入前端目录
cd d:\KFC_CrazyThursday\KFC_CrazyThursday\FE\kfc_frontend

# 安装npm依赖
npm install
```

### 2. API地址配置

前端API地址配置在`src/utils/request.js`中：

```javascript
const request = axios.create({
  baseURL: '/api', // 后端基础地址
  timeout: 30000
})
```

### 3. 开发模式启动

```bash
# 启动开发服务器
npm run dev
```

服务将在 http://localhost:5173/ 上运行（端口可能不同，请查看终端输出）

### 4. 生产环境构建

```bash
# 构建生产版本
npm run build

# 预览生产构建
npm run preview
```

构建后的静态文件将位于`dist`目录

## Nginx配置（生产环境）

### 前端配置

```nginx
server {
    listen 80;
    server_name your_domain.com;
    
    location / {
        root /path/to/FE/kfc_frontend/dist;
        index index.html;
        try_files $uri $uri/ /index.html;
    }
    
    # 代理API请求到后端
    location /api/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## API使用指南

### 认证方式

**Token认证**：
- 登录成功后获取token
- 请求头添加：`Authorization: Token your_token_here`

### 测试账号

```
顾客账号: 
  用户名: frontend
  密码: test123456
  角色: customer

员工账号:
  用户名: staff
  密码: staff123456
  角色: staff

管理员账号:
  用户名: admin
  密码: admin123456
  角色: admin
```

### 主要API端点

**产品相关**：
- GET `/api/products/products/` - 获取产品列表
- GET `/api/products/products/?category=BURGER` - 按分类筛选产品

**订单相关**：
- GET `/api/orders/orders/` - 获取订单列表
- POST `/api/orders/orders/` - 创建新订单

**用户相关**：
- POST `/api/auth/users/register/` - 用户注册
- POST `/api/auth/users/login/` - 用户登录

详细API文档请查看 [API_README.md](API_README.md)

## 常见问题排查

### 1. 跨域问题
- 确保后端CORS配置正确
- 检查`CORS_ALLOWED_ORIGINS`设置

### 2. 数据库连接失败
- 检查数据库服务是否运行
- 验证数据库配置和凭据
- 确保已执行数据库迁移

### 3. API请求401错误
- 检查token是否正确
- 确保token未过期
- 验证请求头格式

### 4. 前端无法连接后端
- 确认后端服务正在运行
- 检查防火墙设置
- 验证API路径配置

### 5. 静态文件加载失败
- 检查`STATIC_URL`和`STATIC_ROOT`配置
- 执行`python manage.py collectstatic`

## 开发注意事项

1. **代码规范**：
   - 遵循PEP 8规范（Python）
   - 遵循Vue.js官方风格指南

2. **环境变量**：
   - 敏感信息（如数据库密码）应使用环境变量
   - 生产环境禁止硬编码配置

3. **安全措施**：
   - 始终验证用户输入
   - 实施适当的权限控制
   - 避免SQL注入和XSS攻击

4. **调试技巧**：
   - 使用Django的调试工具条
   - 前端使用Vue DevTools
   - 检查浏览器控制台和Django日志

## 更新日志

### v1.0.0
- 初始版本发布
- 完成所有基础功能
- API文档编写

### v1.1.0
- 修复产品接口权限
- 完善错误处理
- 增强安全性