"""
数据库连接池配置
使用django-db-connection-pool优化数据库连接性能
"""
from django.conf import settings
from django.db.backends.base.base import BaseDatabaseWrapper
from django.db.backends.mysql.base import DatabaseWrapper
from django.db.backends.postgresql.base import DatabaseWrapper as PostgresDatabaseWrapper

# 如果使用mysql
class PooledMySQLDatabaseWrapper(DatabaseWrapper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 配置连接池参数
        self.pool_options = {
            'pool_size': 10,  # 连接池大小
            'max_overflow': 20,  # 最大溢出连接数
            'timeout': 30,  # 连接超时时间（秒）
            'recycle': 3600,  # 连接回收时间（秒）
        }

# 如果使用postgresql
class PooledPostgresDatabaseWrapper(PostgresDatabaseWrapper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 配置连接池参数
        self.pool_options = {
            'pool_size': 10,
            'max_overflow': 20,
            'timeout': 30,
            'recycle': 3600,
        }