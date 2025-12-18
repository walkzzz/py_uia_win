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
    
    配置项：
    - RF_WIN_TIMEOUT: 超时时间（秒），默认10
    - RF_WIN_RETRY: 重试次数，默认1
    - RF_WIN_RETRY_INTERVAL: 重试间隔（秒），默认1.0
    - RF_WIN_DEFAULT_BACKEND: 默认后端，默认auto
    - RF_WIN_PYWINAUTO_BACKEND: pywinauto后端类型，默认uia
    - RF_WIN_SCREENSHOT_PATH: 截图保存路径，默认./screenshots/
    - RF_WIN_SCREENSHOT_FORMAT: 截图格式，默认png
    - RF_WIN_SCREENSHOT_QUALITY: 截图质量（0-100），默认90
    - RF_WIN_LOG_LEVEL: 日志级别，默认info
    - RF_WIN_LOG_FILE: 日志文件路径，默认./logs/rf_win.log
    - RF_WIN_AUTO_SCREENSHOT: 自动截图开关，默认True
    - RF_WIN_HIGH_DPI: 高DPI适配开关，默认True
    - RF_WIN_CACHE_EXPIRE: 缓存过期时间（秒），默认10
    - RF_WIN_MAX_CACHE: 最大缓存数量，默认100
    - RF_WIN_LANGUAGE: 语言，默认zh-CN
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
        # 关键字注册由Robot Framework自动处理，这里仅做预留
        pass
    
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
    
    def _get_backend(self, backend_name: str = None) -> Any:
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
    
    # ===================
    # 应用管理关键字
    # ===================
    
    def start_application(self, path: str, app_id: str = None, args: str = None, admin: bool = False, background: bool = False, backend: str = None) -> str:
        """启动应用
        
        Args:
            path: 应用路径
            app_id: 应用ID，用于后续操作，如果为None则自动生成
            args: 启动参数
            admin: 是否以管理员权限运行
            background: 是否在后台运行
            backend: 使用的后端，默认使用全局配置
        
        Returns:
            应用ID
        
        Example:
            | ${app_id} | Start Application | C:/Windows/System32/notepad.exe | app_id=notepad |
            | Start Application | C:/Program Files/MyApp/MyApp.exe | args=--debug | admin=True |
        """
        if app_id is None:
            app_id = f"app_{int(time.time())}"
        
        backend_instance = self._get_backend(backend)
        app = backend_instance.create_application(app_id)
        
        if app.start(path, args, admin, background):
            self._add_application(app_id, app)
            logger.info(f"Started application: {path} with app_id: {app_id}")
            return app_id
        else:
            raise RuntimeError(f"Failed to start application: {path}")
    
    def attach_to_application(self, identifier: Any, app_id: str = None, backend: str = None) -> str:
        """附加到已运行的应用
        
        Args:
            identifier: 应用标识符（PID、进程名、窗口标题）
            app_id: 应用ID，用于后续操作，如果为None则自动生成
            backend: 使用的后端，默认使用全局配置
        
        Returns:
            应用ID
        
        Example:
            | ${app_id} | Attach To Application | notepad.exe | app_id=notepad |
            | ${app_id} | Attach To Application | 1234 | app_id=myapp |
        """
        if app_id is None:
            app_id = f"app_{int(time.time())}"
        
        backend_instance = self._get_backend(backend)
        app = backend_instance.create_application(app_id)
        
        if app.attach(identifier):
            self._add_application(app_id, app)
            logger.info(f"Attached to application: {identifier} with app_id: {app_id}")
            return app_id
        else:
            raise RuntimeError(f"Failed to attach to application: {identifier}")
    
    def close_application(self, app_id: str, timeout: float = None) -> bool:
        """优雅关闭应用
        
        Args:
            app_id: 应用ID
            timeout: 超时时间（秒），默认使用全局配置
        
        Returns:
            是否关闭成功
        
        Example:
            | Close Application | notepad |
            | Close Application | myapp | timeout=20 |
        """
        app = self._get_application(app_id)
        if not app:
            raise ValueError(f"Application not found: {app_id}")
        
        if timeout is None:
            timeout = global_config.timeout
        
        result = app.close(timeout)
        if result:
            self._remove_application(app_id)
            logger.info(f"Closed application: {app_id}")
        else:
            logger.warn(f"Failed to close application: {app_id}")
        
        return result
    
    def kill_application(self, app_id: str) -> bool:
        """强制关闭应用
        
        Args:
            app_id: 应用ID
        
        Returns:
            是否关闭成功
        
        Example:
            | Kill Application | notepad |
        """
        app = self._get_application(app_id)
        if not app:
            raise ValueError(f"Application not found: {app_id}")
        
        result = app.kill()
        if result:
            self._remove_application(app_id)
            logger.info(f"Killed application: {app_id}")
        else:
            logger.warn(f"Failed to kill application: {app_id}")
        
        return result
    
    def check_application_running(self, app_id: str) -> bool:
        """检查应用是否正在运行
        
        Args:
            app_id: 应用ID
        
        Returns:
            是否正在运行
        
        Example:
            | ${is_running} | Check Application Running | notepad |
        """
        app = self._get_application(app_id)
        if not app:
            return False
        
        result = app.is_running()
        logger.info(f"Application {app_id} is running: {result}")
        return result
    
    def get_application_process_id(self, app_id: str) -> Optional[int]:
        """获取应用进程ID
        
        Args:
            app_id: 应用ID
        
        Returns:
            进程ID，如果应用未运行则返回None
        
        Example:
            | ${pid} | Get Application Process Id | notepad |
        """
        app = self._get_application(app_id)
        if not app:
            raise ValueError(f"Application not found: {app_id}")
        
        return app.get_process_id()
    
    def wait_for_application_main_window(self, app_id: str, timeout: float = None) -> bool:
        """等待应用主窗口出现
        
        Args:
            app_id: 应用ID
            timeout: 超时时间（秒），默认使用全局配置
        
        Returns:
            是否找到主窗口
        
        Example:
            | Wait For Application Main Window | notepad | timeout=15 |
        """
        app = self._get_application(app_id)
        if not app:
            raise ValueError(f"Application not found: {app_id}")
        
        if timeout is None:
            timeout = global_config.timeout
        
        result = app.wait_for_main_window(timeout)
        logger.info(f"Wait for application {app_id} main window: {result}")
        return result
    
    # ===================
    # 窗口管理关键字
    # ===================
    
    def get_main_window(self, app_id: str, window_id: str = None) -> str:
        """获取应用的主窗口
        
        Args:
            app_id: 应用ID
            window_id: 窗口ID，用于后续操作，如果为None则自动生成
        
        Returns:
            窗口ID
        
        Example:
            | ${window_id} | Get Main Window | notepad | window_id=notepad_window |
        """
        app = self._get_application(app_id)
        if not app:
            raise ValueError(f"Application not found: {app_id}")
        
        main_window = app.get_main_window()
        if not main_window:
            raise RuntimeError(f"Failed to get main window for application: {app_id}")
        
        if window_id is None:
            window_id = f"window_{int(time.time())}"
        
        backend_instance = self._get_backend()
        window = backend_instance.create_window(main_window, app)
        self._add_window(window_id, window)
        
        logger.info(f"Got main window for application {app_id}, window_id: {window_id}")
        return window_id
    
    def locate_window(self, app_id: str, window_identifier: Any, window_id: str = None) -> str:
        """定位应用中的窗口
        
        Args:
            app_id: 应用ID
            window_identifier: 窗口标识符（标题、类名、句柄）
            window_id: 窗口ID，用于后续操作，如果为None则自动生成
        
        Returns:
            窗口ID
        
        Example:
            | ${window_id} | Locate Window | notepad | 记事本 | window_id=notepad_window |
            | ${window_id} | Locate Window | myapp | class=MyAppWindow | window_id=app_window |
        """
        app = self._get_application(app_id)
        if not app:
            raise ValueError(f"Application not found: {app_id}")
        
        if window_id is None:
            window_id = f"window_{int(time.time())}"
        
        backend_instance = self._get_backend()
        window = backend_instance.create_window(window_identifier, app)
        self._add_window(window_id, window)
        
        logger.info(f"Located window for application {app_id}, identifier: {window_identifier}, window_id: {window_id}")
        return window_id
    
    def activate_window(self, window_id: str) -> bool:
        """激活窗口
        
        Args:
            window_id: 窗口ID
        
        Returns:
            是否激活成功
        
        Example:
            | Activate Window | notepad_window |
        """
        window = self._get_window(window_id)
        if not window:
            raise ValueError(f"Window not found: {window_id}")
        
        result = window.activate()
        logger.info(f"Activate window {window_id}: {result}")
        return result
    
    def close_window(self, window_id: str, timeout: float = None) -> bool:
        """关闭窗口
        
        Args:
            window_id: 窗口ID
            timeout: 超时时间（秒），默认使用全局配置
        
        Returns:
            是否关闭成功
        
        Example:
            | Close Window | notepad_window |
            | Close Window | app_window | timeout=20 |
        """
        window = self._get_window(window_id)
        if not window:
            raise ValueError(f"Window not found: {window_id}")
        
        if timeout is None:
            timeout = global_config.timeout
        
        result = window.close(timeout)
        if result:
            self._remove_window(window_id)
            logger.info(f"Closed window: {window_id}")
        else:
            logger.warn(f"Failed to close window: {window_id}")
        
        return result
    
    def maximize_window(self, window_id: str) -> bool:
        """最大化窗口
        
        Args:
            window_id: 窗口ID
        
        Returns:
            是否成功
        
        Example:
            | Maximize Window | notepad_window |
        """
        window = self._get_window(window_id)
        if not window:
            raise ValueError(f"Window not found: {window_id}")
        
        result = window.maximize()
        logger.info(f"Maximize window {window_id}: {result}")
        return result
    
    def minimize_window(self, window_id: str) -> bool:
        """最小化窗口
        
        Args:
            window_id: 窗口ID
        
        Returns:
            是否成功
        
        Example:
            | Minimize Window | notepad_window |
        """
        window = self._get_window(window_id)
        if not window:
            raise ValueError(f"Window not found: {window_id}")
        
        result = window.minimize()
        logger.info(f"Minimize window {window_id}: {result}")
        return result
    
    def restore_window(self, window_id: str) -> bool:
        """恢复窗口（从最大化/最小化状态）
        
        Args:
            window_id: 窗口ID
        
        Returns:
            是否成功
        
        Example:
            | Restore Window | notepad_window |
        """
        window = self._get_window(window_id)
        if not window:
            raise ValueError(f"Window not found: {window_id}")
        
        result = window.restore()
        logger.info(f"Restore window {window_id}: {result}")
        return result
    
    def resize_window(self, window_id: str, width: int, height: int) -> bool:
        """调整窗口大小
        
        Args:
            window_id: 窗口ID
            width: 目标宽度（像素）
            height: 目标高度（像素）
        
        Returns:
            是否成功
        
        Example:
            | Resize Window | notepad_window | 800 | 600 |
        """
        window = self._get_window(window_id)
        if not window:
            raise ValueError(f"Window not found: {window_id}")
        
        result = window.resize(width, height)
        logger.info(f"Resize window {window_id} to {width}x{height}: {result}")
        return result
    
    def move_window(self, window_id: str, x: int, y: int) -> bool:
        """移动窗口
        
        Args:
            window_id: 窗口ID
            x: 目标X坐标（像素）
            y: 目标Y坐标（像素）
        
        Returns:
            是否成功
        
        Example:
            | Move Window | notepad_window | 100 | 100 |
        """
        window = self._get_window(window_id)
        if not window:
            raise ValueError(f"Window not found: {window_id}")
        
        result = window.move(x, y)
        logger.info(f"Move window {window_id} to ({x}, {y}): {result}")
        return result
    
    def get_window_title(self, window_id: str) -> Optional[str]:
        """获取窗口标题
        
        Args:
            window_id: 窗口ID
        
        Returns:
            窗口标题，如果窗口已关闭则返回None
        
        Example:
            | ${title} | Get Window Title | notepad_window |
        """
        window = self._get_window(window_id)
        if not window:
            raise ValueError(f"Window not found: {window_id}")
        
        return window.get_title()
    
    def get_window_rect(self, window_id: str) -> Optional[List[int]]:
        """获取窗口矩形区域
        
        Args:
            window_id: 窗口ID
        
        Returns:
            窗口矩形 [x, y, width, height]，如果窗口已关闭则返回None
        
        Example:
            | ${rect} | Get Window Rect | notepad_window |
        """
        window = self._get_window(window_id)
        if not window:
            raise ValueError(f"Window not found: {window_id}")
        
        rect = window.get_rect()
        if rect:
            return list(rect)
        return None
    
    def wait_for_window_close(self, window_id: str, timeout: float = None) -> bool:
        """等待窗口关闭
        
        Args:
            window_id: 窗口ID
            timeout: 超时时间（秒），默认使用全局配置
        
        Returns:
            窗口是否在超时内关闭
        
        Example:
            | Wait For Window Close | notepad_window | timeout=15 |
        """
        window = self._get_window(window_id)
        if not window:
            return True
        
        if timeout is None:
            timeout = global_config.timeout
        
        result = window.wait_for_close(timeout)
        if result:
            self._remove_window(window_id)
        logger.info(f"Wait for window {window_id} close: {result}")
        return result
    
    def is_window_active(self, window_id: str) -> bool:
        """检查窗口是否处于激活状态
        
        Args:
            window_id: 窗口ID
        
        Returns:
            是否激活
        
        Example:
            | ${is_active} | Is Window Active | notepad_window |
        """
        window = self._get_window(window_id)
        if not window:
            raise ValueError(f"Window not found: {window_id}")
        
        return window.is_active()
    
    def is_window_visible(self, window_id: str) -> bool:
        """检查窗口是否可见
        
        Args:
            window_id: 窗口ID
        
        Returns:
            是否可见
        
        Example:
            | ${is_visible} | Is Window Visible | notepad_window |
        """
        window = self._get_window(window_id)
        if not window:
            raise ValueError(f"Window not found: {window_id}")
        
        return window.is_visible()
    
    def is_window_closed(self, window_id: str) -> bool:
        """检查窗口是否已关闭
        
        Args:
            window_id: 窗口ID
        
        Returns:
            是否关闭
        
        Example:
            | ${is_closed} | Is Window Closed | notepad_window |
        """
        window = self._get_window(window_id)
        if not window:
            return True
        
        result = window.is_closed()
        if result:
            self._remove_window(window_id)
        return result
    
    # ===================
    # 控件交互关键字
    # ===================
    
    def find_element(self, window_id: str, locator: str, control_id: str = None) -> str:
        """查找窗口中的控件
        
        Args:
            window_id: 窗口ID
            locator: 控件定位器
                     - id=xxx: 自动化ID定位
                     - name=xxx: 名称定位
                     - class=xxx: 类名定位
                     - xpath=xxx: XPath定位
                     - 默认为标题定位
            control_id: 控件ID，用于后续操作，如果为None则自动生成
        
        Returns:
            控件ID
        
        Example:
            | ${btn_id} | Find Element | notepad_window | id=btn_login | control_id=login_button |
            | ${edit_id} | Find Element | notepad_window | name=用户名 | control_id=username_edit |
        """
        window = self._get_window(window_id)
        if not window:
            raise ValueError(f"Window not found: {window_id}")
        
        element = window.find_element(locator, global_config.timeout)
        if not element:
            raise RuntimeError(f"Failed to find element with locator: {locator} in window: {window_id}")
        
        if control_id is None:
            control_id = f"control_{int(time.time())}"
        
        backend_instance = self._get_backend()
        control = backend_instance.create_control(element, window)
        self._add_control(control_id, control)
        
        logger.info(f"Found element with locator: {locator} in window: {window_id}, control_id: {control_id}")
        return control_id
    
    def click_element(self, control_id: str, button: str = "left", count: int = 1, x_offset: int = 0, y_offset: int = 0) -> bool:
        """点击控件
        
        Args:
            control_id: 控件ID
            button: 鼠标按钮（left, right, middle），默认left
            count: 点击次数（1: 单击, 2: 双击），默认1
            x_offset: 相对控件左上角的X偏移（像素），默认0
            y_offset: 相对控件左上角的Y偏移（像素），默认0
        
        Returns:
            是否点击成功
        
        Example:
            | Click Element | login_button |
            | Click Element | menu_button | button=right |
            | Click Element | open_button | count=2 |
            | Click Element | btn | x_offset=10 | y_offset=10 |
        """
        control = self._get_control(control_id)
        if not control:
            raise ValueError(f"Control not found: {control_id}")
        
        result = control.click(button, count, x_offset, y_offset)
        logger.info(f"Click element {control_id}: button={button}, count={count}, offset=({x_offset}, {y_offset}): {result}")
        return result
    
    def right_click_element(self, control_id: str, x_offset: int = 0, y_offset: int = 0) -> bool:
        """右键点击控件
        
        Args:
            control_id: 控件ID
            x_offset: 相对控件左上角的X偏移（像素），默认0
            y_offset: 相对控件左上角的Y偏移（像素），默认0
        
        Returns:
            是否点击成功
        
        Example:
            | Right Click Element | menu_item |
        """
        return self.click_element(control_id, button="right", x_offset=x_offset, y_offset=y_offset)
    
    def double_click_element(self, control_id: str, x_offset: int = 0, y_offset: int = 0) -> bool:
        """双击控件
        
        Args:
            control_id: 控件ID
            x_offset: 相对控件左上角的X偏移（像素），默认0
            y_offset: 相对控件左上角的Y偏移（像素），默认0
        
        Returns:
            是否点击成功
        
        Example:
            | Double Click Element | file_icon |
        """
        return self.click_element(control_id, count=2, x_offset=x_offset, y_offset=y_offset)
    
    def type_text(self, control_id: str, text: str, clear_first: bool = True, slow: bool = False, interval: float = 0.05) -> bool:
        """在控件中输入文本
        
        Args:
            control_id: 控件ID
            text: 要输入的文本
            clear_first: 是否先清空控件，默认True
            slow: 是否慢速输入，默认False
            interval: 慢速输入的间隔（秒），默认0.05
        
        Returns:
            是否输入成功
        
        Example:
            | Type Text | username_edit | test_user |
            | Type Text | password_edit | 123456 | clear_first=False |
            | Type Text | search_edit | hello world | slow=True | interval=0.1 |
        """
        control = self._get_control(control_id)
        if not control:
            raise ValueError(f"Control not found: {control_id}")
        
        result = control.type_text(text, clear_first, slow, interval)
        logger.info(f"Type text into element {control_id}: {text}, clear_first={clear_first}, slow={slow}: {result}")
        return result
    
    def clear_element_text(self, control_id: str) -> bool:
        """清空控件内容
        
        Args:
            control_id: 控件ID
        
        Returns:
            是否清空成功
        
        Example:
            | Clear Element Text | username_edit |
        """
        control = self._get_control(control_id)
        if not control:
            raise ValueError(f"Control not found: {control_id}")
        
        result = control.clear()
        logger.info(f"Clear element {control_id} text: {result}")
        return result
    
    def get_element_text(self, control_id: str) -> Optional[str]:
        """获取控件文本
        
        Args:
            control_id: 控件ID
        
        Returns:
            控件文本，如果控件不可访问则返回None
        
        Example:
            | ${text} | Get Element Text | title_label |
        """
        control = self._get_control(control_id)
        if not control:
            raise ValueError(f"Control not found: {control_id}")
        
        return control.get_text()
    
    def set_element_text(self, control_id: str, text: str) -> bool:
        """设置控件文本
        
        Args:
            control_id: 控件ID
            text: 要设置的文本
        
        Returns:
            是否设置成功
        
        Example:
            | Set Element Text | username_edit | new_user |
        """
        control = self._get_control(control_id)
        if not control:
            raise ValueError(f"Control not found: {control_id}")
        
        result = control.set_text(text)
        logger.info(f"Set element {control_id} text to: {text}: {result}")
        return result
    
    def select_element(self, control_id: str) -> bool:
        """选中控件（适用于复选框、单选按钮等）
        
        Args:
            control_id: 控件ID
        
        Returns:
            是否选中成功
        
        Example:
            | Select Element | checkbox_remember |
        """
        control = self._get_control(control_id)
        if not control:
            raise ValueError(f"Control not found: {control_id}")
        
        result = control.select()
        logger.info(f"Select element {control_id}: {result}")
        return result
    
    def deselect_element(self, control_id: str) -> bool:
        """取消选中控件（适用于复选框等）
        
        Args:
            control_id: 控件ID
        
        Returns:
            是否取消选中成功
        
        Example:
            | Deselect Element | checkbox_remember |
        """
        control = self._get_control(control_id)
        if not control:
            raise ValueError(f"Control not found: {control_id}")
        
        result = control.deselect()
        logger.info(f"Deselect element {control_id}: {result}")
        return result
    
    def is_element_selected(self, control_id: str) -> bool:
        """检查控件是否被选中
        
        Args:
            control_id: 控件ID
        
        Returns:
            是否被选中
        
        Example:
            | ${is_selected} | Is Element Selected | checkbox_remember |
        """
        control = self._get_control(control_id)
        if not control:
            raise ValueError(f"Control not found: {control_id}")
        
        return control.is_selected()
    
    def is_element_enabled(self, control_id: str) -> bool:
        """检查控件是否启用
        
        Args:
            control_id: 控件ID
        
        Returns:
            是否启用
        
        Example:
            | ${is_enabled} | Is Element Enabled | btn_login |
        """
        control = self._get_control(control_id)
        if not control:
            raise ValueError(f"Control not found: {control_id}")
        
        return control.is_enabled()
    
    def is_element_visible(self, control_id: str) -> bool:
        """检查控件是否可见
        
        Args:
            control_id: 控件ID
        
        Returns:
            是否可见
        
        Example:
            | ${is_visible} | Is Element Visible | loading_panel |
        """
        control = self._get_control(control_id)
        if not control:
            raise ValueError(f"Control not found: {control_id}")
        
        return control.is_visible()
    
    def get_element_attribute(self, control_id: str, attribute: str) -> Optional[Any]:
        """获取控件属性
        
        Args:
            control_id: 控件ID
            attribute: 属性名
        
        Returns:
            属性值，如果属性不存在则返回None
        
        Example:
            | ${value} | Get Element Attribute | btn_login | enabled |
            | ${text} | Get Element Attribute | label_title | text |
        """
        control = self._get_control(control_id)
        if not control:
            raise ValueError(f"Control not found: {control_id}")
        
        return control.get_attribute(attribute)
    
    def set_element_attribute(self, control_id: str, attribute: str, value: Any) -> bool:
        """设置控件属性
        
        Args:
            control_id: 控件ID
            attribute: 属性名
            value: 属性值
        
        Returns:
            是否设置成功
        
        Example:
            | Set Element Attribute | btn_login | enabled | True |
        """
        control = self._get_control(control_id)
        if not control:
            raise ValueError(f"Control not found: {control_id}")
        
        result = control.set_attribute(attribute, value)
        logger.info(f"Set element {control_id} attribute {attribute} to {value}: {result}")
        return result
    
    def hover_element(self, control_id: str, x_offset: int = 0, y_offset: int = 0, duration: float = 0) -> bool:
        """鼠标悬停在控件上
        
        Args:
            control_id: 控件ID
            x_offset: 相对控件左上角的X偏移（像素），默认0
            y_offset: 相对控件左上角的Y偏移（像素），默认0
            duration: 悬停时长（秒），默认0
        
        Returns:
            是否悬停成功
        
        Example:
            | Hover Element | menu_item | duration=1 |
        """
        control = self._get_control(control_id)
        if not control:
            raise ValueError(f"Control not found: {control_id}")
        
        result = control.hover(x_offset, y_offset, duration)
        logger.info(f"Hover element {control_id} at offset ({x_offset}, {y_offset}) for {duration}s: {result}")
        return result
    
    def drag_element_to(self, source_control_id: str, target: Any, duration: float = 1.0) -> bool:
        """将控件拖拽到目标位置
        
        Args:
            source_control_id: 源控件ID
            target: 目标对象（控件ID或坐标 [x, y]）
            duration: 拖拽时长（秒），默认1.0
        
        Returns:
            是否拖拽成功
        
        Example:
            | Drag Element To | slider | [500, 300] | duration=0.5 |
            | Drag Element To | source_item | target_item |
        """
        source_control = self._get_control(source_control_id)
        if not source_control:
            raise ValueError(f"Source control not found: {source_control_id}")
        
        # 处理目标
        if isinstance(target, str):
            # 目标是控件ID
            target_control = self._get_control(target)
            if not target_control:
                raise ValueError(f"Target control not found: {target}")
            target_obj = target_control
        else:
            # 目标是坐标
            target_obj = target
        
        result = source_control.drag_to(target_obj, duration)
        logger.info(f"Drag element {source_control_id} to {target} with duration {duration}s: {result}")
        return result
    
    # ===================
    # 鼠标键盘关键字
    # ===================
    
    def mouse_click(self, x: int, y: int, button: str = "left", count: int = 1) -> bool:
        """鼠标点击指定坐标
        
        Args:
            x: X坐标（像素）
            y: Y坐标（像素）
            button: 鼠标按钮（left, right, middle），默认left
            count: 点击次数（1: 单击, 2: 双击），默认1
        
        Returns:
            是否点击成功
        
        Example:
            | Mouse Click | 100 | 100 |
            | Mouse Click | 200 | 200 | button=right |
            | Mouse Click | 300 | 300 | count=2 |
        """
        if not self._operation:
            raise RuntimeError("Operation object not initialized")
        
        result = self._operation.mouse_click(x, y, button, count)
        logger.info(f"Mouse click at ({x}, {y}), button={button}, count={count}: {result}")
        return result
    
    def mouse_move(self, x: int, y: int, duration: float = 0) -> bool:
        """鼠标移动到指定坐标
        
        Args:
            x: X坐标（像素）
            y: Y坐标（像素）
            duration: 移动时长（秒），默认0
        
        Returns:
            是否移动成功
        
        Example:
            | Mouse Move | 100 | 100 |
            | Mouse Move | 200 | 200 | duration=1 |
        """
        if not self._operation:
            raise RuntimeError("Operation object not initialized")
        
        result = self._operation.mouse_move(x, y, duration)
        logger.info(f"Mouse move to ({x}, {y}) with duration {duration}s: {result}")
        return result
    
    def mouse_drag(self, start_x: int, start_y: int, end_x: int, end_y: int, duration: float = 1.0) -> bool:
        """鼠标拖拽
        
        Args:
            start_x: 起始X坐标（像素）
            start_y: 起始Y坐标（像素）
            end_x: 结束X坐标（像素）
            end_y: 结束Y坐标（像素）
            duration: 拖拽时长（秒），默认1.0
        
        Returns:
            是否拖拽成功
        
        Example:
            | Mouse Drag | 100 | 100 | 200 | 200 | duration=0.5 |
        """
        if not self._operation:
            raise RuntimeError("Operation object not initialized")
        
        result = self._operation.mouse_drag(start_x, start_y, end_x, end_y, duration)
        logger.info(f"Mouse drag from ({start_x}, {start_y}) to ({end_x}, {end_y}) with duration {duration}s: {result}")
        return result
    
    def mouse_wheel(self, x: int, y: int, direction: str = "up", steps: int = 1) -> bool:
        """鼠标滚轮滚动
        
        Args:
            x: X坐标（像素）
            y: Y坐标（像素）
            direction: 滚动方向（up, down），默认up
            steps: 滚动步数，默认1
        
        Returns:
            是否滚动成功
        
        Example:
            | Mouse Wheel | 100 | 100 | direction=down | steps=3 |
        """
        if not self._operation:
            raise RuntimeError("Operation object not initialized")
        
        result = self._operation.mouse_wheel(x, y, direction, steps)
        logger.info(f"Mouse wheel at ({x}, {y}), direction={direction}, steps={steps}: {result}")
        return result
    
    def mouse_hover(self, x: int, y: int, duration: float = 0) -> bool:
        """鼠标悬停在指定坐标
        
        Args:
            x: X坐标（像素）
            y: Y坐标（像素）
            duration: 悬停时长（秒），默认0
        
        Returns:
            是否悬停成功
        
        Example:
            | Mouse Hover | 100 | 100 | duration=1 |
        """
        if not self._operation:
            raise RuntimeError("Operation object not initialized")
        
        result = self._operation.mouse_hover(x, y, duration)
        logger.info(f"Mouse hover at ({x}, {y}) for {duration}s: {result}")
        return result
    
    def get_mouse_position(self) -> List[int]:
        """获取当前鼠标位置
        
        Returns:
            当前鼠标坐标 [x, y]
        
        Example:
            | ${pos} | Get Mouse Position |
        """
        if not self._operation:
            raise RuntimeError("Operation object not initialized")
        
        return list(self._operation.get_mouse_position())
    
    def press_key(self, key: str) -> bool:
        """按下并释放指定按键
        
        Args:
            key: 按键名称（如A, Enter, Ctrl）
        
        Returns:
            是否按键成功
        
        Example:
            | Press Key | Enter |
            | Press Key | Tab |
        """
        if not self._operation:
            raise RuntimeError("Operation object not initialized")
        
        result = self._operation.press_key(key)
        logger.info(f"Press key {key}: {result}")
        return result
    
    def press_keys(self, keys: str) -> bool:
        """按下并释放组合键
        
        Args:
            keys: 组合键字符串（如Ctrl+C, Alt+Tab）
        
        Returns:
            是否按键成功
        
        Example:
            | Press Keys | Ctrl+C |
            | Press Keys | Alt+Tab |
        """
        if not self._operation:
            raise RuntimeError("Operation object not initialized")
        
        result = self._operation.press_keys(keys)
        logger.info(f"Press keys {keys}: {result}")
        return result
    
    def key_down(self, key: str) -> bool:
        """按下指定按键（不释放）
        
        Args:
            key: 按键名称
        
        Returns:
            是否按下成功
        
        Example:
            | Key Down | Ctrl |
        """
        if not self._operation:
            raise RuntimeError("Operation object not initialized")
        
        result = self._operation.key_down(key)
        logger.info(f"Key down {key}: {result}")
        return result
    
    def key_up(self, key: str) -> bool:
        """释放指定按键
        
        Args:
            key: 按键名称
        
        Returns:
            是否释放成功
        
        Example:
            | Key Up | Ctrl |
        """
        if not self._operation:
            raise RuntimeError("Operation object not initialized")
        
        result = self._operation.key_up(key)
        logger.info(f"Key up {key}: {result}")
        return result
    
    def type_text_with_keyboard(self, text: str, interval: float = 0.05) -> bool:
        """使用键盘输入文本
        
        Args:
            text: 要输入的文本
            interval: 按键间隔（秒），默认0.05
        
        Returns:
            是否输入成功
        
        Example:
            | Type Text With Keyboard | hello world |
        """
        if not self._operation:
            raise RuntimeError("Operation object not initialized")
        
        result = self._operation.type_text(text, interval)
        logger.info(f"Type text with keyboard: {text}: {result}")
        return result
    
    # ===================
    # 截图关键字
    # ===================
    
    def capture_screenshot(self, filename: str = None, x: int = 0, y: int = 0, width: int = 0, height: int = 0) -> str:
        """捕获屏幕截图
        
        Args:
            filename: 截图保存路径，如果为None则自动生成
            x: 起始X坐标（像素），0表示全屏
            y: 起始Y坐标（像素），0表示全屏
            width: 截图宽度（像素），0表示全屏
            height: 截图高度（像素），0表示全屏
        
        Returns:
            截图保存路径
        
        Example:
            | ${screenshot} | Capture Screenshot |
            | ${screenshot} | Capture Screenshot | C:/screenshots/test.png |
            | ${screenshot} | Capture Screenshot | x=100 | y=100 | width=600 | height=400 |
        """
        if not self._operation:
            raise RuntimeError("Operation object not initialized")
        
        screenshot_path = self._operation.capture_screenshot(filename, x, y, width, height)
        if screenshot_path:
            logger.info(f"Captured screenshot: {screenshot_path}")
            # 嵌入到Robot Framework报告
            logger.info(f"<img src='{screenshot_path}' width='800' />", html=True)
        else:
            logger.warn("Failed to capture screenshot")
        
        return screenshot_path
    
    def capture_window_screenshot(self, window_id: str, filename: str = None) -> str:
        """捕获窗口截图
        
        Args:
            window_id: 窗口ID
            filename: 截图保存路径，如果为None则自动生成
        
        Returns:
            截图保存路径
        
        Example:
            | ${screenshot} | Capture Window Screenshot | notepad_window |
        """
        window = self._get_window(window_id)
        if not window:
            raise ValueError(f"Window not found: {window_id}")
        
        if not self._operation:
            raise RuntimeError("Operation object not initialized")
        
        screenshot_path = self._operation.capture_window_screenshot(window._window, filename)
        if screenshot_path:
            logger.info(f"Captured window {window_id} screenshot: {screenshot_path}")
            # 嵌入到Robot Framework报告
            logger.info(f"<img src='{screenshot_path}' width='800' />", html=True)
        else:
            logger.warn(f"Failed to capture window {window_id} screenshot")
        
        return screenshot_path
    
    def capture_element_screenshot(self, control_id: str, filename: str = None) -> str:
        """捕获控件截图
        
        Args:
            control_id: 控件ID
            filename: 截图保存路径，如果为None则自动生成
        
        Returns:
            截图保存路径
        
        Example:
            | ${screenshot} | Capture Element Screenshot | login_button |
        """
        control = self._get_control(control_id)
        if not control:
            raise ValueError(f"Control not found: {control_id}")
        
        if not self._operation:
            raise RuntimeError("Operation object not initialized")
        
        screenshot_path = self._operation.capture_element_screenshot(control._control, filename)
        if screenshot_path:
            logger.info(f"Captured element {control_id} screenshot: {screenshot_path}")
            # 嵌入到Robot Framework报告
            logger.info(f"<img src='{screenshot_path}' width='800' />", html=True)
        else:
            logger.warn(f"Failed to capture element {control_id} screenshot")
        
        return screenshot_path
    
    def capture_screenshot_on_failure(self) -> None:
        """在测试失败时自动捕获截图
        
        该关键字通常与Run Keyword And Capture Screenshot一起使用
        
        Example:
            | Run Keyword And Capture Screenshot | Click Element | login_button |
        """
        if global_config.auto_screenshot_on_fail:
            test_name = BuiltIn().get_variable_value("${TEST NAME}")
            filename = f"{global_config.screenshot_path}failure_{test_name}_{int(time.time())}.{global_config.screenshot_format}"
            self.capture_screenshot(filename)
    
    # ===================
    # 等待关键字
    # ===================
    
    def wait(self, seconds: float) -> None:
        """等待指定时长
        
        Args:
            seconds: 等待时长（秒）
        
        Example:
            | Wait | 2 |
            | Wait | 0.5 |
        """
        if not self._operation:
            raise RuntimeError("Operation object not initialized")
        
        self._operation.wait(seconds)
        logger.info(f"Waited for {seconds} seconds")
    
    def wait_until(self, keyword: str, timeout: float = None, interval: float = 0.5, *args: Any) -> bool:
        """等待直到关键字执行成功或超时
        
        Args:
            keyword: 要执行的关键字
            timeout: 超时时间（秒），默认使用全局配置
            interval: 检查间隔（秒），默认0.5
            *args: 关键字参数
        
        Returns:
            关键字是否在超时内执行成功
        
        Example:
            | Wait Until | Element Is Visible | timeout=10 | loading_panel |
            | Wait Until | Get Element Text | ${element_id} | contains | success |
        """
        if timeout is None:
            timeout = global_config.timeout
        
        builtin = BuiltIn()
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            try:
                result = builtin.run_keyword(keyword, *args)
                if result:
                    logger.info(f"Wait until {keyword} succeeded after {time.time() - start_time:.2f} seconds")
                    return True
            except Exception as e:
                # 忽略异常，继续等待
                pass
            time.sleep(interval)
        
        logger.warn(f"Wait until {keyword} timed out after {timeout} seconds")
        return False
    
    # ===================
    # 工具关键字
    # ===================
    
    def get_screen_size(self) -> List[int]:
        """获取屏幕尺寸
        
        Returns:
            屏幕尺寸 [width, height]
        
        Example:
            | ${size} | Get Screen Size |
        """
        if not self._operation:
            raise RuntimeError("Operation object not initialized")
        
        return list(self._operation.get_screen_size())
    
    def get_dpi_scale(self) -> float:
        """获取屏幕DPI缩放比例
        
        Returns:
            DPI缩放比例
        
        Example:
            | ${dpi} | Get DPI Scale |
        """
        if not self._operation:
            raise RuntimeError("Operation object not initialized")
        
        return self._operation.get_dpi_scale()
    
    def adapt_coordinate(self, x: int, y: int) -> List[int]:
        """适配坐标到当前DPI
        
        Args:
            x: 原始X坐标
            y: 原始Y坐标
        
        Returns:
            适配后的坐标 [x, y]
        
        Example:
            | ${adapted} | Adapt Coordinate | 100 | 100 |
        """
        if not self._operation:
            raise RuntimeError("Operation object not initialized")
        
        return list(self._operation.adapt_coordinate(x, y))
    
    def adapt_size(self, width: int, height: int) -> List[int]:
        """适配尺寸到当前DPI
        
        Args:
            width: 原始宽度
            height: 原始高度
        
        Returns:
            适配后的尺寸 [width, height]
        
        Example:
            | ${adapted} | Adapt Size | 800 | 600 |
        """
        if not self._operation:
            raise RuntimeError("Operation object not initialized")
        
        return list(self._operation.adapt_size(width, height))
    
    # ===================
    # 清理关键字
    # ===================
    
    def close_all_applications(self) -> None:
        """关闭所有已启动或附加的应用
        
        Example:
            | Close All Applications |
        """
        app_ids = list(self._applications.keys())
        for app_id in app_ids:
            try:
                self.kill_application(app_id)
            except Exception as e:
                logger.warn(f"Failed to close application {app_id}: {e}")
        
        # 清理窗口和控件
        self._windows.clear()
        self._controls.clear()
        
        logger.info("Closed all applications")
    
    def clear_all_objects(self) -> None:
        """清理所有对象（应用、窗口、控件）
        
        Example:
            | Clear All Objects |
        """
        self._applications.clear()
        self._windows.clear()
        self._controls.clear()
        logger.info("Cleared all objects")

# 导出库类
__all__ = ["RFWinLibrary"]
