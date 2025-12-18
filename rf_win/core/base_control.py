# 控件抽象层
# 定义控件交互的基本接口

from abc import ABC, abstractmethod
from typing import Optional, List, Dict, Any, Tuple

class BaseControl(ABC):
    """控件抽象类，定义控件交互的基本接口"""
    
    def __init__(self, control_id: str, window: Any, config: Optional[Dict[str, Any]] = None):
        """初始化控件抽象类
        
        Args:
            control_id: 控件ID
            window: 所属窗口对象
            config: 控件配置
        """
        self.control_id = control_id
        self.window = window
        self.config = config or {}
    
    @abstractmethod
    def click(self, button: str = "left", count: int = 1, x_offset: int = 0, y_offset: int = 0) -> bool:
        """点击控件
        
        Args:
            button: 鼠标按钮（left, right, middle）
            count: 点击次数（1: 单击, 2: 双击）
            x_offset: 相对控件左上角的X偏移（像素）
            y_offset: 相对控件左上角的Y偏移（像素）
        
        Returns:
            是否点击成功
        """
        pass
    
    @abstractmethod
    def right_click(self, x_offset: int = 0, y_offset: int = 0) -> bool:
        """右键点击控件
        
        Args:
            x_offset: 相对控件左上角的X偏移（像素）
            y_offset: 相对控件左上角的Y偏移（像素）
        
        Returns:
            是否点击成功
        """
        pass
    
    @abstractmethod
    def double_click(self, x_offset: int = 0, y_offset: int = 0) -> bool:
        """双击控件
        
        Args:
            x_offset: 相对控件左上角的X偏移（像素）
            y_offset: 相对控件左上角的Y偏移（像素）
        
        Returns:
            是否点击成功
        """
        pass
    
    @abstractmethod
    def hover(self, x_offset: int = 0, y_offset: int = 0, duration: float = 0) -> bool:
        """鼠标悬停在控件上
        
        Args:
            x_offset: 相对控件左上角的X偏移（像素）
            y_offset: 相对控件左上角的Y偏移（像素）
            duration: 悬停时长（秒）
        
        Returns:
            是否悬停成功
        """
        pass
    
    @abstractmethod
    def drag_to(self, target: Any, duration: float = 1.0) -> bool:
        """将控件拖拽到目标位置
        
        Args:
            target: 目标对象（控件或坐标元组(x, y)）
            duration: 拖拽时长（秒）
        
        Returns:
            是否拖拽成功
        """
        pass
    
    @abstractmethod
    def type_text(self, text: str, clear_first: bool = True, slow: bool = False, interval: float = 0.05) -> bool:
        """在控件中输入文本
        
        Args:
            text: 要输入的文本
            clear_first: 是否先清空控件
            slow: 是否慢速输入（模拟真人）
            interval: 慢速输入的间隔（秒）
        
        Returns:
            是否输入成功
        """
        pass
    
    @abstractmethod
    def clear(self) -> bool:
        """清空控件内容
        
        Returns:
            是否清空成功
        """
        pass
    
    @abstractmethod
    def get_text(self) -> Optional[str]:
        """获取控件文本
        
        Returns:
            控件文本，如果控件不可访问则返回None
        """
        pass
    
    @abstractmethod
    def set_text(self, text: str) -> bool:
        """设置控件文本
        
        Args:
            text: 要设置的文本
        
        Returns:
            是否设置成功
        """
        pass
    
    @abstractmethod
    def is_enabled(self) -> bool:
        """检查控件是否启用
        
        Returns:
            是否启用
        """
        pass
    
    @abstractmethod
    def is_visible(self) -> bool:
        """检查控件是否可见
        
        Returns:
            是否可见
        """
        pass
    
    @abstractmethod
    def is_selected(self) -> bool:
        """检查控件是否被选中（适用于复选框、单选按钮等）
        
        Returns:
            是否被选中
        """
        pass
    
    @abstractmethod
    def select(self) -> bool:
        """选中控件（适用于复选框、单选按钮等）
        
        Returns:
            是否选中成功
        """
        pass
    
    @abstractmethod
    def deselect(self) -> bool:
        """取消选中控件（适用于复选框等）
        
        Returns:
            是否取消选中成功
        """
        pass
    
    @abstractmethod
    def get_rect(self) -> Optional[Tuple[int, int, int, int]]:
        """获取控件矩形区域（x, y, width, height）
        
        Returns:
            控件矩形，如果控件不可访问则返回None
        """
        pass
    
    @abstractmethod
    def get_name(self) -> Optional[str]:
        """获取控件名称
        
        Returns:
            控件名称，如果控件不可访问则返回None
        """
        pass
    
    @abstractmethod
    def get_class_name(self) -> Optional[str]:
        """获取控件类名
        
        Returns:
            控件类名，如果控件不可访问则返回None
        """
        pass
    
    @abstractmethod
    def get_automation_id(self) -> Optional[str]:
        """获取控件自动化ID
        
        Returns:
            自动化ID，如果控件不可访问则返回None
        """
        pass
    
    @abstractmethod
    def get_control_type(self) -> Optional[str]:
        """获取控件类型
        
        Returns:
            控件类型，如果控件不可访问则返回None
        """
        pass
    
    @abstractmethod
    def get_attribute(self, name: str) -> Optional[Any]:
        """获取控件属性
        
        Args:
            name: 属性名
        
        Returns:
            属性值，如果属性不存在则返回None
        """
        pass
    
    @abstractmethod
    def set_attribute(self, name: str, value: Any) -> bool:
        """设置控件属性
        
        Args:
            name: 属性名
            value: 属性值
        
        Returns:
            是否设置成功
        """
        pass
    
    @abstractmethod
    def focus(self) -> bool:
        """将焦点设置到控件上
        
        Returns:
            是否设置成功
        """
        pass
    
    @abstractmethod
    def has_focus(self) -> bool:
        """检查控件是否有焦点
        
        Returns:
            是否有焦点
        """
        pass
    
    @abstractmethod
    def find_element(self, locator: str, timeout: Optional[float] = None) -> Any:
        """在控件中查找子控件
        
        Args:
            locator: 子控件定位器
            timeout: 超时时间（秒）
        
        Returns:
            子控件对象，如果未找到则返回None
        """
        pass
    
    @abstractmethod
    def find_elements(self, locator: str, timeout: Optional[float] = None) -> List[Any]:
        """在控件中查找所有匹配的子控件
        
        Args:
            locator: 子控件定位器
            timeout: 超时时间（秒）
        
        Returns:
            子控件对象列表
        """
        pass
    
    @abstractmethod
    def get_parent(self) -> Any:
        """获取父控件
        
        Returns:
            父控件对象，如果没有父控件则返回None
        """
        pass
    
    @abstractmethod
    def get_children(self) -> List[Any]:
        """获取所有子控件
        
        Returns:
            子控件对象列表
        """
        pass
    
    @abstractmethod
    def get_control_info(self) -> Dict[str, Any]:
        """获取控件信息
        
        Returns:
            控件信息字典
        """
        pass
