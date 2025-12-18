# 局部配置模块
# 用于管理测试用例级别的配置，允许覆盖全局配置

from typing import Dict, Any, Optional
from .global_config import global_config

class LocalConfig:
    """局部配置类"""
    
    def __init__(self):
        # 存储局部配置，键为配置名，值为配置值
        self._config: Dict[str, Any] = {}
        # 存储当前应用上下文的配置
        self._context_config: Dict[str, Dict[str, Any]] = {}
    
    def get(self, key: str, default: Any = None) -> Any:
        """获取配置值
        
        优先级：局部配置 > 全局配置 > 默认值
        
        Args:
            key: 配置名
            default: 默认值
        
        Returns:
            配置值
        """
        if key in self._config:
            return self._config[key]
        return getattr(global_config, key, default)
    
    def set(self, key: str, value: Any) -> None:
        """设置局部配置
        
        Args:
            key: 配置名
            value: 配置值
        """
        if hasattr(global_config, key):
            self._config[key] = value
        else:
            raise ValueError(f"未知的配置项: {key}")
    
    def get_context_config(self, context_id: str, key: str, default: Any = None) -> Any:
        """获取指定上下文的配置
        
        Args:
            context_id: 上下文ID（如应用ID、窗口ID）
            key: 配置名
            default: 默认值
        
        Returns:
            配置值
        """
        if context_id in self._context_config and key in self._context_config[context_id]:
            return self._context_config[context_id][key]
        return self.get(key, default)
    
    def set_context_config(self, context_id: str, key: str, value: Any) -> None:
        """设置指定上下文的配置
        
        Args:
            context_id: 上下文ID
            key: 配置名
            value: 配置值
        """
        if hasattr(global_config, key):
            if context_id not in self._context_config:
                self._context_config[context_id] = {}
            self._context_config[context_id][key] = value
        else:
            raise ValueError(f"未知的配置项: {key}")
    
    def clear(self) -> None:
        """清空所有局部配置"""
        self._config.clear()
        self._context_config.clear()
    
    def clear_context(self, context_id: str) -> None:
        """清空指定上下文的配置
        
        Args:
            context_id: 上下文ID
        """
        if context_id in self._context_config:
            del self._context_config[context_id]

# 创建局部配置实例
local_config = LocalConfig()
