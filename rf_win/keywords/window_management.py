# 窗口管理关键字模块
# 实现窗口相关的Robot Framework关键字

from typing import Any, List, Optional
from robot.api import logger

from ..core.base_application import BaseApplication
from ..core.base_window import BaseWindow

class WindowManagementKeywords:
    """窗口管理关键字类
    
    提供窗口相关的关键字，包括：
    - 获取主窗口
    - 定位窗口
    - 激活窗口
    - 关闭窗口
    - 窗口状态管理（最大化、最小化、恢复）
    - 窗口属性获取
    - 窗口等待
    """
    
    def __init__(self, library):
        """初始化窗口管理关键字
        
        Args:
            library: 主库实例，用于访问应用、窗口、控件管理器
        """
        self._library = library
        self._applications = library._applications
        self._windows = library._windows
        self._get_backend = library._get_backend
        self._get_application = library._get_application
        self._get_window = library._get_window
        self._add_window = library._add_window
        self._remove_window = library._remove_window
        
    def get_main_window(self, app_id: str, window_id: Optional[str] = None) -> str:
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
            import time
            window_id = f"window_{int(time.time())}"
        
        backend_instance = self._get_backend()
        window = backend_instance.create_window(main_window, app)
        self._add_window(window_id, window)
        
        logger.info(f"Got main window for application {app_id}, window_id: {window_id}")
        return window_id
    
    def locate_window(self, app_id: str, window_identifier: Any, window_id: Optional[str] = None) -> str:
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
            import time
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
    
    def close_window(self, window_id: str, timeout: Optional[float] = None) -> bool:
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
        from ..config.global_config import global_config
        
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
    
    def wait_for_window_close(self, window_id: str, timeout: Optional[float] = None) -> bool:
        """等待窗口关闭
        
        Args:
            window_id: 窗口ID
            timeout: 超时时间（秒），默认使用全局配置
        
        Returns:
            窗口是否在超时内关闭
        
        Example:
            | Wait For Window Close | notepad_window | timeout=15 |
        """
        from ..config.global_config import global_config
        
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
