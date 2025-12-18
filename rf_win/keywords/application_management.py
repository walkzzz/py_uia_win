# 应用管理关键字模块
# 实现应用相关的Robot Framework关键字

from typing import Any, List, Optional
from robot.api import logger

from ..core.base_application import BaseApplication

class ApplicationManagementKeywords:
    """应用管理关键字类
    
    提供应用相关的关键字，包括：
    - 启动应用
    - 附加到应用
    - 关闭应用
    - 强制终止应用
    - 检查应用状态
    - 获取应用进程ID
    - 等待应用主窗口
    """
    
    def __init__(self, library):
        """初始化应用管理关键字
        
        Args:
            library: 主库实例，用于访问应用、窗口、控件管理器
        """
        self._library = library
        self._applications = library._applications
        self._get_backend = library._get_backend
        self._get_application = library._get_application
        self._add_application = library._add_application
        self._remove_application = library._remove_application
        
    def start_application(self, path: str, app_id: Optional[str] = None, args: Optional[str] = None, admin: bool = False, background: bool = False, backend: Optional[str] = None) -> str:
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
        import time
        
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
    
    def attach_to_application(self, identifier: Any, app_id: Optional[str] = None, backend: Optional[str] = None) -> str:
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
        import time
        
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
    
    def close_application(self, app_id: str, timeout: Optional[float] = None) -> bool:
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
        from ..config.global_config import global_config
        
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
    
    def wait_for_application_main_window(self, app_id: str, timeout: Optional[float] = None) -> bool:
        """等待应用主窗口出现
        
        Args:
            app_id: 应用ID
            timeout: 超时时间（秒），默认使用全局配置
        
        Returns:
            是否找到主窗口
        
        Example:
            | Wait For Application Main Window | notepad | timeout=15 |
        """
        from ..config.global_config import global_config
        
        app = self._get_application(app_id)
        if not app:
            raise ValueError(f"Application not found: {app_id}")
        
        if timeout is None:
            timeout = global_config.timeout
        
        result = app.wait_for_main_window(timeout)
        logger.info(f"Wait for application {app_id} main window: {result}")
        return result
