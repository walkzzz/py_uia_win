#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
操作关键字模块
提供鼠标、键盘等操作关键字
"""

from robot.api.deco import keyword, library
from ..services.operation_service import OperationService
from ..utils.logger import logger

@library(scope='GLOBAL', version='1.0.0')
class OperationKeywords:
    """操作关键字类
    
    提供鼠标、键盘等操作关键字，用于Robot Framework测试用例
    """
    
    def __init__(self):
        """初始化操作服务实例"""
        self.operation_service = OperationService()
    
    @keyword(name='点击鼠标', tags=['鼠标操作'])
    def click_mouse(self, x, y, button='left', double=False):
        """点击鼠标
        
        在指定位置点击鼠标
        
        参数:
            x: 点击位置的x坐标
            y: 点击位置的y坐标
            button: 鼠标按钮，可选值为'left'、'right'、'middle'
            double: 是否双击，默认为False
        
        示例:
            | 点击鼠标 | 100 | 200 |
            | 点击鼠标 | 100 | 200 | 按钮=right |
            | 点击鼠标 | 100 | 200 | 双击=True |
        """
        logger.info(f"点击鼠标: x={x}, y={y}, 按钮={button}, 双击={double}")
        return self.operation_service.click_mouse(x, y, button, double)
    
    @keyword(name='右键点击鼠标', tags=['鼠标操作'])
    def right_click_mouse(self, x, y):
        """右键点击鼠标
        
        在指定位置右键点击鼠标
        
        参数:
            x: 点击位置的x坐标
            y: 点击位置的y坐标
        
        示例:
            | 右键点击鼠标 | 100 | 200 |
        """
        logger.info(f"右键点击鼠标: x={x}, y={y}")
        return self.operation_service.click_mouse(x, y, 'right')
    
    @keyword(name='双击鼠标', tags=['鼠标操作'])
    def double_click_mouse(self, x, y):
        """双击鼠标
        
        在指定位置双击鼠标
        
        参数:
            x: 点击位置的x坐标
            y: 点击位置的y坐标
        
        示例:
            | 双击鼠标 | 100 | 200 |
        """
        logger.info(f"双击鼠标: x={x}, y={y}")
        return self.operation_service.click_mouse(x, y, 'left', True)
    
    @keyword(name='移动鼠标', tags=['鼠标操作'])
    def move_mouse(self, x, y, duration=0):
        """移动鼠标
        
        将鼠标移动到指定位置
        
        参数:
            x: 目标位置的x坐标
            y: 目标位置的y坐标
            duration: 移动持续时间，单位为秒
        
        示例:
            | 移动鼠标 | 100 | 200 |
            | 移动鼠标 | 100 | 200 | 持续时间=0.5 |
        """
        logger.info(f"移动鼠标: x={x}, y={y}, 持续时间={duration}")
        return self.operation_service.move_mouse(x, y, duration)
    
    @keyword(name='拖拽鼠标', tags=['鼠标操作'])
    def drag_mouse(self, start_x, start_y, end_x, end_y, duration=0):
        """拖拽鼠标
        
        从起始位置拖拽鼠标到结束位置
        
        参数:
            start_x: 起始位置的x坐标
            start_y: 起始位置的y坐标
            end_x: 结束位置的x坐标
            end_y: 结束位置的y坐标
            duration: 拖拽持续时间，单位为秒
        
        示例:
            | 拖拽鼠标 | 100 | 200 | 300 | 400 |
            | 拖拽鼠标 | 100 | 200 | 300 | 400 | 持续时间=1 |
        """
        logger.info(f"拖拽鼠标: 起始x={start_x}, 起始y={start_y}, 结束x={end_x}, 结束y={end_y}, 持续时间={duration}")
        return self.operation_service.drag_mouse(start_x, start_y, end_x, end_y, duration)
    
    @keyword(name='滚动鼠标', tags=['鼠标操作'])
    def scroll_mouse(self, x, y, clicks, horizontal=False):
        """滚动鼠标
        
        在指定位置滚动鼠标
        
        参数:
            x: 滚动位置的x坐标
            y: 滚动位置的y坐标
            clicks: 滚动的距离，正数向上/向右，负数向下/向左
            horizontal: 是否水平滚动，默认为False（垂直滚动）
        
        示例:
            | 滚动鼠标 | 100 | 200 | -10 |
            | 滚动鼠标 | 100 | 200 | 5 | 水平=True |
        """
        logger.info(f"滚动鼠标: x={x}, y={y}, 距离={clicks}, 水平={horizontal}")
        return self.operation_service.scroll_mouse(x, y, clicks, horizontal)
    
    @keyword(name='按下鼠标', tags=['鼠标操作'])
    def press_mouse(self, x, y, button='left'):
        """按下鼠标
        
        在指定位置按下鼠标按钮
        
        参数:
            x: 按下位置的x坐标
            y: 按下位置的y坐标
            button: 鼠标按钮，可选值为'left'、'right'、'middle'
        
        示例:
            | 按下鼠标 | 100 | 200 |
        """
        logger.info(f"按下鼠标: x={x}, y={y}, 按钮={button}")
        return self.operation_service.press_mouse(x, y, button)
    
    @keyword(name='释放鼠标', tags=['鼠标操作'])
    def release_mouse(self, x, y, button='left'):
        """释放鼠标
        
        在指定位置释放鼠标按钮
        
        参数:
            x: 释放位置的x坐标
            y: 释放位置的y坐标
            button: 鼠标按钮，可选值为'left'、'right'、'middle'
        
        示例:
            | 释放鼠标 | 100 | 200 |
        """
        logger.info(f"释放鼠标: x={x}, y={y}, 按钮={button}")
        return self.operation_service.release_mouse(x, y, button)
    
    @keyword(name='获取鼠标位置', tags=['鼠标操作'])
    def get_mouse_position(self):
        """获取鼠标位置
        
        获取当前鼠标的位置
        
        返回:
            包含x和y坐标的字典
        
        示例:
            | ${pos} | 获取鼠标位置 |
        """
        logger.info("获取鼠标位置")
        return self.operation_service.get_mouse_position()
    
    @keyword(name='输入文本', tags=['键盘操作'])
    def type_text(self, text, delay=0):
        """输入文本
        
        输入指定的文本
        
        参数:
            text: 要输入的文本
            delay: 按键之间的延迟，单位为秒
        
        示例:
            | 输入文本 | Hello World |
            | 输入文本 | Hello World | 延迟=0.1 |
        """
        logger.info(f"输入文本: {text}, 延迟={delay}")
        return self.operation_service.type_text(text, delay)
    
    @keyword(name='按下按键', tags=['键盘操作'])
    def press_key(self, key, modifier=None):
        """按下按键
        
        按下指定的按键
        
        参数:
            key: 要按下的按键
            modifier: 修饰键，可选值为'Ctrl'、'Alt'、'Shift'、'Win'
        
        示例:
            | 按下按键 | Enter |
            | 按下按键 | C | 修饰键=Ctrl |
        """
        logger.info(f"按下按键: 键={key}, 修饰键={modifier}")
        return self.operation_service.press_key(key, modifier)
    
    @keyword(name='释放按键', tags=['键盘操作'])
    def release_key(self, key, modifier=None):
        """释放按键
        
        释放指定的按键
        
        参数:
            key: 要释放的按键
            modifier: 修饰键，可选值为'Ctrl'、'Alt'、'Shift'、'Win'
        
        示例:
            | 释放按键 | Enter |
            | 释放按键 | C | 修饰键=Ctrl |
        """
        logger.info(f"释放按键: 键={key}, 修饰键={modifier}")
        return self.operation_service.release_key(key, modifier)
    
    @keyword(name='组合按键', tags=['键盘操作'])
    def combo_keys(self, keys):
        """组合按键
        
        按下并释放指定的组合按键
        
        参数:
            keys: 组合按键，格式为'Ctrl+C'、'Alt+F4'等
        
        示例:
            | 组合按键 | Ctrl+C |
            | 组合按键 | Alt+F4 |
        """
        logger.info(f"组合按键: {keys}")
        return self.operation_service.combo_keys(keys)
    
    @keyword(name='等待', tags=['等待操作'])
    def wait(self, seconds):
        """等待
        
        等待指定的时间
        
        参数:
            seconds: 等待时间，单位为秒
        
        示例:
            | 等待 | 2 |
        """
        logger.info(f"等待: {seconds}秒")
        return self.operation_service.wait(seconds)
    
    @keyword(name='等待控件存在', tags=['等待操作'])
    def wait_for_control_exists(self, locator, window_title=None, app_alias=None, timeout=30):
        """等待控件存在
        
        等待指定的控件存在
        
        参数:
            locator: 控件定位器，格式为"类型:属性=值"
            window_title: 窗口标题，可以是完整标题或正则表达式
            app_alias: 应用程序的别名
            timeout: 等待超时时间，单位为秒
        
        示例:
            | 等待控件存在 | Button:name=确定 | 窗口标题=Untitled - Notepad | 超时=10 |
        """
        logger.info(f"等待控件存在: 定位器={locator}, 窗口标题={window_title}, 应用别名={app_alias}, 超时={timeout}")
        return self.operation_service.wait_for_control_exists(locator, window_title, app_alias, timeout)
    
    @keyword(name='等待控件可见', tags=['等待操作'])
    def wait_for_control_visible(self, locator, window_title=None, app_alias=None, timeout=30):
        """等待控件可见
        
        等待指定的控件可见
        
        参数:
            locator: 控件定位器，格式为"类型:属性=值"
            window_title: 窗口标题，可以是完整标题或正则表达式
            app_alias: 应用程序的别名
            timeout: 等待超时时间，单位为秒
        
        示例:
            | 等待控件可见 | Button:name=确定 | 窗口标题=Untitled - Notepad | 超时=10 |
        """
        logger.info(f"等待控件可见: 定位器={locator}, 窗口标题={window_title}, 应用别名={app_alias}, 超时={timeout}")
        return self.operation_service.wait_for_control_visible(locator, window_title, app_alias, timeout)
    
    @keyword(name='等待控件启用', tags=['等待操作'])
    def wait_for_control_enabled(self, locator, window_title=None, app_alias=None, timeout=30):
        """等待控件启用
        
        等待指定的控件启用
        
        参数:
            locator: 控件定位器，格式为"类型:属性=值"
            window_title: 窗口标题，可以是完整标题或正则表达式
            app_alias: 应用程序的别名
            timeout: 等待超时时间，单位为秒
        
        示例:
            | 等待控件启用 | Button:name=确定 | 窗口标题=Untitled - Notepad | 超时=10 |
        """
        logger.info(f"等待控件启用: 定位器={locator}, 窗口标题={window_title}, 应用别名={app_alias}, 超时={timeout}")
        return self.operation_service.wait_for_control_enabled(locator, window_title, app_alias, timeout)
    
    @keyword(name='等待窗口存在', tags=['等待操作'])
    def wait_for_window_exists(self, window_title, app_alias=None, timeout=30):
        """等待窗口存在
        
        等待指定的窗口存在
        
        参数:
            window_title: 窗口标题，可以是完整标题或正则表达式
            app_alias: 应用程序的别名
            timeout: 等待超时时间，单位为秒
        
        示例:
            | 等待窗口存在 | Untitled - Notepad | 超时=10 |
        """
        logger.info(f"等待窗口存在: 窗口标题={window_title}, 应用别名={app_alias}, 超时={timeout}")
        return self.operation_service.wait_for_window_exists(window_title, app_alias, timeout)
    
    @keyword(name='截图', tags=['截图操作'])
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
        
        示例:
            | ${screenshot} | 截图 |
            | ${screenshot} | 截图 | 文件名=test | 文件夹=./screenshots |
            | ${screenshot} | 截图 | 窗口标题=Untitled - Notepad |
        """
        logger.info(f"截图: 文件名={filename}, 文件夹={folder}, 窗口标题={window_title}, 应用别名={app_alias}")
        return self.operation_service.take_screenshot(filename, folder, window_title, app_alias)
