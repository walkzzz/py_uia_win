# 后端工厂模块
# 管理和切换不同的自动化后端实现

from typing import Any, Dict, Optional
from abc import ABC, abstractmethod

class Backend(ABC):
    """后端抽象类"""
    
    @abstractmethod
    def create_application(self, app_id: str, config: Optional[Dict[str, Any]] = None) -> Any:
        """创建应用对象
        
        Args:
            app_id: 应用ID
            config: 应用配置
        
        Returns:
            应用对象
        """
        pass
    
    @abstractmethod
    def create_window(self, window_id: str, application: Any, config: Optional[Dict[str, Any]] = None) -> Any:
        """创建窗口对象
        
        Args:
            window_id: 窗口ID
            application: 所属应用对象
            config: 窗口配置
        
        Returns:
            窗口对象
        """
        pass
    
    @abstractmethod
    def create_control(self, control_id: str, window: Any, config: Optional[Dict[str, Any]] = None) -> Any:
        """创建控件对象
        
        Args:
            control_id: 控件ID
            window: 所属窗口对象
            config: 控件配置
        
        Returns:
            控件对象
        """
        pass
    
    @abstractmethod
    def create_operation(self) -> Any:
        """创建操作对象
        
        Returns:
            操作对象
        """
        pass

class BackendFactory:
    """后端工厂类"""
    
    def __init__(self):
        # 注册的后端映射
        self._backends: Dict[str, Backend] = {}
        # 当前默认后端
        self._default_backend: str = "auto"
    
    def register_backend(self, name: str, backend: Backend) -> None:
        """注册后端
        
        Args:
            name: 后端名称
            backend: 后端对象
        """
        self._backends[name] = backend
    
    def get_backend(self, name: str = None) -> Backend:
        """获取后端对象
        
        Args:
            name: 后端名称，如果为None则使用默认后端
        
        Returns:
            后端对象
        
        Raises:
            ValueError: 如果后端不存在
        """
        if name is None:
            name = self._default_backend
        
        if name == "auto":
            # 自动选择后端，默认使用pywinauto
            if "pywinauto" in self._backends:
                return self._backends["pywinauto"]
            raise ValueError("No backend available for auto selection")
        
        if name not in self._backends:
            raise ValueError(f"Unknown backend: {name}")
        
        return self._backends[name]
    
    def set_default_backend(self, name: str) -> None:
        """设置默认后端
        
        Args:
            name: 后端名称
        
        Raises:
            ValueError: 如果后端不存在
        """
        if name not in self._backends and name != "auto":
            raise ValueError(f"Unknown backend: {name}")
        self._default_backend = name
    
    def get_available_backends(self) -> list:
        """获取可用的后端列表
        
        Returns:
            后端名称列表
        """
        return list(self._backends.keys())

# 创建后端工厂实例
backend_factory = BackendFactory()
