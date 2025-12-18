#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
操作服务模块
提供鼠标、键盘、等待和截图等操作的实现
"""

import time
import os
from ..utils.logger import logger
from ..services.control_service import ControlService
from ..services.window_service import WindowService
from ..utils.wait_strategy import WaitStrategy
from ..utils.locator_helper import LocatorHelper
from ..utils.dpi_adapter import DPIAdapter

class OperationService:
    """操作服务类
    
    提供鼠标、键盘、等待和截图等操作的实现
    """
    
    def __init__(self):
        """初始化操作服务实例
        
        创建控件服务和窗口服务实例，用于控件和窗口操作
        """
        self.control_service = ControlService()
        self.window_service = WindowService()
        self.wait_strategy = WaitStrategy()
        self.dpi_adapter = DPIAdapter()
    
    def click_mouse(self, x, y, button='left', double=False):
        """点击鼠标
        
        在指定位置点击鼠标
        
        参数:
            x: 点击位置的x坐标
            y: 点击位置的y坐标
            button: 鼠标按钮，可选值为'left'、'right'、'middle'
            double: 是否双击，默认为False
        """
        # 转换为物理坐标
        physical_x, physical_y = self.dpi_adapter.logical_to_physical(x, y)
        
        # 调用底层操作
        from ..backend.backend_factory import backend_factory
        backend = backend_factory.get_backend()
        return backend.click_mouse(physical_x, physical_y, button, double)
    
    def move_mouse(self, x, y, duration=0):
        """移动鼠标
        
        将鼠标移动到指定位置
        
        参数:
            x: 目标位置的x坐标
            y: 目标位置的y坐标
            duration: 移动持续时间，单位为秒
        """
        # 转换为物理坐标
        physical_x, physical_y = self.dpi_adapter.logical_to_physical(x, y)
        
        # 调用底层操作
        from ..backend.backend_factory import backend_factory
        backend = backend_factory.get_backend()
        return backend.move_mouse(physical_x, physical_y, duration)
    
    def drag_mouse(self, start_x, start_y, end_x, end_y, duration=0):
        """拖拽鼠标
        
        从起始位置拖拽鼠标到结束位置
        
        参数:
            start_x: 起始位置的x坐标
            start_y: 起始位置的y坐标
            end_x: 结束位置的x坐标
            end_y: 结束位置的y坐标
            duration: 拖拽持续时间，单位为秒
        """
        # 转换为物理坐标
        start_physical_x, start_physical_y = self.dpi_adapter.logical_to_physical(start_x, start_y)
        end_physical_x, end_physical_y = self.dpi_adapter.logical_to_physical(end_x, end_y)
        
        # 调用底层操作
        from ..backend.backend_factory import backend_factory
        backend = backend_factory.get_backend()
        return backend.drag_mouse(start_physical_x, start_physical_y, end_physical_x, end_physical_y, duration)
    
    def scroll_mouse(self, x, y, clicks, horizontal=False):
        """滚动鼠标
        
        在指定位置滚动鼠标
        
        参数:
            x: 滚动位置的x坐标
            y: 滚动位置的y坐标
            clicks: 滚动的距离，正数向上/向右，负数向下/向左
            horizontal: 是否水平滚动，默认为False（垂直滚动）
        """
        # 转换为物理坐标
        physical_x, physical_y = self.dpi_adapter.logical_to_physical(x, y)
        
        # 调用底层操作
        from ..backend.backend_factory import backend_factory
        backend = backend_factory.get_backend()
        return backend.scroll_mouse(physical_x, physical_y, clicks, horizontal)
    
    def press_mouse(self, x, y, button='left'):
        """按下鼠标
        
        在指定位置按下鼠标按钮
        
        参数:
            x: 按下位置的x坐标
            y: 按下位置的y坐标
            button: 鼠标按钮，可选值为'left'、'right'、'middle'
        """
        # 转换为物理坐标
        physical_x, physical_y = self.dpi_adapter.logical_to_physical(x, y)
        
        # 调用底层操作
        from ..backend.backend_factory import backend_factory
        backend = backend_factory.get_backend()
        return backend.press_mouse(physical_x, physical_y, button)
    
    def release_mouse(self, x, y, button='left'):
        """释放鼠标
        
        在指定位置释放鼠标按钮
        
        参数:
            x: 释放位置的x坐标
            y: 释放位置的y坐标
            button: 鼠标按钮，可选值为'left'、'right'、'middle'
        """
        # 转换为物理坐标
        physical_x, physical_y = self.dpi_adapter.logical_to_physical(x, y)
        
        # 调用底层操作
        from ..backend.backend_factory import backend_factory
        backend = backend_factory.get_backend()
        return backend.release_mouse(physical_x, physical_y, button)
    
    def get_mouse_position(self):
        """获取鼠标位置
        
        获取当前鼠标的位置
        
        返回:
            包含x和y坐标的字典
        """
        # 调用底层操作
        from ..backend.backend_factory import backend_factory
        backend = backend_factory.get_backend()
        physical_x, physical_y = backend.get_mouse_position()
        
        # 转换为逻辑坐标
        logical_x, logical_y = self.dpi_adapter.physical_to_logical(physical_x, physical_y)
        
        return {'x': logical_x, 'y': logical_y}
    
    def type_text(self, text, delay=0):
        """输入文本
        
        输入指定的文本
        
        参数:
            text: 要输入的文本
            delay: 按键之间的延迟，单位为秒
        """
        # 调用底层操作
        from ..backend.backend_factory import backend_factory
        backend = backend_factory.get_backend()
        return backend.type_text(text, delay)
    
    def press_key(self, key, modifier=None):
        """按下按键
        
        按下指定的按键
        
        参数:
            key: 要按下的按键
            modifier: 修饰键，可选值为'Ctrl'、'Alt'、'Shift'、'Win'
        """
        # 调用底层操作
        from ..backend.backend_factory import backend_factory
        backend = backend_factory.get_backend()
        return backend.press_key(key, modifier)
    
    def release_key(self, key, modifier=None):
        """释放按键
        
        释放指定的按键
        
        参数:
            key: 要释放的按键
            modifier: 修饰键，可选值为'Ctrl'、'Alt'、'Shift'、'Win'
        """
        # 调用底层操作
        from ..backend.backend_factory import backend_factory
        backend = backend_factory.get_backend()
        return backend.release_key(key, modifier)
    
    def combo_keys(self, keys):
        """组合按键
        
        按下并释放指定的组合按键
        
        参数:
            keys: 组合按键，格式为'Ctrl+C'、'Alt+F4'等
        """
        # 调用底层操作
        from ..backend.backend_factory import backend_factory
        backend = backend_factory.get_backend()
        return backend.combo_keys(keys)
    
    def wait(self, seconds):
        """等待
        
        等待指定的时间
        
        参数:
            seconds: 等待时间，单位为秒
        """
        time.sleep(seconds)
        return True
    
    def wait_for_control_exists(self, locator, window_title=None, app_alias=None, timeout=30):
        """等待控件存在
        
        等待指定的控件存在
        
        参数:
            locator: 控件定位器，格式为"类型:属性=值"
            window_title: 窗口标题，可以是完整标题或正则表达式
            app_alias: 应用程序的别名
            timeout: 等待超时时间，单位为秒
        """
        def condition():
            return self.control_service.is_control_exists(locator, window_title, app_alias)
        
        return self.wait_strategy.wait_until(condition, timeout, f"控件不存在: {locator}")
    
    def wait_for_control_visible(self, locator, window_title=None, app_alias=None, timeout=30):
        """等待控件可见
        
        等待指定的控件可见
        
        参数:
            locator: 控件定位器，格式为"类型:属性=值"
            window_title: 窗口标题，可以是完整标题或正则表达式
            app_alias: 应用程序的别名
            timeout: 等待超时时间，单位为秒
        """
        def condition():
            return self.control_service.is_control_visible(locator, window_title, app_alias)
        
        return self.wait_strategy.wait_until(condition, timeout, f"控件不可见: {locator}")
    
    def wait_for_control_enabled(self, locator, window_title=None, app_alias=None, timeout=30):
        """等待控件启用
        
        等待指定的控件启用
        
        参数:
            locator: 控件定位器，格式为"类型:属性=值"
            window_title: 窗口标题，可以是完整标题或正则表达式
            app_alias: 应用程序的别名
            timeout: 等待超时时间，单位为秒
        """
        def condition():
            return self.control_service.is_control_enabled(locator, window_title, app_alias)
        
        return self.wait_strategy.wait_until(condition, timeout, f"控件未启用: {locator}")
    
    def wait_for_window_exists(self, window_title, app_alias=None, timeout=30):
        """等待窗口存在
        
        等待指定的窗口存在
        
        参数:
            window_title: 窗口标题，可以是完整标题或正则表达式
            app_alias: 应用程序的别名
            timeout: 等待超时时间，单位为秒
        """
        def condition():
            return self.window_service.is_window_exists(window_title, app_alias)
        
        return self.wait_strategy.wait_until(condition, timeout, f"窗口不存在: {window_title}")
    
    def take_screenshot(self, filename=None, folder=None, window_title=None, app_alias=None):
        """截图
        
        截取当前屏幕或指定窗口的截图
        
        参数:
            filename: 截图文件名
            folder: 截图保存文件夹
            window_title: 窗口标题，可以是完整标题或正则表达式
            app_alias: 应用程序的别名
        
        返回:
            截图文件路径
        """
        # 生成文件名
        if not filename:
            filename = f"screenshot_{time.strftime('%Y%m%d_%H%M%S')}"
        
        # 生成文件路径
        if not folder:
            folder = os.path.join(os.getcwd(), 'screenshots')
        
        # 确保文件夹存在
        os.makedirs(folder, exist_ok=True)
        
        # 完整文件路径
        file_path = os.path.join(folder, f"{filename}.png")
        
        # 调用底层操作
        from ..backend.backend_factory import backend_factory
        backend = backend_factory.get_backend()
        
        if window_title:
            # 获取窗口实例
            window = self.window_service.switch_window(window_title, app_alias)
            if window:
                return backend.take_screenshot(file_path, window)
            else:
                logger.error(f"未找到窗口: {window_title}")
                return None
        else:
            # 截取整个屏幕
            return backend.take_screenshot(file_path)
