# 数据库优化指南

本文档总结了KFC Crazy Thursday项目的数据库优化措施和建议。

## 已完成的优化

### 1. 索引优化

为所有常用查询字段添加了索引：

- **Product模型**：为name、price、category、created_time字段添加索引
- **User模型**：为phone、role、created_at字段添加索引，修复了Meta类缩进
- **Order模型**：为order_number、user、total_amount、status、payment_method、created_at、completed_time字段添加索引，修复了状态转换验证逻辑
- **OrderItem模型**：
  - 为order、product、quantity、price字段添加索引
  - 添加复合索引：(order, product) 用于优化按订单和商品的联合查询
  - 添加复合索引：(price, quantity) 用于优化价格区间查询

### 2. SQLite性能优化

在settings.py中配置了SQLite优化参数：

- 启用外键约束（foreign_keys: 1）
- 启用WAL模式（journal_mode: 'wal'），提高并发写入性能
- 增加缓存大小至20MB（cache_size: -20000）
- 设置同步模式为NORMAL，平衡性能和安全性

### 3. 数据库连接和事务优化

- 启用ATOMIC_REQUESTS，使每个视图函数在事务中执行
- 添加数据库查询超时设置
- 创建了数据库连接池配置模块（database_pool.py），为将来迁移到MySQL/PostgreSQL做准备

### 4. 缓存优化

- 配置了本地内存缓存，设置最大条目10000，超时时间300秒
- 添加了API限流保护，防止数据库过载

## 未来优化建议

### 1. 数据库迁移

- **迁移到生产级数据库**：从SQLite迁移到MySQL或PostgreSQL
  - MySQL配置示例：
    ```python
    DATABASES = {
        'default': {
            'ENGINE': 'dj_db_conn_pool.backends.mysql',
            'NAME': 'kfc_crazy',
            'USER': 'root',
            'PASSWORD': 'password',
            'HOST': '127.0.0.1',
            'PORT': '3306',
            'OPTIONS': {
                'charset': 'utf8mb4',
                'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            },
            'POOL_OPTIONS': {
                'pool_size': 10,
                'max_overflow': 20,
                'timeout': 30,
                'recycle': 3600,
            }
        }
    }
    ```

### 2. 高级缓存策略

- **使用Redis缓存**：替换本地内存缓存，提高缓存性能和可靠性
  - 安装依赖：`pip install django-redis`
  - 配置Redis缓存

### 3. 查询优化

- 在视图中使用select_related()和prefetch_related()减少数据库查询
- 避免N+1查询问题
- 使用values()和only()减少数据传输量

### 4. 数据库分区和分表

- 对于订单历史数据，考虑按时间分区
- 对于大量数据的表，考虑水平分表策略

### 5. 数据库备份和恢复

- 配置定期数据库备份策略
- 测试数据库恢复流程

### 6. 监控和调优

- 安装数据库监控工具
- 定期分析慢查询日志
- 根据实际负载调整索引和缓存策略

## 性能验证

优化完成后，建议进行以下测试：

1. 使用Django Debug Toolbar监控查询性能
2. 执行高并发测试，验证WAL模式和索引的效果
3. 监控内存使用情况，确保缓存设置合理

## 注意事项

- 每次添加新索引前，先分析查询模式，避免创建不必要的索引
- 索引会增加写入操作的开销，需要平衡读写性能
- 定期更新数据库统计信息，确保查询优化器正常工作

---

通过以上优化措施，系统的数据库性能应该会有显著提升，特别是在高频查询场景下。