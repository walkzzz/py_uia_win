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
    def start_application(self, path: str, args: Optional[str] = None, backend: str = "uia") -> Any:
        """启动应用程序
        
        Args:
            path: 应用程序路径
            args: 启动参数
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
    def close_application(self, app: Any, timeout: float = 10.0) -> bool:
        """关闭应用
        
        Args:
            app: 应用对象
            timeout: 超时时间
        
        Returns:
            是否成功
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
    def find_element(self, parent: Any, locator: Any, timeout: float = 10.0) -> Any:
        """查找单个控件
        
        Args:
            parent: 父控件或窗口对象
            locator: 控件定位器
            timeout: 超时时间
        
        Returns:
            控件对象
        """
        pass
    
    @abstractmethod
    def find_elements(self, parent: Any, locator: Any, timeout: float = 10.0) -> List[Any]:
        """查找多个控件
        
        Args:
            parent: 父控件或窗口对象
            locator: 控件定位器
            timeout: 超时时间
        
        Returns:
            控件对象列表
        """
        pass
    
    @abstractmethod
    def click_element(self, element: Any, button: str = "left", clicks: int = 1, interval: float = 0.0, x_offset: int = 0, y_offset: int = 0) -> bool:
        """点击控件
        
        Args:
            element: 控件对象
            button: 鼠标按钮
            clicks: 点击次数
            interval: 点击间隔
            x_offset: X偏移
            y_offset: Y偏移
        
        Returns:
            是否成功
        """
        pass
    
    @abstractmethod
    def type_text(self, element: Any, text: str, clear_first: bool = True, delay: float = 0.0) -> bool:
        """向控件输入文本
        
        Args:
            element: 控件对象
            text: 要输入的文本
            clear_first: 是否先清空
            delay: 输入延迟
        
        Returns:
            是否成功
        """
        pass
    
    @abstractmethod
    def clear_element_text(self, element: Any) -> bool:
        """清空控件文本
        
        Args:
            element: 控件对象
        
        Returns:
            是否成功
        """
        pass
    
    @abstractmethod
    def get_element_text(self, element: Any) -> Optional[str]:
        """获取控件文本
        
        Args:
            element: 控件对象
        
        Returns:
            控件文本
        """
        pass
    
    @abstractmethod
    def get_element_attribute(self, element: Any, attribute: str) -> Optional[Any]:
        """获取控件属性
        
        Args:
            element: 控件对象
            attribute: 属性名称
        
        Returns:
            属性值
        """
        pass
    
    @abstractmethod
    def is_element_valid(self, element: Any) -> bool:
        """检查控件是否有效
        
        Args:
            element: 控件对象
        
        Returns:
            是否有效
        """
        pass
    
    @abstractmethod
    def is_element_enabled(self, element: Any) -> bool:
        """检查控件是否可用
        
        Args:
            element: 控件对象
        
        Returns:
            是否可用
        """
        pass
    
    @abstractmethod
    def is_element_visible(self, element: Any) -> bool:
        """检查控件是否可见
        
        Args:
            element: 控件对象
        
        Returns:
            是否可见
        """
        pass
    
    @abstractmethod
    def hover_element(self, element: Any) -> bool:
        """鼠标悬停在控件上
        
        Args:
            element: 控件对象
        
        Returns:
            是否成功
        """
        pass
    
    @abstractmethod
    def drag_element_to(self, source_element: Any, target_element: Any) -> bool:
        """拖拽控件到目标位置
        
        Args:
            source_element: 源控件对象
            target_element: 目标控件对象
        
        Returns:
            是否成功
        """
        pass
    
    @abstractmethod
    def select_element(self, element: Any, value: Any = None, text: Optional[str] = None, index: int = -1) -> bool:
        """选择控件选项
        
        Args:
            element: 控件对象
            value: 选项值
            text: 选项文本
            index: 选项索引
        
        Returns:
            是否成功
        """
        pass
    
    @abstractmethod
    def deselect_element(self, element: Any, value: Any = None, text: Optional[str] = None, index: int = -1) -> bool:
        """取消选择控件选项
        
        Args:
            element: 控件对象
            value: 选项值
            text: 选项文本
            index: 选项索引
        
        Returns:
            是否成功
        """
        pass
    
    @abstractmethod
    def is_element_selected(self, element: Any) -> bool:
        """检查控件是否被选中
        
        Args:
            element: 控件对象
        
        Returns:
            是否被选中
        """
        pass

class PywinautoDriver(AutomationDriver):
    """pywinauto驱动实现"""
    
    @property
    def name(self) -> str:
        return "pywinauto"
    
    def start_application(self, path: str, args: Optional[str] = None, backend: str = "uia") -> Any:
        """启动应用程序"""
        from pywinauto import Application as PywinautoApp
        app = PywinautoApp(backend=backend)
        cmd = path
        if args:
            cmd += f" {args}"
        return app.start(cmd)
    
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
    
    def find_element(self, parent: Any, locator: Any, timeout: float = 10.0) -> Any:
        """查找单个控件"""
        # 解析定位器
        if isinstance(locator, str):
            if locator.startswith("id="):
                return parent.child_window(auto_id=locator[3:], timeout=timeout)
            elif locator.startswith("name="):
                return parent.child_window(name=locator[5:], timeout=timeout)
            elif locator.startswith("class="):
                return parent.child_window(class_name=locator[6:], timeout=timeout)
            elif locator.startswith("xpath="):
                # pywinauto不直接支持XPath，这里做简单处理
                return parent.child_window(title=locator[6:], timeout=timeout)
            else:
                return parent.child_window(title=locator, timeout=timeout)
        else:
            return parent.child_window(timeout=timeout, **locator)
    
    def find_elements(self, parent: Any, locator: Any, timeout: float = 10.0) -> List[Any]:
        """查找多个控件"""
        # pywinauto没有直接的find_elements方法，这里返回一个包含单个元素的列表
        return [self.find_element(parent, locator, timeout)]
    
    def click_element(self, element: Any, button: str = "left", clicks: int = 1, interval: float = 0.0, x_offset: int = 0, y_offset: int = 0) -> bool:
        """点击控件"""
        try:
            if clicks == 1:
                if button == "left":
                    element.click()
                elif button == "right":
                    element.right_click()
                else:
                    return False
            elif clicks == 2:
                element.double_click()
            else:
                return False
            return True
        except Exception:
            return False
    
    def type_text(self, element: Any, text: str, clear_first: bool = True, delay: float = 0.0) -> bool:
        """向控件输入文本"""
        try:
            if clear_first:
                self.clear_element_text(element)
            
            if delay > 0:
                for char in text:
                    element.type_keys(char)
                    import time
                    time.sleep(delay)
            else:
                element.type_keys(text)
            return True
        except Exception:
            return False
    
    def clear_element_text(self, element: Any) -> bool:
        """清空控件文本"""
        try:
            element.set_text("")
            return True
        except Exception:
            return False
    
    def get_element_text(self, element: Any) -> Optional[str]:
        """获取控件文本"""
        try:
            return element.window_text()
        except Exception:
            return None
    
    def get_element_attribute(self, element: Any, attribute: str) -> Optional[Any]:
        """获取控件属性"""
        try:
            return getattr(element, attribute, None)
        except Exception:
            return None
    
    def is_element_valid(self, element: Any) -> bool:
        """检查控件是否有效"""
        try:
            return element.exists()
        except Exception:
            return False
    
    def is_element_enabled(self, element: Any) -> bool:
        """检查控件是否可用"""
        try:
            return element.is_enabled()
        except Exception:
            return False
    
    def is_element_visible(self, element: Any) -> bool:
        """检查控件是否可见"""
        try:
            return element.is_visible()
        except Exception:
            return False
    
    def hover_element(self, element: Any) -> bool:
        """鼠标悬停在控件上"""
        try:
            element.hover()
            return True
        except Exception:
            return False
    
    def drag_element_to(self, source_element: Any, target_element: Any) -> bool:
        """拖拽控件到目标位置"""
        try:
            source_element.drag_mouse_input(target_element)
            return True
        except Exception:
            return False
    
    def select_element(self, element: Any, value: Any = None, text: Optional[str] = None, index: int = -1) -> bool:
        """选择控件选项"""
        try:
            if value is not None:
                element.select(value)
            elif text is not None:
                element.select(text=text)
            elif index >= 0:
                element.select(index=index)
            else:
                return False
            return True
        except Exception:
            return False
    
    def deselect_element(self, element: Any, value: Any = None, text: Optional[str] = None, index: int = -1) -> bool:
        """取消选择控件选项"""
        try:
            if value is not None:
                element.deselect(value)
            elif text is not None:
                element.deselect(text=text)
            elif index >= 0:
                element.deselect(index=index)
            else:
                return False
            return True
        except Exception:
            return False
    
    def is_element_selected(self, element: Any) -> bool:
        """检查控件是否被选中"""
        try:
            return element.is_selected()
        except Exception:
            return False
    
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
    
    def start_application(self, path: str, args: Optional[str] = None, backend: str = "uia") -> Any:
        """启动应用程序"""
        import subprocess
        cmd = [path]
        if args:
            cmd.extend(args.split())
        subprocess.Popen(cmd)
        # UIAutomation不直接返回应用对象
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
    
    def find_element(self, parent: Any, locator: Any, timeout: float = 10.0) -> Any:
        """查找单个控件"""
        import uiautomation as auto
        import time
        
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                if isinstance(locator, str):
                    if locator.startswith("id="):
                        return parent.Control(AutomationId=locator[3:])
                    elif locator.startswith("name="):
                        return parent.Control(Name=locator[5:])
                    elif locator.startswith("class="):
                        return parent.Control(ClassName=locator[6:])
                    elif locator.startswith("xpath="):
                        # UIAutomation支持XPath-like语法
                        return parent.Control(searchDepth=10, Name=locator[6:])
                    else:
                        return parent.Control(Name=locator)
                else:
                    return parent.Control(**locator)
            except Exception:
                time.sleep(0.5)
        return None
    
    def find_elements(self, parent: Any, locator: Any, timeout: float = 10.0) -> List[Any]:
        """查找多个控件"""
        # UIAutomation没有直接的find_elements方法，这里返回一个包含单个元素的列表
        element = self.find_element(parent, locator, timeout)
        return [element] if element else []
    
    def click_element(self, element: Any, button: str = "left", clicks: int = 1, interval: float = 0.0, x_offset: int = 0, y_offset: int = 0) -> bool:
        """点击控件"""
        try:
            if clicks == 1:
                if button == "left":
                    element.Click()
                elif button == "right":
                    element.RightClick()
                else:
                    return False
            elif clicks == 2:
                element.DoubleClick()
            else:
                return False
            return True
        except Exception:
            return False
    
    def type_text(self, element: Any, text: str, clear_first: bool = True, delay: float = 0.0) -> bool:
        """向控件输入文本"""
        try:
            if clear_first:
                self.clear_element_text(element)
                
            if delay > 0:
                for char in text:
                    element.SendKeys(char, waitTime=delay)
            else:
                element.SendKeys(text)
            return True
        except Exception:
            return False
    
    def clear_element_text(self, element: Any) -> bool:
        """清空控件文本"""
        try:
            element.SendKeys("{Ctrl}a", waitTime=0.1)
            element.SendKeys("{Delete}", waitTime=0.1)
            return True
        except Exception:
            return False
    
    def get_element_text(self, element: Any) -> Optional[str]:
        """获取控件文本"""
        try:
            return element.Name
        except Exception:
            return None
    
    def get_element_attribute(self, element: Any, attribute: str) -> Optional[Any]:
        """获取控件属性"""
        try:
            return getattr(element, attribute, None)
        except Exception:
            return None
    
    def is_element_valid(self, element: Any) -> bool:
        """检查控件是否有效"""
        try:
            return element.Exists()
        except Exception:
            return False
    
    def is_element_enabled(self, element: Any) -> bool:
        """检查控件是否可用"""
        try:
            return element.IsEnabled()
        except Exception:
            return False
    
    def is_element_visible(self, element: Any) -> bool:
        """检查控件是否可见"""
        try:
            return element.IsVisible()
        except Exception:
            return False
    
    def hover_element(self, element: Any) -> bool:
        """鼠标悬停在控件上"""
        try:
            element.Hover()
            return True
        except Exception:
            return False
    
    def drag_element_to(self, source_element: Any, target_element: Any) -> bool:
        """拖拽控件到目标位置"""
        try:
            source_element.DragTo(target_element)
            return True
        except Exception:
            return False
    
    def select_element(self, element: Any, value: Any = None, text: Optional[str] = None, index: int = -1) -> bool:
        """选择控件选项"""
        try:
            # UIAutomation的选择逻辑比较特殊，这里做简单处理
            element.Select()
            return True
        except Exception:
            return False
    
    def deselect_element(self, element: Any, value: Any = None, text: Optional[str] = None, index: int = -1) -> bool:
        """取消选择控件选项"""
        try:
            # UIAutomation的取消选择逻辑比较特殊，这里做简单处理
            element.Deselect()
            return True
        except Exception:
            return False
    
    def is_element_selected(self, element: Any) -> bool:
        """检查控件是否被选中"""
        try:
            return element.IsSelected()
        except Exception:
            return False
    
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
        
        if name == "auto":
            # 自动选择驱动，默认使用pywinauto
            if "pywinauto" in self._drivers:
                return self._drivers["pywinauto"]
            elif "uiautomation" in self._drivers:
                return self._drivers["uiautomation"]
            raise ValueError("No driver available for auto selection")
        
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
        if name != "auto" and name not in self._drivers:
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

# 导出类
export = AutomationDriver, PywinautoDriver, UIAutomationDriver, DriverFactory
