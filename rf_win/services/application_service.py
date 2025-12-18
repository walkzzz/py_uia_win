# 应用服务模块
# 封装应用管理的核心业务逻辑

from typing import Any, Optional
from ..drivers.automation_driver import driver_factory
from ..utils.cache import ControlCache
from ..utils.logger import logger

class ApplicationService:
    """应用服务，负责应用管理的核心业务逻辑"""
    
    def __init__(self):
        self._driver = driver_factory.get_driver()
        self._cache = ControlCache()
    
    def start_application(self, path: str, args: Optional[str] = None, backend: str = "pywinauto") -> Any:
        """启动应用程序
        
        Args:
            path: 应用程序路径
            args: 启动参数
            backend: 后端类型
        
        Returns:
            应用对象
        """
        logger.info(f"Starting application: {path}, args: {args}, backend: {backend}")
        return self._driver.start_application(path, args, backend)
    
    def attach_to_application(self, identifier: Any, backend: str = "pywinauto") -> Any:
        """连接到已运行的应用程序
        
        Args:
            identifier: 应用标识符（PID、进程名、窗口标题等）
            backend: 后端类型
        
        Returns:
            应用对象
        """
        logger.info(f"Attaching to application: {identifier}, backend: {backend}")
        return self._driver.attach_to_application(identifier, backend)
    
    def close_application(self, app: Any, timeout: float = 10.0) -> bool:
        """关闭应用程序
        
        Args:
            app: 应用对象
            timeout: 超时时间
        
        Returns:
            是否成功
        """
        logger.info(f"Closing application: {app}")
        return self._driver.close_application(app, timeout)
    
    def kill_application(self, app: Any) -> bool:
        """强制终止应用程序
        
        Args:
            app: 应用对象
        
        Returns:
            是否成功
        """
        logger.info(f"Killing application: {app}")
        # 对于kill操作，直接调用close_application，驱动会处理强制终止逻辑
        return self._driver.close_application(app, 0)
    
    def check_application_running(self, app: Any) -> bool:
        """检查应用程序是否正在运行
        
        Args:
            app: 应用对象
        
        Returns:
            是否正在运行
        """
        logger.info(f"Checking application running status: {app}")
        try:
            # 这里简单检查app对象是否还能响应
            # 实际实现可能需要根据驱动类型进行调整
            if hasattr(app, 'is_process_running'):
                return app.is_process_running()
            elif hasattr(app, 'process_id'):
                return app.process_id() is not None
            else:
                return True
        except Exception as e:
            logger.error(f"Failed to check application running status: {e}")
            return False
    
    def get_application_process_id(self, app: Any) -> Optional[int]:
        """获取应用程序进程ID
        
        Args:
            app: 应用对象
        
        Returns:
            进程ID
        """
        logger.info(f"Getting application process ID: {app}")
        try:
            if hasattr(app, 'process_id'):
                return app.process_id()
            elif hasattr(app, '_process_id'):
                return app._process_id
            elif hasattr(app, 'process'):
                return app.process.id
            else:
                return None
        except Exception as e:
            logger.error(f"Failed to get application process ID: {e}")
            return None
    
    def wait_for_application_main_window(self, app: Any, timeout: float = 10.0) -> Any:
        """等待应用程序主窗口出现
        
        Args:
            app: 应用对象
            timeout: 超时时间
        
        Returns:
            主窗口对象
        
        Raises:
            TimeoutError: 如果超时
        """
        logger.info(f"Waiting for application main window: {app}")
        import time
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            try:
                # 使用驱动的find_window方法查找主窗口
                main_window = self._driver.find_window(app, {})
                if main_window:
                    return main_window
            except Exception:
                pass
            time.sleep(0.5)
        
        raise TimeoutError(f"Main window not found within timeout: {timeout}s")
