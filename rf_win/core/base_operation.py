# 基础操作抽象层
# 定义鼠标、键盘、截图等通用操作的基本接口

from abc import ABC, abstractmethod
from typing import Optional, List, Tuple, Any, Callable

class BaseOperation(ABC):
    """基础操作抽象类，定义鼠标、键盘、截图等通用操作的接口"""
    
    @abstractmethod
    def mouse_click(self, x: int, y: int, button: str = "left", count: int = 1) -> bool:
        """鼠标点击指定坐标
        
        Args:
            x: X坐标（像素）
            y: Y坐标（像素）
            button: 鼠标按钮（left, right, middle）
            count: 点击次数（1: 单击, 2: 双击）
        
        Returns:
            是否点击成功
        """
        pass
    
    @abstractmethod
    def mouse_move(self, x: int, y: int, duration: float = 0) -> bool:
        """鼠标移动到指定坐标
        
        Args:
            x: X坐标（像素）
            y: Y坐标（像素）
            duration: 移动时长（秒）
        
        Returns:
            是否移动成功
        """
        pass
    
    @abstractmethod
    def mouse_drag(self, start_x: int, start_y: int, end_x: int, end_y: int, duration: float = 1.0) -> bool:
        """鼠标拖拽
        
        Args:
            start_x: 起始X坐标（像素）
            start_y: 起始Y坐标（像素）
            end_x: 结束X坐标（像素）
            end_y: 结束Y坐标（像素）
            duration: 拖拽时长（秒）
        
        Returns:
            是否拖拽成功
        """
        pass
    
    @abstractmethod
    def mouse_wheel(self, x: int, y: int, direction: str = "up", steps: int = 1) -> bool:
        """鼠标滚轮滚动
        
        Args:
            x: X坐标（像素）
            y: Y坐标（像素）
            direction: 滚动方向（up, down）
            steps: 滚动步数
        
        Returns:
            是否滚动成功
        """
        pass
    
    @abstractmethod
    def mouse_hover(self, x: int, y: int, duration: float = 0) -> bool:
        """鼠标悬停在指定坐标
        
        Args:
            x: X坐标（像素）
            y: Y坐标（像素）
            duration: 悬停时长（秒）
        
        Returns:
            是否悬停成功
        """
        pass
    
    @abstractmethod
    def get_mouse_position(self) -> Tuple[int, int]:
        """获取当前鼠标位置
        
        Returns:
            当前鼠标坐标（x, y）
        """
        pass
    
    @abstractmethod
    def press_key(self, key: str) -> bool:
        """按下并释放指定按键
        
        Args:
            key: 按键名称（如A, Enter, Ctrl）
        
        Returns:
            是否按键成功
        """
        pass
    
    @abstractmethod
    def press_keys(self, keys: str) -> bool:
        """按下并释放组合键
        
        Args:
            keys: 组合键字符串（如Ctrl+C, Alt+Tab）
        
        Returns:
            是否按键成功
        """
        pass
    
    @abstractmethod
    def key_down(self, key: str) -> bool:
        """按下指定按键（不释放）
        
        Args:
            key: 按键名称
        
        Returns:
            是否按下成功
        """
        pass
    
    @abstractmethod
    def key_up(self, key: str) -> bool:
        """释放指定按键
        
        Args:
            key: 按键名称
        
        Returns:
            是否释放成功
        """
        pass
    
    @abstractmethod
    def type_text(self, text: str, interval: float = 0.05) -> bool:
        """输入文本
        
        Args:
            text: 要输入的文本
            interval: 按键间隔（秒）
        
        Returns:
            是否输入成功
        """
        pass
    
    @abstractmethod
    def capture_screenshot(self, filename: Optional[str] = None, x: int = 0, y: int = 0, width: int = 0, height: int = 0) -> Optional[str]:
        """捕获屏幕截图
        
        Args:
            filename: 截图保存路径，如果为None则自动生成
            x: 起始X坐标（像素），0表示全屏
            y: 起始Y坐标（像素），0表示全屏
            width: 截图宽度（像素），0表示全屏
            height: 截图高度（像素），0表示全屏
        
        Returns:
            截图保存路径，如果截图失败则返回None
        """
        pass
    
    @abstractmethod
    def capture_window_screenshot(self, window: Any, filename: Optional[str] = None) -> Optional[str]:
        """捕获窗口截图
        
        Args:
            window: 窗口对象
            filename: 截图保存路径，如果为None则自动生成
        
        Returns:
            截图保存路径，如果截图失败则返回None
        """
        pass
    
    @abstractmethod
    def capture_element_screenshot(self, element: Any, filename: Optional[str] = None) -> Optional[str]:
        """捕获控件截图
        
        Args:
            element: 控件对象
            filename: 截图保存路径，如果为None则自动生成
        
        Returns:
            截图保存路径，如果截图失败则返回None
        """
        pass
    
    @abstractmethod
    def wait(self, seconds: float) -> None:
        """等待指定时长
        
        Args:
            seconds: 等待时长（秒）
        """
        pass
    
    @abstractmethod
    def wait_until(self, condition_func: Callable[[], bool], timeout: float = 10.0, interval: float = 0.5) -> bool:
        """等待直到条件满足或超时
        
        Args:
            condition_func: 条件函数，返回True表示条件满足
            timeout: 超时时间（秒）
            interval: 检查间隔（秒）
        
        Returns:
            条件是否在超时内满足
        """
        pass
    
    @abstractmethod
    def get_screen_size(self) -> Tuple[int, int]:
        """获取屏幕尺寸
        
        Returns:
            屏幕尺寸（宽度, 高度）
        """
        pass
    
    @abstractmethod
    def get_dpi_scale(self) -> float:
        """获取屏幕DPI缩放比例
        
        Returns:
            DPI缩放比例（如1.0, 1.25, 1.5）
        """
        pass
    
    @abstractmethod
    def adapt_coordinate(self, x: int, y: int) -> Tuple[int, int]:
        """适配坐标到当前DPI
        
        Args:
            x: 原始X坐标
            y: 原始Y坐标
        
        Returns:
            适配后的坐标
        """
        pass
    
    @abstractmethod
    def adapt_size(self, width: int, height: int) -> Tuple[int, int]:
        """适配尺寸到当前DPI
        
        Args:
            width: 原始宽度
            height: 原始高度
        
        Returns:
            适配后的尺寸
        """
        pass
