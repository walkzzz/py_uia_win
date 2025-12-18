# 控件缓存模块
# 缓存控件查找结果，减少重复查找开销

from typing import Any, Dict, Optional
from datetime import datetime, timedelta

class CacheItem:
    """缓存项，包含缓存值和过期时间"""
    
    def __init__(self, value: Any, expire_time: Optional[float] = None):
        """初始化缓存项
        
        Args:
            value: 缓存值
            expire_time: 过期时间（秒），如果为None则永不过期
        """
        self.value = value
        self.expire_time = datetime.now() + timedelta(seconds=expire_time) if expire_time is not None else None
    
    @property
    def is_expired(self) -> bool:
        """检查缓存项是否过期
        
        Returns:
            是否过期
        """
        if self.expire_time is None:
            return False
        return datetime.now() > self.expire_time

class ControlCache:
    """控件缓存，缓存控件查找结果"""
    
    def __init__(self, max_size: int = 100, default_expire_time: float = 30.0):
        """初始化控件缓存
        
        Args:
            max_size: 最大缓存大小
            default_expire_time: 默认过期时间（秒）
        """
        self._cache: Dict[str, CacheItem] = {}
        self._max_size = max_size
        self._default_expire_time = default_expire_time
    
    def get(self, key: str) -> Optional[Any]:
        """获取缓存值
        
        Args:
            key: 缓存键
        
        Returns:
            缓存值，如果不存在或已过期则返回None
        """
        if key in self._cache:
            item = self._cache[key]
            if not item.is_expired:
                return item.value
            # 移除过期项
            del self._cache[key]
        return None
    
    def set(self, key: str, value: Any, expire_time: Optional[float] = None) -> None:
        """设置缓存值
        
        Args:
            key: 缓存键
            value: 缓存值
            expire_time: 过期时间（秒），如果为None则使用默认值
        """
        if expire_time is None:
            expire_time = self._default_expire_time
        
        # 检查缓存大小
        if len(self._cache) >= self._max_size:
            # 移除最早的过期项或最旧的项
            self._cleanup_expired()
            if len(self._cache) >= self._max_size:
                # 仍然超过大小限制，移除最旧的项
                oldest_key = next(iter(self._cache))
                del self._cache[oldest_key]
        
        self._cache[key] = CacheItem(value, expire_time)
    
    def remove(self, key: str) -> None:
        """移除缓存项
        
        Args:
            key: 缓存键
        """
        if key in self._cache:
            del self._cache[key]
    
    def clear(self) -> None:
        """清空缓存"""
        self._cache.clear()
    
    def _cleanup_expired(self) -> None:
        """清理过期的缓存项"""
        expired_keys = []
        for key, item in self._cache.items():
            if item.is_expired:
                expired_keys.append(key)
        
        for key in expired_keys:
            del self._cache[key]
    
    def __contains__(self, key: str) -> bool:
        """检查键是否在缓存中且未过期
        
        Args:
            key: 缓存键
        
        Returns:
            是否存在且未过期
        """
        return self.get(key) is not None

# 创建全局缓存实例
control_cache = ControlCache()
