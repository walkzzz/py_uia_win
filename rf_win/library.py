# rf-win库主入口文件
# 实现Robot Framework关键字，管理应用、窗口、控件对象

import os
import sys
import time
from typing import Any, Dict, List, Optional
from robot.api import logger
from robot.libraries.BuiltIn import BuiltIn

from .config.global_config import global_config, CONFIG_KEY_MAP
from .config.local_config import local_config
from .backend.backend_factory import backend_factory
from .core.base_application import BaseApplication
from .core.base_window import BaseWindow
from .core.base_control import BaseControl
from .core.base_operation import BaseOperation

class RFWinLibrary:
    """Windows桌面自动化Robot Framework库
    
    该库封装了pywinauto和UIAutomation的功能，提供一套统一的关键字，用于自动化Windows桌面应用。
    
    支持的功能包括：
    - 应用管理（启动、关闭、检查状态）
    - 窗口管理（定位、激活、调整大小）
    - 控件交互（点击、输入文本、获取属性）
    - 鼠标键盘操作
    - 截图功能
    - 数据输入输出
    """
    
    # 关键字文档格式
    ROBOT_LIBRARY_DOC_FORMAT = "REST"
    ROBOT_LIBRARY_VERSION = "1.0.0"
    ROBOT_LIBRARY_SCOPE = "GLOBAL"
    
    def __init__(self, **kwargs: Any):
        """初始化库
        
        Args:
            **kwargs: 配置参数，用于覆盖默认配置
        """
        # 初始化配置
        self._init_config(**kwargs)
        
        # 对象管理器，用于存储应用、窗口、控件对象
        self._applications: Dict[str, BaseApplication] = {}
        self._windows: Dict[str, BaseWindow] = {}
        self._controls: Dict[str, BaseControl] = {}
        
        # 操作对象
        self._operation: Optional[BaseOperation] = None
        
        # 初始化操作对象
        self._init_operation()
        
        # 初始化日志
        self._init_logger()
        
        # 注册关键字
        self._register_keywords()
    
    def _init_config(self, **kwargs: Any) -> None:
        """初始化配置
        
        优先级：kwargs > Robot Framework变量 > 环境变量 > 默认配置
        
        Args:
            **kwargs: 初始化参数
        """
        builtin = BuiltIn()
        
        # 从环境变量加载配置
        for env_key, config_key in CONFIG_KEY_MAP.items():
            if env_key in os.environ:
                try:
                    value = os.environ[env_key]
                    # 获取当前配置值的类型，用于正确转换
                    current_value = getattr(global_config, config_key)
                    expected_type = type(current_value)
                    
                    # 转换类型
                    if expected_type is int:
                        value = int(value)  # type: ignore[assignment]
                    elif expected_type is float:
                        value = float(value)  # type: ignore[assignment]
                    elif expected_type is bool:
                        value = value.lower() in ["true", "1", "yes"]  # type: ignore[assignment]
                    global_config.update(**{config_key: value})
                except Exception as e:
                    logger.warn(f"Failed to load config from env {env_key}: {e}")
        
        # 从Robot Framework变量加载配置
        for env_key, config_key in CONFIG_KEY_MAP.items():
            try:
                value = builtin.get_variable_value(f"${{{env_key}}}")
                if value is not None:
                    # 获取当前配置值的类型，用于正确转换
                    current_value = getattr(global_config, config_key)
                    expected_type = type(current_value)
                    
                    # 转换类型
                    if isinstance(value, str):
                        if expected_type is int:
                            value = int(value)  # type: ignore[assignment]
                        elif expected_type is float:
                            value = float(value)  # type: ignore[assignment]
                        elif expected_type is bool:
                            value = value.lower() in ["true", "1", "yes"]  # type: ignore[assignment]
                    else:
                        # 已经是其他类型，直接转换为预期类型
                        value = expected_type(value)  # type: ignore[assignment]
                    global_config.update(**{config_key: value})
            except Exception as e:
                logger.warn(f"Failed to load config from RF variable {env_key}: {e}")
        
        # 从初始化参数加载配置
        global_config.update(**kwargs)
        
        # 设置默认后端
        backend_factory.set_default_backend(global_config.default_backend)
        
        logger.info(f"RFWinLibrary initialized with config: {{'timeout': {global_config.timeout}, 'retry': {global_config.retry}, 'default_backend': '{global_config.default_backend}', 'pywinauto_backend': '{global_config.pywinauto_backend}', 'auto_screenshot_on_fail': {global_config.auto_screenshot_on_fail}, 'high_dpi_adapter': {global_config.high_dpi_adapter}}}")
    
    def _init_operation(self) -> None:
        """初始化操作对象"""
        self._operation = backend_factory.get_backend().create_operation()
    
    def _init_logger(self) -> None:
        """初始化日志"""
        # 确保日志目录存在
        log_dir = os.path.dirname(global_config.log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        # 配置日志级别
        logger.set_level(global_config.log_level.upper())
    
    def _register_keywords(self) -> None:
        """注册关键字"""
        # 导入关键字模块
        from .keywords.application_management import ApplicationManagementKeywords
        from .keywords.window_management import WindowManagementKeywords
        from .keywords.control_operations import ControlOperationsKeywords
        from .keywords.keyboard_mouse import KeyboardMouseKeywords
        from .keywords.screenshot import ScreenshotKeywords
        
        # 初始化关键字实例
        self._application_keywords = ApplicationManagementKeywords(self)
        self._window_keywords = WindowManagementKeywords(self)
        self._control_keywords = ControlOperationsKeywords(self)
        self._keyboard_mouse_keywords = KeyboardMouseKeywords(self)
        self._screenshot_keywords = ScreenshotKeywords(self)
        
        # 动态绑定关键字方法到主类
        # 应用管理关键字
        self.start_application = self._application_keywords.start_application
        self.attach_to_application = self._application_keywords.attach_to_application
        self.close_application = self._application_keywords.close_application
        self.kill_application = self._application_keywords.kill_application
        self.check_application_running = self._application_keywords.check_application_running
        self.get_application_process_id = self._application_keywords.get_application_process_id
        self.wait_for_application_main_window = self._application_keywords.wait_for_application_main_window
        
        # 窗口管理关键字
        self.get_main_window = self._window_keywords.get_main_window
        self.locate_window = self._window_keywords.locate_window
        self.activate_window = self._window_keywords.activate_window
        self.close_window = self._window_keywords.close_window
        self.maximize_window = self._window_keywords.maximize_window
        self.minimize_window = self._window_keywords.minimize_window
        self.restore_window = self._window_keywords.restore_window
        self.resize_window = self._window_keywords.resize_window
        self.move_window = self._window_keywords.move_window
        self.get_window_title = self._window_keywords.get_window_title
        self.get_window_rect = self._window_keywords.get_window_rect
        self.wait_for_window_close = self._window_keywords.wait_for_window_close
        self.is_window_active = self._window_keywords.is_window_active
        self.is_window_visible = self._window_keywords.is_window_visible
        self.is_window_closed = self._window_keywords.is_window_closed
        
        # 控件操作关键字
        self.find_element = self._control_keywords.find_element
        self.click_element = self._control_keywords.click_element
        self.right_click_element = self._control_keywords.right_click_element
        self.double_click_element = self._control_keywords.double_click_element
        self.type_text = self._control_keywords.type_text
        self.clear_element_text = self._control_keywords.clear_element_text
        self.get_element_text = self._control_keywords.get_element_text
        self.set_element_text = self._control_keywords.set_element_text
        self.select_element = self._control_keywords.select_element
        self.deselect_element = self._control_keywords.deselect_element
        self.is_element_selected = self._control_keywords.is_element_selected
        self.is_element_enabled = self._control_keywords.is_element_enabled
        self.is_element_visible = self._control_keywords.is_element_visible
        self.get_element_attribute = self._control_keywords.get_element_attribute
        self.set_element_attribute = self._control_keywords.set_element_attribute
        self.hover_element = self._control_keywords.hover_element
        self.drag_element_to = self._control_keywords.drag_element_to
        
        # 鼠标键盘关键字
        self.mouse_click = self._keyboard_mouse_keywords.mouse_click
        self.mouse_move = self._keyboard_mouse_keywords.mouse_move
        self.mouse_drag = self._keyboard_mouse_keywords.mouse_drag
        self.mouse_wheel = self._keyboard_mouse_keywords.mouse_wheel
        self.mouse_hover = self._keyboard_mouse_keywords.mouse_hover
        self.get_mouse_position = self._keyboard_mouse_keywords.get_mouse_position
        self.press_key = self._keyboard_mouse_keywords.press_key
        self.press_keys = self._keyboard_mouse_keywords.press_keys
        self.key_down = self._keyboard_mouse_keywords.key_down
        self.key_up = self._keyboard_mouse_keywords.key_up
        self.type_text_with_keyboard = self._keyboard_mouse_keywords.type_text_with_keyboard
        
        # 截图关键字
        self.capture_screenshot = self._screenshot_keywords.capture_screenshot
        self.capture_window_screenshot = self._screenshot_keywords.capture_window_screenshot
        self.capture_element_screenshot = self._screenshot_keywords.capture_element_screenshot
    
    def _get_application(self, app_id: str) -> Optional[BaseApplication]:
        """获取应用对象
        
        Args:
            app_id: 应用ID
        
        Returns:
            应用对象，如果不存在则返回None
        """
        return self._applications.get(app_id)
    
    def _add_application(self, app_id: str, app: BaseApplication) -> None:
        """添加应用对象
        
        Args:
            app_id: 应用ID
            app: 应用对象
        """
        self._applications[app_id] = app
    
    def _remove_application(self, app_id: str) -> None:
        """移除应用对象
        
        Args:
            app_id: 应用ID
        """
        if app_id in self._applications:
            del self._applications[app_id]
    
    def _get_window(self, window_id: str) -> Optional[BaseWindow]:
        """获取窗口对象
        
        Args:
            window_id: 窗口ID
        
        Returns:
            窗口对象，如果不存在则返回None
        """
        return self._windows.get(window_id)
    
    def _add_window(self, window_id: str, window: BaseWindow) -> None:
        """添加窗口对象
        
        Args:
            window_id: 窗口ID
            window: 窗口对象
        """
        self._windows[window_id] = window
    
    def _remove_window(self, window_id: str) -> None:
        """移除窗口对象
        
        Args:
            window_id: 窗口ID
        """
        if window_id in self._windows:
            del self._windows[window_id]
    
    def _get_control(self, control_id: str) -> Optional[BaseControl]:
        """获取控件对象
        
        Args:
            control_id: 控件ID
        
        Returns:
            控件对象，如果不存在则返回None
        """
        return self._controls.get(control_id)
    
    def _add_control(self, control_id: str, control: BaseControl) -> None:
        """添加控件对象
        
        Args:
            control_id: 控件ID
            control: 控件对象
        """
        self._controls[control_id] = control
    
    def _remove_control(self, control_id: str) -> None:
        """移除控件对象
        
        Args:
            control_id: 控件ID
        """
        if control_id in self._controls:
            del self._controls[control_id]
    
    def _get_backend(self, backend_name: Optional[str] = None) -> Any:
        """获取后端对象
        
        Args:
            backend_name: 后端名称，默认使用全局配置
        
        Returns:
            后端对象
        """
        return backend_factory.get_backend(backend_name)
    
    # ===================
    # 配置管理关键字
    # ===================
    
    def set_global_config(self, key: str, value: Any) -> None:
        """设置全局配置
        
        Args:
            key: 配置项名称
            value: 配置值
        
        Example:
            | Set Global Config | timeout | 20 |
            | Set Global Config | default_backend | pywinauto |
        """
        if hasattr(global_config, key):
            setattr(global_config, key, value)
            logger.info(f"Set global config: {key} = {value}")
        else:
            raise ValueError(f"Unknown config key: {key}")
    
    def get_global_config(self, key: str) -> Any:
        """获取全局配置
        
        Args:
            key: 配置项名称
        
        Returns:
            配置值
        
        Example:
            | ${timeout} | Get Global Config | timeout |
        """
        if hasattr(global_config, key):
            return getattr(global_config, key)
        else:
            raise ValueError(f"Unknown config key: {key}")
    
    def set_backend(self, backend_name: str) -> None:
        """设置默认后端
        
        Args:
            backend_name: 后端名称，可选值：auto, pywinauto, uiautomation
        
        Example:
            | Set Backend | pywinauto |
        """
        backend_factory.set_default_backend(backend_name)
        logger.info(f"Set default backend to: {backend_name}")
    
    def get_available_backends(self) -> List[str]:
        """获取可用的后端列表
        
        Returns:
            后端名称列表
        
        Example:
            | ${backends} | Get Available Backends |
        """
        return backend_factory.get_available_backends()
    