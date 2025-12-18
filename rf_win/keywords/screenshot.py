# 截图关键字模块
# 实现截图相关的Robot Framework关键字

from typing import Any, List, Optional
from robot.api import logger

class ScreenshotKeywords:
    """截图关键字类
    
    提供截图相关的关键字，包括：
    - 捕获屏幕截图
    - 捕获窗口截图
    - 捕获控件截图
    """
    
    def __init__(self, library):
        """初始化截图关键字
        
        Args:
            library: 主库实例，用于访问应用、窗口、控件管理器
        """
        self._library = library
        self._operation = library._operation
        self._get_window = library._get_window
        self._get_control = library._get_control
        
    def capture_screenshot(self, filename: Optional[str] = None, x: int = 0, y: int = 0, width: int = 0, height: int = 0) -> str:
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
    
    def capture_window_screenshot(self, window_id: str, filename: Optional[str] = None) -> str:
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
    
    def capture_element_screenshot(self, control_id: str, filename: Optional[str] = None) -> str:
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
