# 缓存管理器模块
# 管理窗口和控件对象的缓存，提高自动化执行效率

from typing import Dict, Any, Optional, List
import time

class CacheItem:
    """缓存项类"""
    
    def __init__(self, value: Any, expire_time: float = 10.0):
        """初始化缓存项
        
        Args:
            value: 缓存值
            expire_time: 过期时间（秒）
        """
        self.value = value
        self.expire_time = expire_time
        self.created_time = time.time()
    
    def is_expired(self) -> bool:
        """检查缓存项是否过期
        
        Returns:
            是否过期
        """
        return time.time() - self.created_time > self.expire_time
    
    def get_remaining_time(self) -> float:
        """获取缓存项剩余有效时间
        
        Returns:
            剩余有效时间（秒）
        """
        remaining = self.expire_time - (time.time() - self.created_time)
        return max(0, remaining)

class CacheManager:
    """缓存管理器类"""
    
    def __init__(self, max_size: int = 100, default_expire_time: float = 10.0):
        """初始化缓存管理器
        
        Args:
            max_size: 最大缓存数量
            default_expire_time: 默认过期时间（秒）
        """
        self._cache: Dict[str, CacheItem] = {}
        self.max_size = max_size
        self.default_expire_time = default_expire_time
    
    def set(self, key: str, value: Any, expire_time: Optional[float] = None) -> None:
        """设置缓存
        
        Args:
            key: 缓存键
            value: 缓存值
            expire_time: 过期时间（秒），如果为None则使用默认值
        """
        if expire_time is None:
            expire_time = self.default_expire_time
        
        # 检查缓存大小，超过则删除最旧的缓存项
        if len(self._cache) >= self.max_size:
            self._remove_oldest()
        
        self._cache[key] = CacheItem(value, expire_time)
    
    def get(self, key: str) -> Optional[Any]:
        """获取缓存
        
        Args:
            key: 缓存键
            
        Returns:
            缓存值，如果缓存不存在或已过期则返回None
        """
        if key not in self._cache:
            return None
        
        cache_item = self._cache[key]
        if cache_item.is_expired():
            # 删除过期缓存
            del self._cache[key]
            return None
        
        return cache_item.value
    
    def exists(self, key: str) -> bool:
        """检查缓存是否存在且未过期
        
        Args:
            key: 缓存键
            
        Returns:
            缓存是否存在且未过期
        """
        if key not in self._cache:
            return False
        
        if self._cache[key].is_expired():
            # 删除过期缓存
            del self._cache[key]
            return False
        
        return True
    
    def remove(self, key: str) -> bool:
        """删除缓存
        
        Args:
            key: 缓存键
            
        Returns:
            是否删除成功
        """
        if key in self._cache:
            del self._cache[key]
            return True
        return False
    
    def clear(self) -> None:
        """清空所有缓存"""
        self._cache.clear()
    
    def get_size(self) -> int:
        """获取当前缓存大小
        
        Returns:
            当前缓存大小
        """
        # 先清理过期缓存
        self._clean_expired()
        return len(self._cache)
    
    def get_keys(self) -> List[str]:
        """获取所有缓存键
        
        Returns:
            缓存键列表
        """
        # 先清理过期缓存
        self._clean_expired()
        return list(self._cache.keys())
    
    def _clean_expired(self) -> None:
        """清理过期缓存"""
        expired_keys = [key for key, item in self._cache.items() if item.is_expired()]
        for key in expired_keys:
            del self._cache[key]
    
    def _remove_oldest(self) -> None:
        """删除最旧的缓存项"""
        if not self._cache:
            return
        
        # 清理过期缓存
        self._clean_expired()
        
        if not self._cache:
            return
        
        # 找到最旧的缓存项
        oldest_key = min(self._cache.items(), key=lambda x: x[1].created_time)[0]
        del self._cache[oldest_key]
    
    def update_expire_time(self, key: str, expire_time: float) -> bool:
        """更新缓存过期时间
        
        Args:
            key: 缓存键
            expire_time: 新的过期时间（秒）
            
        Returns:
            是否更新成功
        """
        if key not in self._cache:
            return False
        
        self._cache[key].expire_time = expire_time
        return True

# 创建缓存管理器实例
# 应用缓存：保存应用对象，过期时间30秒
application_cache = CacheManager(max_size=50, default_expire_time=30.0)

# 窗口缓存：保存窗口对象，过期时间20秒
window_cache = CacheManager(max_size=100, default_expire_time=20.0)

# 控件缓存：保存控件对象，过期时间10秒
control_cache = CacheManager(max_size=200, default_expire_time=10.0)

# 定位器缓存：保存定位结果，过期时间5秒
locator_cache = CacheManager(max_size=300, default_expire_time=5.0)
