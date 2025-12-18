# 版本适配器
# 自动适配不同版本的依赖库，解决依赖冲突问题

import sys
from typing import Any, Optional

# pywinauto版本适配
try:
    from pywinauto import Application as PywinautoApp
    from pywinauto.findwindows import find_window, find_windows, ElementNotFoundError
    from pywinauto.keyboard import send_keys, press, release
    from pywinauto.mouse import click, double_click, right_click, move, drag
    from pywinauto.base_wrapper import BaseWrapper
    from pywinauto.controls.uiawrapper import UIAWrapper
    from pywinauto.controls.hwndwrapper import HwndWrapper
    PYWINAUTO_AVAILABLE = True
    PYWINAUTO_VERSION = sys.modules['pywinauto'].__version__
except ImportError:
    PYWINAUTO_AVAILABLE = False
    PYWINAUTO_VERSION = None

# UIAutomation版本适配
try:
    import uiautomation as auto
    UIAUTOMATION_AVAILABLE = True
    # 尝试获取版本，如果__version__属性不存在则使用默认值
    try:
        UIAUTOMATION_VERSION = auto.__version__
    except AttributeError:
        # uiautomation 2.x版本可能没有__version__属性，使用默认值
        UIAUTOMATION_VERSION = "2.0.0"
except ImportError:
    UIAUTOMATION_AVAILABLE = False
    UIAUTOMATION_VERSION = None

class VersionAdapter:
    """版本适配器，提供统一的接口适配不同版本的依赖库"""
    
    @staticmethod
    def is_pywinauto_available() -> bool:
        """检查pywinauto是否可用"""
        return PYWINAUTO_AVAILABLE
    
    @staticmethod
    def get_pywinauto_version() -> Optional[str]:
        """获取pywinauto版本"""
        return PYWINAUTO_VERSION
    
    @staticmethod
    def is_uiautomation_available() -> bool:
        """检查UIAutomation是否可用"""
        return UIAUTOMATION_AVAILABLE
    
    @staticmethod
    def get_uiautomation_version() -> Optional[str]:
        """获取UIAutomation版本"""
        return UIAUTOMATION_VERSION
    
    @staticmethod
    def create_pywinauto_app(backend: str = "uia") -> Any:
        """创建pywinauto应用对象
        
        Args:
            backend: 后端类型（win32, uia）
        
        Returns:
            pywinauto应用对象
        """
        if not PYWINAUTO_AVAILABLE:
            raise ImportError("pywinauto is not installed")
        
        return PywinautoApp(backend=backend)
    
    @staticmethod
    def get_uiautomation_control_from_point(x: int, y: int) -> Any:
        """从坐标获取UIAutomation控件
        
        Args:
            x: X坐标
            y: Y坐标
        
        Returns:
            UIAutomation控件对象
        """
        if not UIAUTOMATION_AVAILABLE:
            raise ImportError("UIAutomation is not installed")
        
        return auto.ControlFromPoint(x, y)

# 创建版本适配器实例
version_adapter = VersionAdapter()
