# pywinauto后端实现
# 封装pywinauto库的功能，提供统一的接口给上层使用

from typing import Any, Dict, List, Optional, Tuple
import time
import subprocess
import psutil
from ..core.base_application import BaseApplication
from ..core.base_window import BaseWindow
from ..core.base_control import BaseControl
from ..core.base_operation import BaseOperation
from .backend_factory import Backend
from ..config.local_config import local_config

# 尝试导入pywinauto，处理导入错误
try:
    from pywinauto import Application as PywinautoApp
    from pywinauto.findwindows import find_window, find_windows, ElementNotFoundError
    from pywinauto.keyboard import send_keys, press, release
    from pywinauto.mouse import click, double_click, right_click, move, drag
    from pywinauto.base_wrapper import BaseWrapper
    from pywinauto.controls.uiawrapper import UIAWrapper
    from pywinauto.controls.hwndwrapper import HwndWrapper
    PYWINAUTO_AVAILABLE = True
except ImportError:
    PYWINAUTO_AVAILABLE = False

class PywinautoApplication(BaseApplication):
    """pywinauto应用实现"""
    
    def __init__(self, app_id: str, config: Optional[Dict[str, Any]] = None):
        super().__init__(app_id, config)
        self._app: Optional[Any] = None
        self._process_id: Optional[int] = None
        self._backend = local_config.get("pywinauto_backend", "uia")
    
    def start(self, path: str, args: Optional[str] = None, admin: bool = False, background: bool = False) -> bool:
        """启动应用"""
        if not PYWINAUTO_AVAILABLE:
            raise ImportError("pywinauto is not installed. Please install it with 'pip install pywinauto'")
        
        try:
            cmd = path
            if args:
                cmd += f" {args}"
            
            if admin:
                # 以管理员权限启动
                self._app = PywinautoApp(backend=self._backend)
                self._app.start(cmd, wait_for_idle=True, create_new_console=True, shell=True)
            else:
                self._app = PywinautoApp(backend=self._backend).start(cmd, wait_for_idle=True)
            
            # 获取进程ID
            time.sleep(0.5)  # 等待进程启动
            self._process_id = self._app.process
            return True
        except Exception as e:
            return False
    
    def attach(self, identifier: Any) -> bool:
        """附加到已运行的应用"""
        if not PYWINAUTO_AVAILABLE:
            raise ImportError("pywinauto is not installed. Please install it with 'pip install pywinauto'")
        
        try:
            self._app = PywinautoApp(backend=self._backend)
            
            if isinstance(identifier, int):
                # 通过进程ID附加
                self._app.connect(process=identifier)
            elif isinstance(identifier, str):
                # 通过进程名或窗口标题附加
                if identifier.isdigit():
                    self._app.connect(process=int(identifier))
                else:
                    self._app.connect(title=identifier, timeout=local_config.get("timeout", 10))
            else:
                return False
            
            self._process_id = self._app.process
            return True
        except Exception as e:
            return False
    
    def close(self, timeout: float = 10.0) -> bool:
        """优雅关闭应用"""
        if not self._app:
            return False
        
        try:
            self._app.kill_me(timeout=timeout)
            self._process_id = None
            self._app = None
            return True
        except Exception as e:
            return False
    
    def kill(self) -> bool:
        """强制关闭应用"""
        if not self._process_id:
            return False
        
        try:
            process = psutil.Process(self._process_id)
            process.terminate()
            try:
                process.wait(timeout=5)
            except psutil.TimeoutExpired:
                process.kill()
            
            self._process_id = None
            self._app = None
            return True
        except Exception as e:
            return False
    
    def is_running(self) -> bool:
        """检查应用是否正在运行"""
        if not self._process_id:
            return False
        
        try:
            process = psutil.Process(self._process_id)
            return process.is_running()
        except Exception:
            return False
    
    def get_process_id(self) -> Optional[int]:
        """获取应用进程ID"""
        return self._process_id
    
    def get_main_window(self) -> Any:
        """获取主窗口"""
        if not self._app:
            return None
        
        try:
            main_dlg = self._app.top_window()
            return main_dlg
        except Exception as e:
            return None
    
    def get_all_windows(self) -> List[Any]:
        """获取应用的所有窗口"""
        if not self._process_id:
            return []
        
        try:
            windows = find_windows(process=self._process_id)
            return windows
        except Exception as e:
            return []
    
    def wait_for_main_window(self, timeout: float = 10.0) -> bool:
        """等待主窗口出现"""
        if not self._app:
            return False
        
        try:
            self._app.wait_for_window(timeout=timeout)
            return True
        except Exception as e:
            return False
    
    def get_app_info(self) -> Dict[str, Any]:
        """获取应用信息"""
        info = {
            "app_id": self.app_id,
            "process_id": self._process_id,
            "is_running": self.is_running(),
            "backend": self._backend
        }
        
        if self._app:
            try:
                main_window = self.get_main_window()
                if main_window:
                    info["main_window_title"] = main_window.window_text()
                    info["main_window_class"] = main_window.class_name()
            except Exception as e:
                pass
        
        return info

class PywinautoWindow(BaseWindow):
    """pywinauto窗口实现"""
    
    def __init__(self, window_id: Any, application: Any, config: Optional[Dict[str, Any]] = None):
        super().__init__(window_id, application, config)
        self._window: Optional[BaseWrapper] = None
        self._parse_window_id(window_id)
    
    def _parse_window_id(self, window_id: str) -> None:
        """解析窗口ID"""
        if isinstance(window_id, int):
            # 窗口句柄
            try:
                self._window = self.application._app.window(handle=window_id)
            except Exception as e:
                self._window = None
        elif isinstance(window_id, str):
            # 窗口标题或其他标识符
            try:
                self._window = self.application._app.window(title=window_id, timeout=local_config.get("timeout", 10))
            except Exception as e:
                self._window = None
        else:
            self._window = window_id
    
    def activate(self) -> bool:
        """激活窗口"""
        if not self._window:
            return False
        
        try:
            self._window.set_focus()
            return True
        except Exception as e:
            return False
    
    def close(self, timeout: float = 10.0) -> bool:
        """关闭窗口"""
        if not self._window:
            return False
        
        try:
            self._window.close(timeout=timeout)
            return True
        except Exception as e:
            return False
    
    def is_active(self) -> bool:
        """检查窗口是否处于激活状态"""
        if not self._window:
            return False
        
        try:
            return self._window.is_active()
        except Exception as e:
            return False
    
    def is_visible(self) -> bool:
        """检查窗口是否可见"""
        if not self._window:
            return False
        
        try:
            return self._window.is_visible()
        except Exception as e:
            return False
    
    def is_closed(self) -> bool:
        """检查窗口是否已关闭"""
        if not self._window:
            return True
        
        try:
            return not self._window.exists()
        except Exception as e:
            return True
    
    def maximize(self) -> bool:
        """最大化窗口"""
        if not self._window:
            return False
        
        try:
            self._window.maximize()
            return True
        except Exception as e:
            return False
    
    def minimize(self) -> bool:
        """最小化窗口"""
        if not self._window:
            return False
        
        try:
            self._window.minimize()
            return True
        except Exception as e:
            return False
    
    def restore(self) -> bool:
        """恢复窗口（从最大化/最小化状态）"""
        if not self._window:
            return False
        
        try:
            self._window.restore()
            return True
        except Exception as e:
            return False
    
    def resize(self, width: int, height: int) -> bool:
        """调整窗口大小"""
        if not self._window:
            return False
        
        try:
            self._window.resize(width=width, height=height)
            return True
        except Exception as e:
            return False
    
    def move(self, x: int, y: int) -> bool:
        """移动窗口"""
        if not self._window:
            return False
        
        try:
            self._window.move_window(x, y)
            return True
        except Exception as e:
            return False
    
    def get_title(self) -> Optional[str]:
        """获取窗口标题"""
        if not self._window:
            return None
        
        try:
            return self._window.window_text()
        except Exception as e:
            return None
    
    def get_class_name(self) -> Optional[str]:
        """获取窗口类名"""
        if not self._window:
            return None
        
        try:
            return self._window.class_name()
        except Exception as e:
            return None
    
    def get_rect(self) -> Optional[Tuple[int, int, int, int]]:
        """获取窗口矩形区域（x, y, width, height）"""
        if not self._window:
            return None
        
        try:
            rect = self._window.rectangle()
            return (rect.left, rect.top, rect.width(), rect.height())
        except Exception as e:
            return None
    
    def get_client_rect(self) -> Optional[Tuple[int, int, int, int]]:
        """获取窗口客户端区域（x, y, width, height）"""
        if not self._window:
            return None
        
        try:
            rect = self._window.client_rects()[0]
            return (rect.left, rect.top, rect.width(), rect.height())
        except Exception as e:
            return None
    
    def wait_for_close(self, timeout: float = 10.0) -> bool:
        """等待窗口关闭"""
        if not self._window:
            return True
        
        try:
            self._window.wait_not('exists', timeout=timeout)
            return True
        except Exception as e:
            return False
    
    def _parse_locator(self, locator: str) -> Dict[str, Any]:
        """解析定位器
        
        将定位器字符串（如id=btn_login, name=登录）转换为pywinauto可以理解的格式
        
        Args:
            locator: 定位器字符串
        
        Returns:
            定位器字典
        """
        locator_dict = {}
        
        if locator.startswith("id="):
            # 自动化ID定位
            locator_dict["auto_id"] = locator[3:]
        elif locator.startswith("name="):
            # 名称定位
            locator_dict["name"] = locator[5:]
        elif locator.startswith("class="):
            # 类名定位
            locator_dict["class_name"] = locator[6:]
        elif locator.startswith("xpath="):
            # XPath定位（pywinauto不直接支持，需要特殊处理）
            # 这里简单处理，实际实现需要更复杂的逻辑
            locator_dict["title"] = locator[6:]
        else:
            # 默认使用标题定位
            locator_dict["title"] = locator
        
        return locator_dict
    
    def find_element(self, locator: str, timeout: float = None) -> Any:
        """查找窗口中的控件"""
        if not self._window:
            return None
        
        if timeout is None:
            timeout = local_config.get("timeout", 10)
        
        try:
            locator_dict = self._parse_locator(locator)
            element = self._window.child_window(timeout=timeout, **locator_dict)
            return element
        except Exception as e:
            return None
    
    def find_elements(self, locator: str, timeout: float = None) -> List[Any]:
        """查找窗口中的所有匹配控件"""
        if not self._window:
            return []
        
        if timeout is None:
            timeout = local_config.get("timeout", 10)
        
        try:
            locator_dict = self._parse_locator(locator)
            elements = self._window.children(timeout=timeout, **locator_dict)
            return elements
        except Exception as e:
            return []
    
    def get_all_elements(self) -> List[Any]:
        """获取窗口中的所有控件"""
        if not self._window:
            return []
        
        try:
            return self._window.children()
        except Exception as e:
            return []
    
    def get_window_info(self) -> Dict[str, Any]:
        """获取窗口信息"""
        info = {
            "window_id": self.window_id,
            "is_closed": self.is_closed(),
            "is_active": self.is_active(),
            "is_visible": self.is_visible()
        }
        
        if self._window:
            try:
                info["title"] = self.get_title()
                info["class_name"] = self.get_class_name()
                info["rect"] = self.get_rect()
                info["client_rect"] = self.get_client_rect()
            except Exception as e:
                pass
        
        return info

class PywinautoControl(BaseControl):
    """pywinauto控件实现"""
    
    def __init__(self, control_id: str, window: Any, config: Dict[str, Any] = None):
        super().__init__(control_id, window, config)
        self._control: Optional[BaseWrapper] = None
        self._parse_control_id(control_id)
    
    def _parse_control_id(self, control_id: str) -> None:
        """解析控件ID"""
        if isinstance(control_id, str):
            # 通过定位器查找控件
            self._control = self.window.find_element(control_id)
        else:
            # 直接使用控件对象
            self._control = control_id
    
    def click(self, button: str = "left", count: int = 1, x_offset: int = 0, y_offset: int = 0) -> bool:
        """点击控件"""
        if not self._control:
            return False
        
        try:
            if count == 1:
                if button == "left":
                    self._control.click(coords=(x_offset, y_offset))
                elif button == "right":
                    self._control.right_click(coords=(x_offset, y_offset))
                elif button == "middle":
                    # pywinauto不直接支持中键点击，使用坐标定位
                    rect = self._control.rectangle()
                    x = rect.left + x_offset
                    y = rect.top + y_offset
                    click(coords=(x, y), button="middle")
                else:
                    return False
            elif count == 2:
                self._control.double_click(coords=(x_offset, y_offset))
            else:
                return False
            
            return True
        except Exception as e:
            return False
    
    def right_click(self, x_offset: int = 0, y_offset: int = 0) -> bool:
        """右键点击控件"""
        return self.click(button="right", x_offset=x_offset, y_offset=y_offset)
    
    def double_click(self, x_offset: int = 0, y_offset: int = 0) -> bool:
        """双击控件"""
        return self.click(count=2, x_offset=x_offset, y_offset=y_offset)
    
    def hover(self, x_offset: int = 0, y_offset: int = 0, duration: float = 0) -> bool:
        """鼠标悬停在控件上"""
        if not self._control:
            return False
        
        try:
            rect = self._control.rectangle()
            x = rect.left + x_offset
            y = rect.top + y_offset
            move(coords=(x, y))
            if duration > 0:
                time.sleep(duration)
            return True
        except Exception as e:
            return False
    
    def drag_to(self, target: Any, duration: float = 1.0) -> bool:
        """将控件拖拽到目标位置"""
        if not self._control:
            return False
        
        try:
            start_rect = self._control.rectangle()
            start_x = start_rect.left + start_rect.width() // 2
            start_y = start_rect.top + start_rect.height() // 2
            
            if isinstance(target, (tuple, list)) and len(target) == 2:
                # 拖拽到坐标
                end_x, end_y = target
            else:
                # 拖拽到控件
                end_rect = target.rectangle()
                end_x = end_rect.left + end_rect.width() // 2
                end_y = end_rect.top + end_rect.height() // 2
            
            drag(start=(start_x, start_y), end=(end_x, end_y))
            return True
        except Exception as e:
            return False
    
    def type_text(self, text: str, clear_first: bool = True, slow: bool = False, interval: float = 0.05) -> bool:
        """在控件中输入文本"""
        if not self._control:
            return False
        
        try:
            if clear_first:
                self._control.set_text("")
            
            if slow:
                # 慢速输入
                for char in text:
                    self._control.type_keys(char)
                    time.sleep(interval)
            else:
                self._control.type_keys(text)
            
            return True
        except Exception as e:
            return False
    
    def clear(self) -> bool:
        """清空控件内容"""
        if not self._control:
            return False
        
        try:
            self._control.set_text("")
            return True
        except Exception as e:
            return False
    
    def get_text(self) -> Optional[str]:
        """获取控件文本"""
        if not self._control:
            return None
        
        try:
            return self._control.window_text()
        except Exception as e:
            return None
    
    def set_text(self, text: str) -> bool:
        """设置控件文本"""
        if not self._control:
            return False
        
        try:
            self._control.set_text(text)
            return True
        except Exception as e:
            return False
    
    def is_enabled(self) -> bool:
        """检查控件是否启用"""
        if not self._control:
            return False
        
        try:
            return self._control.is_enabled()
        except Exception as e:
            return False
    
    def is_visible(self) -> bool:
        """检查控件是否可见"""
        if not self._control:
            return False
        
        try:
            return self._control.is_visible()
        except Exception as e:
            return False
    
    def is_selected(self) -> bool:
        """检查控件是否被选中"""
        if not self._control:
            return False
        
        try:
            return self._control.is_selected()
        except Exception as e:
            return False
    
    def select(self) -> bool:
        """选中控件"""
        if not self._control:
            return False
        
        try:
            if hasattr(self._control, "select"):
                self._control.select()
            else:
                self.click()
            return True
        except Exception as e:
            return False
    
    def deselect(self) -> bool:
        """取消选中控件"""
        if not self._control:
            return False
        
        try:
            if hasattr(self._control, "deselect"):
                self._control.deselect()
            else:
                self.click()
            return True
        except Exception as e:
            return False
    
    def get_rect(self) -> Optional[Tuple[int, int, int, int]]:
        """获取控件矩形区域"""
        if not self._control:
            return None
        
        try:
            rect = self._control.rectangle()
            return (rect.left, rect.top, rect.width(), rect.height())
        except Exception as e:
            return None
    
    def get_name(self) -> Optional[str]:
        """获取控件名称"""
        if not self._control:
            return None
        
        try:
            return self._control.window_text()
        except Exception as e:
            return None
    
    def get_class_name(self) -> Optional[str]:
        """获取控件类名"""
        if not self._control:
            return None
        
        try:
            return self._control.class_name()
        except Exception as e:
            return None
    
    def get_automation_id(self) -> Optional[str]:
        """获取控件自动化ID"""
        if not self._control:
            return None
        
        try:
            if hasattr(self._control, "automation_id"):
                return self._control.automation_id()
            elif hasattr(self._control, "get_properties"):
                props = self._control.get_properties()
                return props.get("automation_id")
            return None
        except Exception as e:
            return None
    
    def get_control_type(self) -> Optional[str]:
        """获取控件类型"""
        if not self._control:
            return None
        
        try:
            if hasattr(self._control, "control_type"):
                return self._control.control_type()
            elif hasattr(self._control, "get_properties"):
                props = self._control.get_properties()
                return props.get("control_type")
            return None
        except Exception as e:
            return None
    
    def get_attribute(self, name: str) -> Optional[Any]:
        """获取控件属性"""
        if not self._control:
            return None
        
        try:
            if hasattr(self._control, name):
                attr = getattr(self._control, name)
                if callable(attr):
                    return attr()
                return attr
            elif hasattr(self._control, "get_properties"):
                props = self._control.get_properties()
                return props.get(name)
            return None
        except Exception as e:
            return None
    
    def set_attribute(self, name: str, value: Any) -> bool:
        """设置控件属性"""
        if not self._control:
            return False
        
        try:
            if hasattr(self._control, name):
                attr = getattr(self._control, name)
                if callable(attr):
                    attr(value)
                else:
                    setattr(self._control, name, value)
                return True
            return False
        except Exception as e:
            return False
    
    def focus(self) -> bool:
        """将焦点设置到控件上"""
        if not self._control:
            return False
        
        try:
            self._control.set_focus()
            return True
        except Exception as e:
            return False
    
    def has_focus(self) -> bool:
        """检查控件是否有焦点"""
        if not self._control:
            return False
        
        try:
            return self._control.has_focus()
        except Exception as e:
            return False
    
    def find_element(self, locator: str, timeout: float = None) -> Any:
        """在控件中查找子控件"""
        if not self._control:
            return None
        
        if timeout is None:
            timeout = local_config.get("timeout", 10)
        
        try:
            from .pywinauto_backend import PywinautoWindow
            window = PywinautoWindow("", self.window.application)
            window._window = self._control
            return window.find_element(locator, timeout)
        except Exception as e:
            return None
    
    def find_elements(self, locator: str, timeout: float = None) -> List[Any]:
        """在控件中查找所有匹配的子控件"""
        if not self._control:
            return []
        
        if timeout is None:
            timeout = local_config.get("timeout", 10)
        
        try:
            from .pywinauto_backend import PywinautoWindow
            window = PywinautoWindow("", self.window.application)
            window._window = self._control
            return window.find_elements(locator, timeout)
        except Exception as e:
            return []
    
    def get_parent(self) -> Any:
        """获取父控件"""
        if not self._control:
            return None
        
        try:
            return self._control.parent()
        except Exception as e:
            return None
    
    def get_children(self) -> List[Any]:
        """获取所有子控件"""
        if not self._control:
            return []
        
        try:
            return self._control.children()
        except Exception as e:
            return []
    
    def get_control_info(self) -> Dict[str, Any]:
        """获取控件信息"""
        info = {
            "control_id": self.control_id,
            "is_enabled": self.is_enabled(),
            "is_visible": self.is_visible(),
            "is_selected": self.is_selected()
        }
        
        if self._control:
            try:
                info["name"] = self.get_name()
                info["class_name"] = self.get_class_name()
                info["automation_id"] = self.get_automation_id()
                info["control_type"] = self.get_control_type()
                info["rect"] = self.get_rect()
            except Exception as e:
                pass
        
        return info

class PywinautoOperation(BaseOperation):
    """pywinauto操作实现"""
    
    def mouse_click(self, x: int, y: int, button: str = "left", count: int = 1) -> bool:
        """鼠标点击指定坐标"""
        try:
            if button == "left":
                if count == 1:
                    click(coords=(x, y), button="left")
                elif count == 2:
                    double_click(coords=(x, y))
                else:
                    return False
            elif button == "right":
                right_click(coords=(x, y))
            elif button == "middle":
                click(coords=(x, y), button="middle")
            else:
                return False
            return True
        except Exception as e:
            return False
    
    def mouse_move(self, x: int, y: int, duration: float = 0) -> bool:
        """鼠标移动到指定坐标"""
        try:
            move(coords=(x, y))
            if duration > 0:
                time.sleep(duration)
            return True
        except Exception as e:
            return False
    
    def mouse_drag(self, start_x: int, start_y: int, end_x: int, end_y: int, duration: float = 1.0) -> bool:
        """鼠标拖拽"""
        try:
            drag(start=(start_x, start_y), end=(end_x, end_y))
            return True
        except Exception as e:
            return False
    
    def mouse_wheel(self, x: int, y: int, direction: str = "up", steps: int = 1) -> bool:
        """鼠标滚轮滚动"""
        try:
            # pywinauto的mouse模块没有直接的滚轮方法，使用send_keys模拟
            # 这是一个临时实现，后续可以优化
            move(coords=(x, y))
            wheel_key = "{VK_UP}" if direction == "up" else "{VK_DOWN}"
            send_keys(wheel_key * steps)
            return True
        except Exception as e:
            return False
    
    def mouse_hover(self, x: int, y: int, duration: float = 0) -> bool:
        """鼠标悬停在指定坐标"""
        try:
            move(coords=(x, y))
            if duration > 0:
                time.sleep(duration)
            return True
        except Exception as e:
            return False
    
    def get_mouse_position(self) -> Tuple[int, int]:
        """获取当前鼠标位置"""
        try:
            from pywinauto.mouse import get_position
            return get_position()
        except Exception as e:
            return (0, 0)
    
    def press_key(self, key: str) -> bool:
        """按下并释放指定按键"""
        try:
            send_keys(f"{{{key}}}")
            return True
        except Exception as e:
            return False
    
    def press_keys(self, keys: str) -> bool:
        """按下并释放组合键"""
        try:
            # 转换组合键格式，如Ctrl+C -> ^c
            keys = keys.replace("Ctrl+", "^")
            keys = keys.replace("Alt+", "%")
            keys = keys.replace("Shift+", "+")
            send_keys(keys)
            return True
        except Exception as e:
            return False
    
    def key_down(self, key: str) -> bool:
        """按下指定按键（不释放）"""
        try:
            press(key)
            return True
        except Exception as e:
            return False
    
    def key_up(self, key: str) -> bool:
        """释放指定按键"""
        try:
            release(key)
            return True
        except Exception as e:
            return False
    
    def type_text(self, text: str, interval: float = 0.05) -> bool:
        """输入文本"""
        try:
            send_keys(text, pause=interval)
            return True
        except Exception as e:
            return False
    
    def capture_screenshot(self, filename: Optional[str] = None, x: int = 0, y: int = 0, width: int = 0, height: int = 0) -> Optional[str]:
        """捕获屏幕截图"""
        try:
            from PIL import ImageGrab
            import os
            
            if x == 0 and y == 0 and width == 0 and height == 0:
                # 全屏截图
                image = ImageGrab.grab()
            else:
                # 区域截图
                image = ImageGrab.grab(bbox=(x, y, x + width, y + height))
            
            if filename is None:
                # 自动生成文件名
                if not os.path.exists(local_config.get("screenshot_path", "./screenshots/")):
                    os.makedirs(local_config.get("screenshot_path", "./screenshots/"))
                filename = f"{local_config.get('screenshot_path', './screenshots/')}screenshot_{int(time.time())}.{local_config.get('screenshot_format', 'png')}"
            
            # 保存截图
            image_format = local_config.get("screenshot_format", "png").upper()
            if image_format == "JPG":
                image.save(filename, "JPEG", quality=local_config.get("screenshot_quality", 90))
            else:
                image.save(filename, image_format)
            
            return filename
        except Exception as e:
            return None
    
    def capture_window_screenshot(self, window: Any, filename: Optional[str] = None) -> Optional[str]:
        """捕获窗口截图"""
        try:
            if not window:
                return None
            
            # 使用pywinauto的截图功能
            image = window.capture_as_image()
            
            if filename is None:
                # 自动生成文件名
                import os
                if not os.path.exists(local_config.get("screenshot_path", "./screenshots/")):
                    os.makedirs(local_config.get("screenshot_path", "./screenshots/"))
                filename = f"{local_config.get('screenshot_path', './screenshots/')}window_screenshot_{int(time.time())}.{local_config.get('screenshot_format', 'png')}"
            
            # 保存截图
            image_format = local_config.get("screenshot_format", "png").upper()
            if image_format == "JPG":
                image.save(filename, "JPEG", quality=local_config.get("screenshot_quality", 90))
            else:
                image.save(filename, image_format)
            
            return filename
        except Exception as e:
            return None
    
    def capture_element_screenshot(self, element: Any, filename: Optional[str] = None) -> Optional[str]:
        """捕获控件截图"""
        try:
            if not element:
                return None
            
            # 使用pywinauto的截图功能
            image = element.capture_as_image()
            
            if filename is None:
                # 自动生成文件名
                import os
                if not os.path.exists(local_config.get("screenshot_path", "./screenshots/")):
                    os.makedirs(local_config.get("screenshot_path", "./screenshots/"))
                filename = f"{local_config.get('screenshot_path', './screenshots/')}element_screenshot_{int(time.time())}.{local_config.get('screenshot_format', 'png')}"
            
            # 保存截图
            image_format = local_config.get("screenshot_format", "png").upper()
            if image_format == "JPG":
                image.save(filename, "JPEG", quality=local_config.get("screenshot_quality", 90))
            else:
                image.save(filename, image_format)
            
            return filename
        except Exception as e:
            return None
    
    def wait(self, seconds: float) -> None:
        """等待指定时长"""
        time.sleep(seconds)
    
    def wait_until(self, condition_func: callable, timeout: float = 10.0, interval: float = 0.5) -> bool:
        """等待直到条件满足或超时"""
        start_time = time.time()
        while time.time() - start_time < timeout:
            if condition_func():
                return True
            time.sleep(interval)
        return False
    
    def get_screen_size(self) -> Tuple[int, int]:
        """获取屏幕尺寸"""
        try:
            from pywinauto import Desktop
            desktop = Desktop(backend="uia")
            return (desktop.rectangle().width(), desktop.rectangle().height())
        except Exception as e:
            return (1920, 1080)  # 默认值
    
    def get_dpi_scale(self) -> float:
        """获取屏幕DPI缩放比例"""
        try:
            import ctypes
            user32 = ctypes.windll.user32
            user32.SetProcessDPIAware()
            dpi = user32.GetDpiForSystem()
            return dpi / 96.0
        except Exception as e:
            return 1.0  # 默认值
    
    def adapt_coordinate(self, x: int, y: int) -> Tuple[int, int]:
        """适配坐标到当前DPI"""
        dpi_scale = self.get_dpi_scale()
        return (int(x * dpi_scale), int(y * dpi_scale))
    
    def adapt_size(self, width: int, height: int) -> Tuple[int, int]:
        """适配尺寸到当前DPI"""
        dpi_scale = self.get_dpi_scale()
        return (int(width * dpi_scale), int(height * dpi_scale))

class PywinautoBackend(Backend):
    """pywinauto后端"""
    
    def create_application(self, app_id: str, config: Dict[str, Any] = None) -> Any:
        """创建应用对象"""
        return PywinautoApplication(app_id, config)
    
    def create_window(self, window_id: str, application: Any, config: Dict[str, Any] = None) -> Any:
        """创建窗口对象"""
        return PywinautoWindow(window_id, application, config)
    
    def create_control(self, control_id: str, window: Any, config: Dict[str, Any] = None) -> Any:
        """创建控件对象"""
        return PywinautoControl(control_id, window, config)
    
    def create_operation(self) -> Any:
        """创建操作对象"""
        return PywinautoOperation()

# 注册pywinauto后端
from .backend_factory import backend_factory
backend_factory.register_backend("pywinauto", PywinautoBackend())
