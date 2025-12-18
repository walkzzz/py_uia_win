# 应用服务模块
# 封装应用管理的核心业务逻辑

from typing import Any, Optional, Dict
from ..drivers.automation_driver import driver_factory
from ..utils.cache_manager import cache_manager
from ..utils.logger import logger

class ApplicationService:
    """应用服务，负责应用管理的核心业务逻辑"""
    
    def __init__(self):
        self._driver = driver_factory.get_driver()
        # 保存应用实例，key为别名，value为应用对象
        self._applications: Dict[str, Any] = {}
        # 当前活动的应用别名
        self._current_app_alias: Optional[str] = None
    
    def start_application(self, app_path: str, alias: Optional[str] = None, backend: Optional[str] = None, **kwargs) -> Any:
        """启动应用程序
        
        启动指定路径的应用程序，并返回应用实例
        
        参数:
            app_path: 应用程序路径
            alias: 应用程序的别名，用于后续操作引用
            backend: 后端类型
            **kwargs: 启动应用程序时的额外参数
        
        返回:
            应用对象
        """
        logger.info(f"启动应用: {app_path}, 别名: {alias}, 后端: {backend}")
        
        # 调用驱动的启动应用方法
        app = self._driver.start_application(app_path, None, backend or "pywinauto")
        
        # 如果提供了别名，保存应用实例
        if alias:
            self._applications[alias] = app
            self._current_app_alias = alias
        
        return app
    
    def connect_application(self, process_id: Optional[int] = None, title: Optional[str] = None, alias: Optional[str] = None, backend: Optional[str] = None, **kwargs) -> Any:
        """连接到已运行的应用程序
        
        通过进程ID或窗口标题连接到已运行的应用程序
        
        参数:
            process_id: 应用程序的进程ID
            title: 应用程序的窗口标题
            alias: 应用程序的别名，用于后续操作引用
            backend: 后端类型
            **kwargs: 连接应用程序时的额外参数
        
        返回:
            应用对象
        """
        logger.info(f"连接应用: 进程ID={process_id}, 标题={title}, 别名={alias}, 后端={backend}")
        
        # 构建标识符
        identifier = process_id or title
        if not identifier:
            logger.error("必须提供进程ID或窗口标题")
            return None
        
        # 调用驱动的连接应用方法
        app = self._driver.attach_to_application(identifier, backend or "pywinauto")
        
        # 如果提供了别名，保存应用实例
        if alias:
            self._applications[alias] = app
            self._current_app_alias = alias
        
        return app
    
    def get_application(self, app_alias: Optional[str] = None) -> Any:
        """获取应用实例
        
        获取指定别名的应用实例，如果不指定别名，则获取当前活动的应用实例
        
        参数:
            app_alias: 应用程序的别名
        
        返回:
            应用对象
        """
        if app_alias:
            # 获取指定别名的应用实例
            return self._applications.get(app_alias)
        else:
            # 获取当前活动的应用实例
            if self._current_app_alias:
                return self._applications.get(self._current_app_alias)
            return None
    
    def get_current_application(self) -> Any:
        """获取当前活动的应用实例
        
        返回当前活动的应用实例
        
        返回:
            应用对象
        """
        return self.get_application()
    
    def switch_application(self, app_alias: str) -> Any:
        """切换当前活动的应用实例
        
        切换当前活动的应用实例为指定别名的应用实例
        
        参数:
            app_alias: 应用程序的别名
        
        返回:
            应用对象
        """
        if app_alias in self._applications:
            self._current_app_alias = app_alias
            return self._applications[app_alias]
        logger.error(f"未找到应用实例: {app_alias}")
        return None
    
    def close_application(self, app_alias: Optional[str] = None) -> bool:
        """关闭应用程序
        
        关闭指定别名的应用程序，如果不指定别名，则关闭当前活动的应用程序
        
        参数:
            app_alias: 应用程序的别名
        
        返回:
            是否成功
        """
        # 获取应用实例
        app = self.get_application(app_alias)
        if not app:
            logger.error(f"未找到应用实例: {app_alias}")
            return False
        
        # 调用驱动的关闭应用方法
        result = self._driver.close_application(app, 10.0)
        
        # 如果成功关闭，从应用实例字典中移除
        if result and app_alias:
            self._applications.pop(app_alias, None)
            # 如果关闭的是当前活动的应用实例，重置当前应用别名
            if self._current_app_alias == app_alias:
                self._current_app_alias = None
        
        return result
    
    def close_all_applications(self) -> bool:
        """关闭所有已连接的应用程序
        
        关闭所有通过关键字启动或连接的应用程序
        
        返回:
            是否成功
        """
        success = True
        # 复制应用实例字典的键，避免在迭代过程中修改字典
        app_aliases = list(self._applications.keys())
        
        for alias in app_aliases:
            if not self.close_application(alias):
                success = False
        
        # 重置当前应用别名
        self._current_app_alias = None
        
        return success
    
    def is_application_running(self, app_alias: str) -> bool:
        """检查应用程序是否正在运行
        
        检查指定别名的应用程序是否正在运行
        
        参数:
            app_alias: 应用程序的别名
        
        返回:
            True如果应用程序正在运行，否则返回False
        """
        # 获取应用实例
        app = self._applications.get(app_alias)
        if not app:
            return False
        
        # 检查应用实例是否正在运行
        try:
            # 这里简单检查app对象是否还能响应
            # 实际实现可能需要根据驱动类型进行调整
            if hasattr(app, 'is_process_running'):
                return app.is_process_running()
            elif hasattr(app, 'process_id'):
                return app.process_id() is not None
            elif hasattr(app, 'process'):
                return app.process is not None
            else:
                return True
        except Exception as e:
            logger.error(f"检查应用运行状态时出错: {e}")
            return False
    
    def get_application_process_id(self, app: Any) -> Optional[int]:
        """获取应用程序进程ID
        
        获取指定应用实例的进程ID
        
        参数:
            app: 应用对象
        
        返回:
            进程ID
        """
        logger.info(f"获取应用进程ID: {app}")
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
            logger.error(f"获取应用进程ID时出错: {e}")
            return None
    
    def wait_for_application_main_window(self, app: Any, timeout: float = 10.0) -> Any:
        """等待应用程序主窗口出现
        
        等待指定应用实例的主窗口出现
        
        参数:
            app: 应用对象
            timeout: 超时时间
        
        返回:
            主窗口对象
        
        抛出:
            TimeoutError: 如果超时
        """
        logger.info(f"等待应用主窗口: {app}")
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
        
        raise TimeoutError(f"超时未找到主窗口: {timeout}s")
