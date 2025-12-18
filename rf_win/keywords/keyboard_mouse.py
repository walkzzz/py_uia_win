# 鼠标键盘操作关键字模块
# 实现鼠标键盘相关的Robot Framework关键字

from typing import Any, List, Optional
from robot.api import logger

class KeyboardMouseKeywords:
    """鼠标键盘操作关键字类
    
    提供鼠标键盘相关的关键字，包括：
    - 鼠标点击
    - 鼠标移动
    - 鼠标拖拽
    - 鼠标滚轮
    - 鼠标悬停
    - 获取鼠标位置
    - 按键操作
    - 组合键操作
    - 键盘输入文本
    """
    
    def __init__(self, library):
        """初始化鼠标键盘操作关键字
        
        Args:
            library: 主库实例，用于访问应用、窗口、控件管理器
        """
        self._library = library
        self._operation = library._operation
        
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