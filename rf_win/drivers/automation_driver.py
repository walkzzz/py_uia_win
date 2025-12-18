# 自动化驱动模块
# 封装对pywinauto和UIAutomation的调用，提供统一的接口

from typing import Any, Dict, List, Optional, Tuple
from abc import ABC, abstractmethod
from .version_adapter import version_adapter

class AutomationDriver(ABC):
    """自动化驱动抽象基类，定义统一的自动化接口"""
    
    @property
    @abstractmethod
    def name(self) -> str:
        """驱动名称"""
        pass
    
    @abstractmethod
    def create_application(self, app_id: str, backend: str = "uia") -> Any:
        """创建应用对象
        
        Args:
            app_id: 应用ID
            backend: 后端类型
        
        Returns:
            应用对象
        """
        pass
    
    @abstractmethod
    def connect_to_application(self, identifier: Any, backend: str = "uia") -> Any:
        """连接到已运行的应用
        
        Args:
            identifier: 应用标识符（PID、进程名、窗口标题等）
            backend: 后端类型
        
        Returns:
            应用对象
        """
        pass
    
    @abstractmethod
    def find_window(self, app: Any, window_identifier: Any) -> Any:
        """查找窗口
        
        Args:
            app: 应用对象
            window_identifier: 窗口标识符
        
        Returns:
            窗口对象
        """
        pass
    
    @abstractmethod
    def find_control(self, window: Any, locator: str, timeout: float = 10.0) -> Any:
        """查找控件
        
        Args:
            window: 窗口对象
            locator: 控件定位器
            timeout: 超时时间
        
        Returns:
            控件对象
        """
        pass
    
    @abstractmethod
    def click_control(self, control: Any, button: str = "left", count: int = 1, x_offset: int = 0, y_offset: int = 0) -> bool:
        """点击控件
        
        Args:
            control: 控件对象
            button: 鼠标按钮
            count: 点击次数
            x_offset: X偏移
            y_offset: Y偏移
        
        Returns:
            是否成功
        """
        pass
    
    @abstractmethod
    def type_into_control(self, control: Any, text: str, clear_first: bool = True, slow: bool = False, interval: float = 0.05) -> bool:
        """向控件输入文本
        
        Args:
            control: 控件对象
            text: 要输入的文本
            clear_first: 是否先清空
            slow: 是否慢速输入
            interval: 输入间隔
        
        Returns:
            是否成功
        """
        pass
    
    @abstractmethod
    def get_control_text(self, control: Any) -> Optional[str]:
        """获取控件文本
        
        Args:
            control: 控件对象
        
        Returns:
            控件文本
        """
        pass
    
    @abstractmethod
    def close_application(self, app: Any, timeout: float = 10.0) -> bool:
        """关闭应用
        
        Args:
            app: 应用对象
            timeout: 超时时间
        
        Returns:
            是否成功
        """
        pass

class PywinautoDriver(AutomationDriver):
    """pywinauto驱动实现"""
    
    @property
    def name(self) -> str:
        return "pywinauto"
    
    def create_application(self, app_id: str, backend: str = "uia") -> Any:
        """创建pywinauto应用对象"""
        from pywinauto import Application as PywinautoApp
        return PywinautoApp(backend=backend)
    
    def connect_to_application(self, identifier: Any, backend: str = "uia") -> Any:
        """连接到已运行的应用"""
        from pywinauto import Application as PywinautoApp
        app = PywinautoApp(backend=backend)
        
        if isinstance(identifier, int):
            app.connect(process=identifier)
        elif isinstance(identifier, str):
            if identifier.isdigit():
                app.connect(process=int(identifier))
            else:
                app.connect(title=identifier)
        else:
            raise ValueError(f"Invalid identifier type: {type(identifier)}")
        
        return app
    
    def find_window(self, app: Any, window_identifier: Any) -> Any:
        """查找窗口"""
        if isinstance(window_identifier, str):
            return app.window(title=window_identifier)
        elif isinstance(window_identifier, int):
            return app.window(handle=window_identifier)
        else:
            return app.window(**window_identifier)
    
    def find_control(self, window: Any, locator: str, timeout: float = 10.0) -> Any:
        """查找控件"""
        # 解析定位器
        if locator.startswith("id="):
            return window.child_window(auto_id=locator[3:], timeout=timeout)
        elif locator.startswith("name="):
            return window.child_window(name=locator[5:], timeout=timeout)
        elif locator.startswith("class="):
            return window.child_window(class_name=locator[6:], timeout=timeout)
        elif locator.startswith("xpath="):
            # pywinauto不直接支持XPath，这里做简单处理
            return window.child_window(title=locator[6:], timeout=timeout)
        else:
            return window.child_window(title=locator, timeout=timeout)
    
    def click_control(self, control: Any, button: str = "left", count: int = 1, x_offset: int = 0, y_offset: int = 0) -> bool:
        """点击控件"""
        try:
            if count == 1:
                if button == "left":
                    control.click(coords=(x_offset, y_offset))
                elif button == "right":
                    control.right_click(coords=(x_offset, y_offset))
                else:
                    return False
            elif count == 2:
                control.double_click(coords=(x_offset, y_offset))
            else:
                return False
            return True
        except Exception:
            return False
    
    def type_into_control(self, control: Any, text: str, clear_first: bool = True, slow: bool = False, interval: float = 0.05) -> bool:
        """向控件输入文本"""
        try:
            if clear_first:
                control.set_text("")
            
            if slow:
                for char in text:
                    control.type_keys(char)
                    import time
                    time.sleep(interval)
            else:
                control.type_keys(text)
            return True
        except Exception:
            return False
    
    def get_control_text(self, control: Any) -> Optional[str]:
        """获取控件文本"""
        try:
            return control.window_text()
        except Exception:
            return None
    
    def close_application(self, app: Any, timeout: float = 10.0) -> bool:
        """关闭应用"""
        try:
            app.kill_me(timeout=timeout)
            return True
        except Exception:
            return False

class UIAutomationDriver(AutomationDriver):
    """UIAutomation驱动实现"""
    
    @property
    def name(self) -> str:
        return "uiautomation"
    
    def create_application(self, app_id: str, backend: str = "uia") -> Any:
        """创建UIAutomation应用对象"""
        # UIAutomation不直接使用应用对象，这里返回None
        return None
    
    def connect_to_application(self, identifier: Any, backend: str = "uia") -> Any:
        """连接到已运行的应用"""
        # UIAutomation不直接使用应用对象，这里返回None
        return None
    
    def find_window(self, app: Any, window_identifier: Any) -> Any:
        """查找窗口"""
        import uiautomation as auto
        if isinstance(window_identifier, str):
            return auto.WindowControl(searchDepth=1, Name=window_identifier)
        elif isinstance(window_identifier, int):
            return auto.WindowControl(handle=window_identifier)
        else:
            return auto.WindowControl(**window_identifier)
    
    def find_control(self, window: Any, locator: str, timeout: float = 10.0) -> Any:
        """查找控件"""
        try:
            if locator.startswith("id="):
                return window.Control(AutomationId=locator[3:])
            elif locator.startswith("name="):
                return window.Control(Name=locator[5:])
            elif locator.startswith("class="):
                return window.Control(ClassName=locator[6:])
            elif locator.startswith("xpath="):
                # UIAutomation支持XPath-like语法
                return window.Control(searchDepth=10, Name=locator[6:])
            else:
                return window.Control(Name=locator)
        except Exception:
            import time
            time.sleep(0.5)
            # 重试一次
            try:
                if locator.startswith("id="):
                    return window.Control(AutomationId=locator[3:])
                else:
                    return window.Control(Name=locator)
            except Exception:
                return None
    
    def click_control(self, control: Any, button: str = "left", count: int = 1, x_offset: int = 0, y_offset: int = 0) -> bool:
        """点击控件"""
        try:
            if count == 1:
                if button == "left":
                    control.Click()
                elif button == "right":
                    control.RightClick()
                else:
                    return False
            elif count == 2:
                control.DoubleClick()
            else:
                return False
            return True
        except Exception:
            return False
    
    def type_into_control(self, control: Any, text: str, clear_first: bool = True, slow: bool = False, interval: float = 0.05) -> bool:
        """向控件输入文本"""
        try:
            if clear_first:
                control.SendKeys("{Ctrl}a", waitTime=0.1)
                control.SendKeys("{Delete}", waitTime=0.1)
            
            if slow:
                for char in text:
                    control.SendKeys(char, waitTime=interval)
            else:
                control.SendKeys(text)
            return True
        except Exception:
            return False
    
    def get_control_text(self, control: Any) -> Optional[str]:
        """获取控件文本"""
        try:
            return control.Name
        except Exception:
            return None
    
    def close_application(self, app: Any, timeout: float = 10.0) -> bool:
        """关闭应用"""
        # UIAutomation通过窗口关闭应用
        try:
            app.Close()
            return True
        except Exception:
            return False

class DriverFactory:
    """驱动工厂，负责创建和管理自动化驱动"""
    
    def __init__(self):
        self._drivers: Dict[str, AutomationDriver] = {}
        self._default_driver: Optional[str] = None
        
        # 注册可用的驱动
        if version_adapter.is_pywinauto_available():
            self._drivers["pywinauto"] = PywinautoDriver()
        if version_adapter.is_uiautomation_available():
            self._drivers["uiautomation"] = UIAutomationDriver()
        
        # 设置默认驱动
        if "pywinauto" in self._drivers:
            self._default_driver = "pywinauto"
        elif "uiautomation" in self._drivers:
            self._default_driver = "uiautomation"
    
    def get_driver(self, name: Optional[str] = None) -> AutomationDriver:
        """获取驱动实例
        
        Args:
            name: 驱动名称，如果为None则使用默认驱动
        
        Returns:
            驱动实例
        
        Raises:
            ValueError: 如果驱动不存在
        """
        if name is None:
            name = self._default_driver
        
        if name not in self._drivers:
            raise ValueError(f"Driver {name} not available")
        
        return self._drivers[name]
    
    def set_default_driver(self, name: str) -> None:
        """设置默认驱动
        
        Args:
            name: 驱动名称
        
        Raises:
            ValueError: 如果驱动不存在
        """
        if name not in self._drivers:
            raise ValueError(f"Driver {name} not available")
        
        self._default_driver = name
    
    def get_available_drivers(self) -> List[str]:
        """获取可用的驱动列表
        
        Returns:
            驱动名称列表
        """
        return list(self._drivers.keys())

# 创建驱动工厂实例
driver_factory = DriverFactory()
