#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pywinauto驱动模块
实现基于pywinauto库的自动化驱动
"""

from typing import Any, List, Optional, Dict
from pywinauto import Application as PywinautoApp
from pywinauto.findwindows import find_window, find_windows, ElementNotFoundError
from pywinauto.keyboard import send_keys, press, release
from pywinauto.mouse import click, double_click, right_click, move, drag
from pywinauto.base_wrapper import BaseWrapper
from pywinauto.controls.uiawrapper import UIAWrapper
from pywinauto.controls.hwndwrapper import HwndWrapper
from pywinauto.timings import wait_until_passes
from pywinauto.application import ProcessNotFoundError
from ..utils.logger import logger

class PywinautoDriver:
    """pywinauto驱动类，实现自动化驱动接口
    
    基于pywinauto库，实现自动化驱动的核心功能，包括应用管理、窗口管理、控件操作等
    """
    
    def __init__(self):
        """初始化pywinauto驱动实例
        
        设置默认的后端类型为'uia'，因为uia后端支持更多的控件类型
        """
        self._default_backend = 'uia'
    
    def start_application(self, path: str, args: Optional[str] = None, backend: Optional[str] = None) -> Any:
        """启动应用程序
        
        启动指定路径的应用程序，并返回应用对象
        
        参数:
            path: 应用程序路径
            args: 启动参数
            backend: 后端类型，可选值为'uia'或'win32'
        
        返回:
            应用对象
        """
        logger.info(f"启动应用: {path}, 参数: {args}, 后端: {backend}")
        
        # 使用pywinauto.Application启动应用
        app = PywinautoApp(backend=backend or self._default_backend)
        
        if args:
            app.start(f"{path} {args}")
        else:
            app.start(path)
        
        return app
    
    def attach_to_application(self, identifier: Any, backend: Optional[str] = None) -> Any:
        """连接到已运行的应用程序
        
        通过进程ID或窗口标题连接到已运行的应用程序
        
        参数:
            identifier: 应用标识符（PID、进程名、窗口标题等）
            backend: 后端类型，可选值为'uia'或'win32'
        
        返回:
            应用对象
        """
        logger.info(f"连接应用: 标识符={identifier}, 后端: {backend}")
        
        # 使用pywinauto.Application连接到已运行的应用
        app = PywinautoApp(backend=backend or self._default_backend)
        
        if isinstance(identifier, int):
            # 通过进程ID连接
            app.connect(process=identifier)
        else:
            # 通过窗口标题连接
            app.connect(title_re=identifier)
        
        return app
    
    def close_application(self, app: Any, timeout: float = 10.0) -> bool:
        """关闭应用程序
        
        关闭指定的应用程序
        
        参数:
            app: 应用对象
            timeout: 超时时间
        
        返回:
            是否成功
        """
        logger.info(f"关闭应用: {app}, 超时: {timeout}")
        
        try:
            # 尝试优雅关闭应用
            app.kill()
            return True
        except Exception as e:
            logger.error(f"关闭应用失败: {e}")
            return False
    
    def find_window(self, app: Any, locator: Dict[str, Any], timeout: float = 10.0) -> Any:
        """查找窗口
        
        根据定位器查找指定应用中的窗口
        
        参数:
            app: 应用对象
            locator: 窗口定位器，格式为字典
            timeout: 超时时间
        
        返回:
            窗口对象
        
        抛出:
            TimeoutError: 如果超时
        """
        logger.info(f"查找窗口: 应用={app}, 定位器={locator}, 超时={timeout}")
        
        try:
            # 使用pywinauto的window方法查找窗口
            window = app.window(**locator)
            # 等待窗口可见
            window.wait('visible', timeout=timeout)
            return window
        except Exception as e:
            logger.error(f"查找窗口失败: {e}")
            raise TimeoutError(f"超时未找到窗口: {locator}")
    
    def find_element(self, parent: Any, locator: Any, timeout: float = 10.0) -> Any:
        """查找控件
        
        根据定位器查找指定父控件或窗口中的控件
        
        参数:
            parent: 父控件或窗口对象
            locator: 控件定位器
            timeout: 超时时间
        
        返回:
            控件对象
        
        抛出:
            TimeoutError: 如果超时
        """
        logger.info(f"查找控件: 父控件={parent}, 定位器={locator}, 超时={timeout}")
        
        try:
            # 如果定位器是字符串，解析为字典
            if isinstance(locator, str):
                # 简单解析定位器，格式为"类型:属性=值"
                control_type, *attrs = locator.split(':')
                locator_dict = {'control_type': control_type}
                if attrs:
                    for attr in attrs[0].split(';'):
                        if '=' in attr:
                            key, value = attr.split('=', 1)
                            locator_dict[key] = value
            else:
                locator_dict = locator
            
            # 使用pywinauto的child_window方法查找控件
            control = parent.child_window(**locator_dict)
            # 等待控件可见
            control.wait('visible', timeout=timeout)
            return control
        except Exception as e:
            logger.error(f"查找控件失败: {e}")
            raise TimeoutError(f"超时未找到控件: {locator}")
    
    def find_elements(self, parent: Any, locator: Any, timeout: float = 10.0) -> List[Any]:
        """查找多个控件
        
        根据定位器查找指定父控件或窗口中的所有匹配控件
        
        参数:
            parent: 父控件或窗口对象
            locator: 控件定位器
            timeout: 超时时间
        
        返回:
            控件对象列表
        """
        logger.info(f"查找多个控件: 父控件={parent}, 定位器={locator}, 超时={timeout}")
        
        try:
            # 如果定位器是字符串，解析为字典
            if isinstance(locator, str):
                # 简单解析定位器，格式为"类型:属性=值"
                control_type, *attrs = locator.split(':')
                locator_dict = {'control_type': control_type}
                if attrs:
                    for attr in attrs[0].split(';'):
                        if '=' in attr:
                            key, value = attr.split('=', 1)
                            locator_dict[key] = value
            else:
                locator_dict = locator
            
            # 使用pywinauto的children方法查找控件
            controls = parent.children(**locator_dict)
            return controls
        except Exception as e:
            logger.error(f"查找多个控件失败: {e}")
            return []
    
    def click_element(self, element: Any, button: str = "left", clicks: int = 1, interval: float = 0.0) -> bool:
        """点击控件
        
        点击指定的控件
        
        参数:
            element: 控件对象
            button: 鼠标按钮，可选值：left, right, middle
            clicks: 点击次数
            interval: 点击间隔（秒）
        
        返回:
            是否成功
        """
        logger.info(f"点击控件: {element}, 按钮={button}, 次数={clicks}, 间隔={interval}")
        
        try:
            if clicks == 1:
                # 单击
                if button == "left":
                    element.click_input()
                elif button == "right":
                    element.right_click_input()
                elif button == "middle":
                    element.click_input(button="middle")
            elif clicks == 2:
                # 双击
                element.double_click_input()
            return True
        except Exception as e:
            logger.error(f"点击控件失败: {e}")
            return False
    
    def type_text(self, element: Any, text: str, delay: float = 0.0) -> bool:
        """输入文本
        
        向指定的控件输入文本
        
        参数:
            element: 控件对象
            text: 要输入的文本
            delay: 输入延迟（秒）
        
        返回:
            是否成功
        """
        logger.info(f"输入文本: {element}, 文本={text}, 延迟={delay}")
        
        try:
            element.type_keys(text, with_spaces=True, pause=delay)
            return True
        except Exception as e:
            logger.error(f"输入文本失败: {e}")
            return False
    
    def clear_element_text(self, element: Any) -> bool:
        """清空文本
        
        清空指定控件的文本内容
        
        参数:
            element: 控件对象
        
        返回:
            是否成功
        """
        logger.info(f"清空文本: {element}")
        
        try:
            # 选择所有文本并删除
            element.type_keys('^a{DELETE}')
            return True
        except Exception as e:
            logger.error(f"清空文本失败: {e}")
            return False
    
    def get_element_text(self, element: Any) -> Optional[str]:
        """获取文本
        
        获取指定控件的文本内容
        
        参数:
            element: 控件对象
        
        返回:
            控件文本
        """
        logger.info(f"获取文本: {element}")
        
        try:
            return element.window_text()
        except Exception as e:
            logger.error(f"获取文本失败: {e}")
            return None
    
    def set_element_text(self, element: Any, text: str) -> bool:
        """设置文本（直接设置，不模拟输入）
        
        直接设置指定控件的文本内容
        
        参数:
            element: 控件对象
            text: 要设置的文本
        
        返回:
            是否成功
        """
        logger.info(f"设置文本: {element}, 文本={text}")
        
        try:
            element.set_text(text)
            return True
        except Exception as e:
            logger.error(f"设置文本失败: {e}")
            return False
    
    def get_element_attribute(self, element: Any, attribute: str) -> Optional[Any]:
        """获取属性
        
        获取指定控件的指定属性值
        
        参数:
            element: 控件对象
            attribute: 属性名称
        
        返回:
            属性值
        """
        logger.info(f"获取属性: {element}, 属性={attribute}")
        
        try:
            return getattr(element, attribute)
        except Exception as e:
            logger.error(f"获取属性失败: {e}")
            return None
    
    def is_element_enabled(self, element: Any) -> bool:
        """检查控件是否可用
        
        检查指定控件是否可用
        
        参数:
            element: 控件对象
        
        返回:
            是否可用
        """
        logger.info(f"检查控件是否可用: {element}")
        
        try:
            return element.is_enabled()
        except Exception as e:
            logger.error(f"检查控件是否可用失败: {e}")
            return False
    
    def is_element_visible(self, element: Any) -> bool:
        """检查控件是否可见
        
        检查指定控件是否可见
        
        参数:
            element: 控件对象
        
        返回:
            是否可见
        """
        logger.info(f"检查控件是否可见: {element}")
        
        try:
            return element.is_visible()
        except Exception as e:
            logger.error(f"检查控件是否可见失败: {e}")
            return False
    
    def is_element_valid(self, element: Any) -> bool:
        """检查控件是否有效
        
        检查指定控件是否有效
        
        参数:
            element: 控件对象
        
        返回:
            是否有效
        """
        logger.info(f"检查控件是否有效: {element}")
        
        try:
            # 尝试访问控件的基本属性，如果成功则控件有效
            return hasattr(element, 'window_text')
        except Exception as e:
            logger.error(f"检查控件是否有效失败: {e}")
            return False
    
    def hover_element(self, element: Any) -> bool:
        """鼠标悬停
        
        将鼠标悬停在指定控件上
        
        参数:
            element: 控件对象
        
        返回:
            是否成功
        """
        logger.info(f"鼠标悬停: {element}")
        
        try:
            element.hover_input()
            return True
        except Exception as e:
            logger.error(f"鼠标悬停失败: {e}")
            return False
    
    def drag_element_to(self, source_element: Any, target_element: Any) -> bool:
        """拖拽控件到目标位置
        
        将源控件拖拽到目标控件位置
        
        参数:
            source_element: 源控件对象
            target_element: 目标控件对象
        
        返回:
            是否成功
        """
        logger.info(f"拖拽控件: {source_element} 到 {target_element}")
        
        try:
            # 拖拽控件
            source_element.drag_mouse_input(dst=target_element)
            return True
        except Exception as e:
            logger.error(f"拖拽控件失败: {e}")
            return False
    
    def select_element(self, element: Any, value: Any = None, text: Optional[str] = None, index: int = -1) -> bool:
        """选择控件选项（适用于下拉列表、单选按钮等）
        
        选择指定控件的选项
        
        参数:
            element: 控件对象
            value: 选项值
            text: 选项文本
            index: 选项索引
        
        返回:
            是否成功
        """
        logger.info(f"选择控件选项: {element}, 值={value}, 文本={text}, 索引={index}")
        
        try:
            if text is not None:
                # 根据文本选择
                element.select(text)
            elif index >= 0:
                # 根据索引选择
                element.select(index)
            return True
        except Exception as e:
            logger.error(f"选择控件选项失败: {e}")
            return False
    
    def deselect_element(self, element: Any, value: Any = None, text: Optional[str] = None, index: int = -1) -> bool:
        """取消选择控件选项（适用于复选框等）
        
        取消选择指定控件的选项
        
        参数:
            element: 控件对象
            value: 选项值
            text: 选项文本
            index: 选项索引
        
        返回:
            是否成功
        """
        logger.info(f"取消选择控件选项: {element}, 值={value}, 文本={text}, 索引={index}")
        
        try:
            # 对于复选框，直接点击即可取消选择
            element.click_input()
            return True
        except Exception as e:
            logger.error(f"取消选择控件选项失败: {e}")
            return False
    
    def is_element_selected(self, element: Any) -> bool:
        """检查控件是否被选中
        
        检查指定控件是否被选中
        
        参数:
            element: 控件对象
        
        返回:
            是否被选中
        """
        logger.info(f"检查控件是否被选中: {element}")
        
        try:
            return element.get_toggle_state() == 1
        except Exception as e:
            logger.error(f"检查控件是否被选中失败: {e}")
            return False
    
    def click_mouse(self, x: int, y: int, button: str = "left", double: bool = False) -> bool:
        """点击鼠标
        
        在指定位置点击鼠标
        
        参数:
            x: x坐标
            y: y坐标
            button: 鼠标按钮，可选值：left, right, middle
            double: 是否双击
        
        返回:
            是否成功
        """
        logger.info(f"点击鼠标: x={x}, y={y}, 按钮={button}, 双击={double}")
        
        try:
            from pywinauto.mouse import click as mouse_click, double_click as mouse_double_click
            
            if double:
                mouse_double_click(coords=(x, y), button=button)
            else:
                mouse_click(coords=(x, y), button=button)
            return True
        except Exception as e:
            logger.error(f"点击鼠标失败: {e}")
            return False
    
    def move_mouse(self, x: int, y: int, duration: float = 0) -> bool:
        """移动鼠标
        
        将鼠标移动到指定位置
        
        参数:
            x: x坐标
            y: y坐标
            duration: 移动持续时间（秒）
        
        返回:
            是否成功
        """
        logger.info(f"移动鼠标: x={x}, y={y}, 持续时间={duration}")
        
        try:
            from pywinauto.mouse import move as mouse_move
            mouse_move(coords=(x, y))
            return True
        except Exception as e:
            logger.error(f"移动鼠标失败: {e}")
            return False
    
    def drag_mouse(self, start_x: int, start_y: int, end_x: int, end_y: int, duration: float = 0) -> bool:
        """拖拽鼠标
        
        从起始位置拖拽鼠标到结束位置
        
        参数:
            start_x: 起始x坐标
            start_y: 起始y坐标
            end_x: 结束x坐标
            end_y: 结束y坐标
            duration: 拖拽持续时间（秒）
        
        返回:
            是否成功
        """
        logger.info(f"拖拽鼠标: 起始({start_x}, {start_y}) 到 结束({end_x}, {end_y}), 持续时间={duration}")
        
        try:
            from pywinauto.mouse import drag as mouse_drag
            mouse_drag(coords=(start_x, start_y), dst=(end_x, end_y))
            return True
        except Exception as e:
            logger.error(f"拖拽鼠标失败: {e}")
            return False
    
    def scroll_mouse(self, x: int, y: int, clicks: int, horizontal: bool = False) -> bool:
        """滚动鼠标
        
        在指定位置滚动鼠标
        
        参数:
            x: x坐标
            y: y坐标
            clicks: 滚动距离，正数向上/向右，负数向下/向左
            horizontal: 是否水平滚动
        
        返回:
            是否成功
        """
        logger.info(f"滚动鼠标: x={x}, y={y}, 距离={clicks}, 水平={horizontal}")
        
        try:
            from pywinauto.mouse import scroll as mouse_scroll
            mouse_scroll(coords=(x, y), wheel_dist=clicks, horizontal=horizontal)
            return True
        except Exception as e:
            logger.error(f"滚动鼠标失败: {e}")
            return False
    
    def press_mouse(self, x: int, y: int, button: str = "left") -> bool:
        """按下鼠标按钮
        
        在指定位置按下鼠标按钮
        
        参数:
            x: x坐标
            y: y坐标
            button: 鼠标按钮，可选值：left, right, middle
        
        返回:
            是否成功
        """
        logger.info(f"按下鼠标按钮: x={x}, y={y}, 按钮={button}")
        
        try:
            from pywinauto.mouse import press as mouse_press
            mouse_press(coords=(x, y), button=button)
            return True
        except Exception as e:
            logger.error(f"按下鼠标按钮失败: {e}")
            return False
    
    def release_mouse(self, x: int, y: int, button: str = "left") -> bool:
        """释放鼠标按钮
        
        在指定位置释放鼠标按钮
        
        参数:
            x: x坐标
            y: y坐标
            button: 鼠标按钮，可选值：left, right, middle
        
        返回:
            是否成功
        """
        logger.info(f"释放鼠标按钮: x={x}, y={y}, 按钮={button}")
        
        try:
            from pywinauto.mouse import release as mouse_release
            mouse_release(coords=(x, y), button=button)
            return True
        except Exception as e:
            logger.error(f"释放鼠标按钮失败: {e}")
            return False
    
    def get_mouse_position(self) -> tuple:
        """获取鼠标位置
        
        获取当前鼠标的位置
        
        返回:
            包含x和y坐标的元组
        """
        logger.info("获取鼠标位置")
        
        try:
            from pywinauto.mouse import get_position
            return get_position()
        except Exception as e:
            logger.error(f"获取鼠标位置失败: {e}")
            return (0, 0)
    
    def press_key(self, key: str, modifier: Optional[str] = None) -> bool:
        """按下键盘按键
        
        按下指定的键盘按键
        
        参数:
            key: 按键名称
            modifier: 修饰键，可选值：Ctrl, Alt, Shift, Win
        
        返回:
            是否成功
        """
        logger.info(f"按下键盘按键: 键={key}, 修饰键={modifier}")
        
        try:
            from pywinauto.keyboard import press as keyboard_press
            
            if modifier:
                keyboard_press(f"{modifier}+{key}")
            else:
                keyboard_press(key)
            return True
        except Exception as e:
            logger.error(f"按下键盘按键失败: {e}")
            return False
    
    def release_key(self, key: str, modifier: Optional[str] = None) -> bool:
        """释放键盘按键
        
        释放指定的键盘按键
        
        参数:
            key: 按键名称
            modifier: 修饰键，可选值：Ctrl, Alt, Shift, Win
        
        返回:
            是否成功
        """
        logger.info(f"释放键盘按键: 键={key}, 修饰键={modifier}")
        
        try:
            from pywinauto.keyboard import release as keyboard_release
            
            if modifier:
                keyboard_release(f"{modifier}+{key}")
            else:
                keyboard_release(key)
            return True
        except Exception as e:
            logger.error(f"释放键盘按键失败: {e}")
            return False
    
    def combo_keys(self, keys: str) -> bool:
        """组合按键
        
        按下并释放指定的组合按键
        
        参数:
            keys: 组合按键，格式为"Ctrl+C"
        
        返回:
            是否成功
        """
        logger.info(f"组合按键: {keys}")
        
        try:
            from pywinauto.keyboard import send_keys as keyboard_send_keys
            keyboard_send_keys(keys)
            return True
        except Exception as e:
            logger.error(f"组合按键失败: {e}")
            return False
    
    def take_screenshot(self, file_path: str, window: Any = None) -> str:
        """截图
        
        截取指定窗口或整个屏幕的截图
        
        参数:
            file_path: 截图保存路径
            window: 窗口对象，如果为None则截取整个屏幕
        
        返回:
            截图文件路径
        """
        logger.info(f"截图: 文件路径={file_path}, 窗口={window}")
        
        try:
            if window:
                # 截取指定窗口
                window.capture_as_image().save(file_path)
            else:
                # 截取整个屏幕
                from pywinauto.screenshot import grab
                grab().save(file_path)
            return file_path
        except Exception as e:
            logger.error(f"截图失败: {e}")
            return ""
