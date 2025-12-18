# 窗口抽象层
# 定义窗口管理的基本接口

from abc import ABC, abstractmethod
from typing import Optional, List, Dict, Any, Tuple

class BaseWindow(ABC):
    """窗口抽象类，定义窗口管理的基本接口"""
    
    def __init__(self, window_id: str, application: Any, config: Optional[Dict[str, Any]] = None):
        """初始化窗口抽象类
        
        Args:
            window_id: 窗口ID
            application: 所属应用对象
            config: 窗口配置
        """
        self.window_id = window_id
        self.application = application
        self.config = config or {}
    
    @abstractmethod
    def activate(self) -> bool:
        """激活窗口
        
        Returns:
            是否激活成功
        """
        pass
    
    @abstractmethod
    def close(self, timeout: float = 10.0) -> bool:
        """关闭窗口
        
        Args:
            timeout: 超时时间（秒）
        
        Returns:
            是否关闭成功
        """
        pass
    
    @abstractmethod
    def is_active(self) -> bool:
        """检查窗口是否处于激活状态
        
        Returns:
            是否激活
        """
        pass
    
    @abstractmethod
    def is_visible(self) -> bool:
        """检查窗口是否可见
        
        Returns:
            是否可见
        """
        pass
    
    @abstractmethod
    def is_closed(self) -> bool:
        """检查窗口是否已关闭
        
        Returns:
            是否关闭
        """
        pass
    
    @abstractmethod
    def maximize(self) -> bool:
        """最大化窗口
        
        Returns:
            是否成功
        """
        pass
    
    @abstractmethod
    def minimize(self) -> bool:
        """最小化窗口
        
        Returns:
            是否成功
        """
        pass
    
    @abstractmethod
    def restore(self) -> bool:
        """恢复窗口（从最大化/最小化状态）
        
        Returns:
            是否成功
        """
        pass
    
    @abstractmethod
    def resize(self, width: int, height: int) -> bool:
        """调整窗口大小
        
        Args:
            width: 宽度（像素）
            height: 高度（像素）
        
        Returns:
            是否成功
        """
        pass
    
    @abstractmethod
    def move(self, x: int, y: int) -> bool:
        """移动窗口
        
        Args:
            x: 目标X坐标（像素）
            y: 目标Y坐标（像素）
        
        Returns:
            是否成功
        """
        pass
    
    @abstractmethod
    def get_title(self) -> Optional[str]:
        """获取窗口标题
        
        Returns:
            窗口标题，如果窗口已关闭则返回None
        """
        pass
    
    @abstractmethod
    def get_class_name(self) -> Optional[str]:
        """获取窗口类名
        
        Returns:
            窗口类名，如果窗口已关闭则返回None
        """
        pass
    
    @abstractmethod
    def get_rect(self) -> Optional[Tuple[int, int, int, int]]:
        """获取窗口矩形区域（x, y, width, height）
        
        Returns:
            窗口矩形，如果窗口已关闭则返回None
        """
        pass
    
    @abstractmethod
    def get_client_rect(self) -> Optional[Tuple[int, int, int, int]]:
        """获取窗口客户端区域（x, y, width, height）
        
        Returns:
            客户端区域矩形，如果窗口已关闭则返回None
        """
        pass
    
    @abstractmethod
    def wait_for_close(self, timeout: float = 10.0) -> bool:
        """等待窗口关闭
        
        Args:
            timeout: 超时时间（秒）
        
        Returns:
            窗口是否在超时内关闭
        """
        pass
    
    @abstractmethod
    def find_element(self, locator: str, timeout: Optional[float] = None) -> Any:
        """查找窗口中的控件
        
        Args:
            locator: 控件定位器
            timeout: 超时时间（秒）
        
        Returns:
            控件对象，如果未找到则返回None
        """
        pass
    
    @abstractmethod
    def find_elements(self, locator: str, timeout: Optional[float] = None) -> List[Any]:
        """查找窗口中的所有匹配控件
        
        Args:
            locator: 控件定位器
            timeout: 超时时间（秒）
        
        Returns:
            控件对象列表
        """
        pass
    
    @abstractmethod
    def get_all_elements(self) -> List[Any]:
        """获取窗口中的所有控件
        
        Returns:
            控件对象列表
        """
        pass
    
    @abstractmethod
    def get_window_info(self) -> Dict[str, Any]:
        """获取窗口信息
        
        Returns:
            窗口信息字典
        """
        pass
