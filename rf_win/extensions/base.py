# 扩展模块基础类
# 提供插件化扩展机制，支持自定义定位策略和关键字扩展

from abc import ABC, abstractmethod
from typing import Any, Dict, List

class ExtensionBase(ABC):
    """扩展基础类，所有扩展必须继承此类"""
    
    @property
    @abstractmethod
    def name(self) -> str:
        """扩展名称"""
        pass
    
    @abstractmethod
    def initialize(self) -> None:
        """初始化扩展"""
        pass
    
    def get_custom_keywords(self) -> Dict[str, Any]:
        """获取自定义关键字
        
        Returns:
            关键字名称到关键字函数的映射
        """
        return {}
    
    def get_custom_locator_strategies(self) -> Dict[str, Any]:
        """获取自定义定位策略
        
        Returns:
            定位策略名称到定位函数的映射
        """
        return {}
    
    def shutdown(self) -> None:
        """关闭扩展"""
        pass

class ExtensionManager:
    """扩展管理器，负责管理所有扩展"""
    
    def __init__(self):
        self._extensions: Dict[str, ExtensionBase] = {}
        self._custom_keywords: Dict[str, Any] = {}
        self._custom_locator_strategies: Dict[str, Any] = {}
    
    def register_extension(self, extension: ExtensionBase) -> None:
        """注册扩展
        
        Args:
            extension: 扩展实例
        """
        name = extension.name
        if name in self._extensions:
            raise ValueError(f"Extension already registered: {name}")
        
        extension.initialize()
        self._extensions[name] = extension
        
        # 注册自定义关键字
        self._custom_keywords.update(extension.get_custom_keywords())
        
        # 注册自定义定位策略
        self._custom_locator_strategies.update(extension.get_custom_locator_strategies())
    
    def get_extension(self, name: str) -> ExtensionBase:
        """获取扩展实例
        
        Args:
            name: 扩展名称
        
        Returns:
            扩展实例
        
        Raises:
            ValueError: 如果扩展不存在
        """
        if name not in self._extensions:
            raise ValueError(f"Extension not found: {name}")
        return self._extensions[name]
    
    def get_custom_keywords(self) -> Dict[str, Any]:
        """获取所有自定义关键字
        
        Returns:
            关键字名称到关键字函数的映射
        """
        return self._custom_keywords
    
    def get_custom_locator_strategy(self, name: str) -> Any:
        """获取自定义定位策略
        
        Args:
            name: 定位策略名称
        
        Returns:
            定位函数
        
        Raises:
            ValueError: 如果定位策略不存在
        """
        if name not in self._custom_locator_strategies:
            raise ValueError(f"Locator strategy not found: {name}")
        return self._custom_locator_strategies[name]
    
    def shutdown_all(self) -> None:
        """关闭所有扩展"""
        for extension in self._extensions.values():
            extension.shutdown()
        self._extensions.clear()
        self._custom_keywords.clear()
        self._custom_locator_strategies.clear()

# 创建扩展管理器实例
extension_manager = ExtensionManager()
