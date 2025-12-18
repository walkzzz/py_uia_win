# 应用抽象层
# 定义应用管理的基本接口

from abc import ABC, abstractmethod
from typing import Optional, List, Dict, Any

class BaseApplication(ABC):
    """应用抽象类，定义应用管理的基本接口"""
    
    def __init__(self, app_id: str, config: Optional[Dict[str, Any]] = None):
        """初始化应用抽象类
        
        Args:
            app_id: 应用ID
            config: 应用配置
        """
        self.app_id = app_id
        self.config = config or {}
    
    @abstractmethod
    def start(self, path: str, args: Optional[str] = None, admin: bool = False, background: bool = False) -> bool:
        """启动应用
        
        Args:
            path: 应用路径
            args: 启动参数
            admin: 是否以管理员权限运行
            background: 是否在后台运行
        
        Returns:
            是否启动成功
        """
        pass
    
    @abstractmethod
    def attach(self, identifier: Any) -> bool:
        """附加到已运行的应用
        
        Args:
            identifier: 应用标识符（PID、进程名、窗口标题等）
        
        Returns:
            是否附加成功
        """
        pass
    
    @abstractmethod
    def close(self, timeout: float = 10.0) -> bool:
        """优雅关闭应用
        
        Args:
            timeout: 超时时间（秒）
        
        Returns:
            是否关闭成功
        """
        pass
    
    @abstractmethod
    def kill(self) -> bool:
        """强制关闭应用
        
        Returns:
            是否关闭成功
        """
        pass
    
    @abstractmethod
    def is_running(self) -> bool:
        """检查应用是否正在运行
        
        Returns:
            是否正在运行
        """
        pass
    
    @abstractmethod
    def get_process_id(self) -> Optional[int]:
        """获取应用进程ID
        
        Returns:
            进程ID，如果应用未运行则返回None
        """
        pass
    
    @abstractmethod
    def get_main_window(self) -> Any:
        """获取主窗口
        
        Returns:
            主窗口对象，如果没有主窗口则返回None
        """
        pass
    
    @abstractmethod
    def get_all_windows(self) -> List[Any]:
        """获取应用的所有窗口
        
        Returns:
            窗口对象列表
        """
        pass
    
    @abstractmethod
    def wait_for_main_window(self, timeout: float = 10.0) -> bool:
        """等待主窗口出现
        
        Args:
            timeout: 超时时间（秒）
        
        Returns:
            是否成功找到主窗口
        """
        pass
    
    @abstractmethod
    def get_app_info(self) -> Dict[str, Any]:
        """获取应用信息
        
        Returns:
            应用信息字典
        """
        pass
    
    def __enter__(self):
        """上下文管理器进入方法"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器退出方法，自动关闭应用"""
        self.close()
