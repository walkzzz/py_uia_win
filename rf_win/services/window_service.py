# 窗口服务模块
# 封装窗口管理的核心业务逻辑

from typing import Any, Dict, List, Optional
from ..drivers.automation_driver import driver_factory
from ..utils.cache import ControlCache

class WindowService:
    """窗口服务，负责窗口管理的核心业务逻辑"""
    
    def __init__(self):
        self._driver = driver_factory.get_driver()
        self._cache = ControlCache()
    
    def create_application(self, path: str, app_id: str, args: Optional[str] = None, backend: str = "uia") -> Any:
        """创建应用程序
        
        Args:
            path: 应用路径
            app_id: 应用ID
            args: 启动参数
            backend: 后端类型
        
        Returns:
            应用对象
        """
        app = self._driver.create_application(app_id, backend)
        cmd = path
        if args:
            cmd += f" {args}"
        app.start(cmd, wait_for_idle=True)
        return app
    
    def connect_to_application(self, identifier: Any, backend: str = "uia") -> Any:
        """连接到已运行的应用程序
        
        Args:
            identifier: 应用标识符（PID、进程名、窗口标题等）
            backend: 后端类型
        
        Returns:
            应用对象
        """
        return self._driver.connect_to_application(identifier, backend)
    
    def find_window(self, app: Any, window_identifier: Any) -> Any:
        """查找窗口
        
        Args:
            app: 应用对象
            window_identifier: 窗口标识符
        
        Returns:
            窗口对象
        """
        return self._driver.find_window(app, window_identifier)
    
    def activate_window(self, window: Any) -> bool:
        """激活窗口
        
        Args:
            window: 窗口对象
        
        Returns:
            是否成功
        """
        try:
            window.set_focus()
            return True
        except Exception:
            return False
    
    def close_window(self, window: Any, timeout: float = 10.0) -> bool:
        """关闭窗口
        
        Args:
            window: 窗口对象
            timeout: 超时时间
        
        Returns:
            是否成功
        """
        try:
            window.close(timeout=timeout)
            return True
        except Exception:
            return False
    
    def minimize_window(self, window: Any) -> bool:
        """最小化窗口
        
        Args:
            window: 窗口对象
        
        Returns:
            是否成功
        """
        try:
            window.minimize()
            return True
        except Exception:
            return False
    
    def maximize_window(self, window: Any) -> bool:
        """最大化窗口
        
        Args:
            window: 窗口对象
        
        Returns:
            是否成功
        """
        try:
            window.maximize()
            return True
        except Exception:
            return False
    
    def restore_window(self, window: Any) -> bool:
        """恢复窗口
        
        Args:
            window: 窗口对象
        
        Returns:
            是否成功
        """
        try:
            window.restore()
            return True
        except Exception:
            return False
    
    def get_window_title(self, window: Any) -> Optional[str]:
        """获取窗口标题
        
        Args:
            window: 窗口对象
        
        Returns:
            窗口标题
        """
        try:
            return window.window_text()
        except Exception:
            return None
    
    def get_window_rect(self, window: Any) -> Optional[Dict[str, int]]:
        """获取窗口矩形
        
        Args:
            window: 窗口对象
        
        Returns:
            窗口矩形字典，包含x, y, width, height
        """
        try:
            rect = window.rectangle()
            return {
                "x": rect.left,
                "y": rect.top,
                "width": rect.width(),
                "height": rect.height()
            }
        except Exception:
            return None
    
    def set_window_rect(self, window: Any, x: int, y: int, width: int, height: int) -> bool:
        """设置窗口矩形
        
        Args:
            window: 窗口对象
            x: X坐标
            y: Y坐标
            width: 宽度
            height: 高度
        
        Returns:
            是否成功
        """
        try:
            window.move_window(x, y, width, height)
            return True
        except Exception:
            return False
    
    def is_window_active(self, window: Any) -> bool:
        """检查窗口是否激活
        
        Args:
            window: 窗口对象
        
        Returns:
            是否激活
        """
        try:
            return window.is_active()
        except Exception:
            return False
    
    def is_window_visible(self, window: Any) -> bool:
        """检查窗口是否可见
        
        Args:
            window: 窗口对象
        
        Returns:
            是否可见
        """
        try:
            return window.is_visible()
        except Exception:
            return False
    
    def is_window_closed(self, window: Any) -> bool:
        """检查窗口是否关闭
        
        Args:
            window: 窗口对象
        
        Returns:
            是否关闭
        """
        try:
            return not window.exists()
        except Exception:
            return True
    
    def wait_for_window(self, app: Any, window_identifier: Any, timeout: float = 10.0) -> Any:
        """等待窗口出现
        
        Args:
            app: 应用对象
            window_identifier: 窗口标识符
            timeout: 超时时间
        
        Returns:
            窗口对象
        
        Raises:
            TimeoutError: 如果超时
        """
        import time
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                window = self.find_window(app, window_identifier)
                if window and window.exists():
                    return window
            except Exception:
                pass
            time.sleep(0.5)
        raise TimeoutError(f"Window not found within timeout: {timeout}s")
    
    def wait_for_window_close(self, window: Any, timeout: float = 10.0) -> bool:
        """等待窗口关闭
        
        Args:
            window: 窗口对象
            timeout: 超时时间
        
        Returns:
            是否关闭
        """
        import time
        start_time = time.time()
        while time.time() - start_time < timeout:
            if self.is_window_closed(window):
                return True
            time.sleep(0.5)
        return False
