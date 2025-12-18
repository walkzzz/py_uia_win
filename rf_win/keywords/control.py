#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
控件管理关键字模块
提供控件的查找、点击、输入等关键字
"""

from robot.api.deco import keyword, library
from ..services.control_service import ControlService
from ..utils.logger import logger

@library(scope='GLOBAL', version='1.0.0')
class ControlKeywords:
    """控件管理关键字类
    
    提供控件的查找、点击、输入等关键字，用于Robot Framework测试用例
    """
    
    def __init__(self):
        """初始化控件服务实例"""
        self.control_service = ControlService()
    
    @keyword(name='查找控件', tags=['控件管理'])
    def find_control(self, locator, window_title=None, app_alias=None, timeout=None):
        """查找控件
        
        根据定位器查找指定窗口中的控件
        
        参数:
            locator: 控件定位器，格式为"类型:属性=值"
            window_title: 窗口标题，可以是完整标题或正则表达式
            app_alias: 应用程序的别名
            timeout: 查找超时时间，单位为秒
        
        返回:
            控件实例
        
        示例:
            | ${button} | 查找控件 | Button:name=确定 | 窗口标题=Untitled - Notepad |
        """
        logger.info(f"查找控件: 定位器={locator}, 窗口标题={window_title}, 应用别名={app_alias}, 超时={timeout}")
        return self.control_service.find_control(locator, window_title, app_alias, timeout)
    
    @keyword(name='查找所有控件', tags=['控件管理'])
    def find_all_controls(self, locator, window_title=None, app_alias=None, timeout=None):
        """查找所有匹配的控件
        
        根据定位器查找指定窗口中的所有匹配控件
        
        参数:
            locator: 控件定位器，格式为"类型:属性=值"
            window_title: 窗口标题，可以是完整标题或正则表达式
            app_alias: 应用程序的别名
            timeout: 查找超时时间，单位为秒
        
        返回:
            控件实例列表
        
        示例:
            | ${buttons} | 查找所有控件 | Button: | 窗口标题=Untitled - Notepad |
        """
        logger.info(f"查找所有控件: 定位器={locator}, 窗口标题={window_title}, 应用别名={app_alias}, 超时={timeout}")
        return self.control_service.find_all_controls(locator, window_title, app_alias, timeout)
    
    @keyword(name='点击控件', tags=['控件管理'])
    def click_control(self, locator, window_title=None, app_alias=None, button='left', double=False, timeout=None):
        """点击控件
        
        点击指定的控件
        
        参数:
            locator: 控件定位器，格式为"类型:属性=值"
            window_title: 窗口标题，可以是完整标题或正则表达式
            app_alias: 应用程序的别名
            button: 鼠标按钮，可选值为'left'、'right'、'middle'
            double: 是否双击，默认为False
            timeout: 查找超时时间，单位为秒
        
        示例:
            | 点击控件 | Button:name=确定 | 窗口标题=Untitled - Notepad |
            | 点击控件 | Button:name=确定 | 窗口标题=Untitled - Notepad | 按钮=right |
            | 点击控件 | Button:name=确定 | 窗口标题=Untitled - Notepad | 双击=True |
        """
        logger.info(f"点击控件: 定位器={locator}, 窗口标题={window_title}, 应用别名={app_alias}, 按钮={button}, 双击={double}, 超时={timeout}")
        return self.control_service.click_control(locator, window_title, app_alias, button, double, timeout)
    
    @keyword(name='右键点击控件', tags=['控件管理'])
    def right_click_control(self, locator, window_title=None, app_alias=None, timeout=None):
        """右键点击控件
        
        右键点击指定的控件
        
        参数:
            locator: 控件定位器，格式为"类型:属性=值"
            window_title: 窗口标题，可以是完整标题或正则表达式
            app_alias: 应用程序的别名
            timeout: 查找超时时间，单位为秒
        
        示例:
            | 右键点击控件 | Button:name=确定 | 窗口标题=Untitled - Notepad |
        """
        logger.info(f"右键点击控件: 定位器={locator}, 窗口标题={window_title}, 应用别名={app_alias}, 超时={timeout}")
        return self.control_service.click_control(locator, window_title, app_alias, 'right', False, timeout)
    
    @keyword(name='双击控件', tags=['控件管理'])
    def double_click_control(self, locator, window_title=None, app_alias=None, timeout=None):
        """双击控件
        
        双击指定的控件
        
        参数:
            locator: 控件定位器，格式为"类型:属性=值"
            window_title: 窗口标题，可以是完整标题或正则表达式
            app_alias: 应用程序的别名
            timeout: 查找超时时间，单位为秒
        
        示例:
            | 双击控件 | Button:name=确定 | 窗口标题=Untitled - Notepad |
        """
        logger.info(f"双击控件: 定位器={locator}, 窗口标题={window_title}, 应用别名={app_alias}, 超时={timeout}")
        return self.control_service.click_control(locator, window_title, app_alias, 'left', True, timeout)
    
    @keyword(name='控件输入文本', tags=['控件管理'])
    def set_control_text(self, locator, text, window_title=None, app_alias=None, timeout=None, clear_first=True):
        """控件输入文本
        
        向指定控件输入文本
        
        参数:
            locator: 控件定位器，格式为"类型:属性=值"
            text: 要输入的文本
            window_title: 窗口标题，可以是完整标题或正则表达式
            app_alias: 应用程序的别名
            timeout: 查找超时时间，单位为秒
            clear_first: 是否先清空控件内容，默认为True
        
        示例:
            | 控件输入文本 | Edit:name=文本编辑框 | Hello World | 窗口标题=Untitled - Notepad |
            | 控件输入文本 | Edit:name=文本编辑框 | Hello | 窗口标题=Untitled - Notepad | 清空=False |
        """
        logger.info(f"控件输入文本: 定位器={locator}, 文本={text}, 窗口标题={window_title}, 应用别名={app_alias}, 超时={timeout}, 清空={clear_first}")
        return self.control_service.set_control_text(locator, text, window_title, app_alias, timeout, clear_first)
    
    @keyword(name='获取控件文本', tags=['控件管理'])
    def get_control_text(self, locator, window_title=None, app_alias=None, timeout=None):
        """获取控件文本
        
        获取指定控件的文本内容
        
        参数:
            locator: 控件定位器，格式为"类型:属性=值"
            window_title: 窗口标题，可以是完整标题或正则表达式
            app_alias: 应用程序的别名
            timeout: 查找超时时间，单位为秒
        
        返回:
            控件的文本内容
        
        示例:
            | ${text} | 获取控件文本 | Edit:name=文本编辑框 | 窗口标题=Untitled - Notepad |
        """
        logger.info(f"获取控件文本: 定位器={locator}, 窗口标题={window_title}, 应用别名={app_alias}, 超时={timeout}")
        return self.control_service.get_control_text(locator, window_title, app_alias, timeout)
    
    @keyword(name='清空控件文本', tags=['控件管理'])
    def clear_control_text(self, locator, window_title=None, app_alias=None, timeout=None):
        """清空控件文本
        
        清空指定控件的文本内容
        
        参数:
            locator: 控件定位器，格式为"类型:属性=值"
            window_title: 窗口标题，可以是完整标题或正则表达式
            app_alias: 应用程序的别名
            timeout: 查找超时时间，单位为秒
        
        示例:
            | 清空控件文本 | Edit:name=文本编辑框 | 窗口标题=Untitled - Notepad |
        """
        logger.info(f"清空控件文本: 定位器={locator}, 窗口标题={window_title}, 应用别名={app_alias}, 超时={timeout}")
        return self.control_service.clear_control_text(locator, window_title, app_alias, timeout)
    
    @keyword(name='选择控件项', tags=['控件管理'])
    def select_control_item(self, locator, item, window_title=None, app_alias=None, timeout=None):
        """选择控件项
        
        选择下拉列表或列表框中的项
        
        参数:
            locator: 控件定位器，格式为"类型:属性=值"
            item: 要选择的项，可以是文本或索引
            window_title: 窗口标题，可以是完整标题或正则表达式
            app_alias: 应用程序的别名
            timeout: 查找超时时间，单位为秒
        
        示例:
            | 选择控件项 | ComboBox:name=下拉列表 | 选项1 | 窗口标题=Untitled - Notepad |
            | 选择控件项 | ListBox:name=列表框 | 0 | 窗口标题=Untitled - Notepad |
        """
        logger.info(f"选择控件项: 定位器={locator}, 项={item}, 窗口标题={window_title}, 应用别名={app_alias}, 超时={timeout}")
        return self.control_service.select_control_item(locator, item, window_title, app_alias, timeout)
    
    @keyword(name='获取控件项', tags=['控件管理'])
    def get_control_items(self, locator, window_title=None, app_alias=None, timeout=None):
        """获取控件项列表
        
        获取下拉列表或列表框中的所有项
        
        参数:
            locator: 控件定位器，格式为"类型:属性=值"
            window_title: 窗口标题，可以是完整标题或正则表达式
            app_alias: 应用程序的别名
            timeout: 查找超时时间，单位为秒
        
        返回:
            控件项列表
        
        示例:
            | ${items} | 获取控件项 | ComboBox:name=下拉列表 | 窗口标题=Untitled - Notepad |
        """
        logger.info(f"获取控件项: 定位器={locator}, 窗口标题={window_title}, 应用别名={app_alias}, 超时={timeout}")
        return self.control_service.get_control_items(locator, window_title, app_alias, timeout)
    
    @keyword(name='控件是否存在', tags=['控件管理'])
    def is_control_exists(self, locator, window_title=None, app_alias=None, timeout=None):
        """检查控件是否存在
        
        检查指定的控件是否存在
        
        参数:
            locator: 控件定位器，格式为"类型:属性=值"
            window_title: 窗口标题，可以是完整标题或正则表达式
            app_alias: 应用程序的别名
            timeout: 查找超时时间，单位为秒
        
        返回:
            True如果控件存在，否则返回False
        
        示例:
            | ${exists} | 控件是否存在 | Button:name=确定 | 窗口标题=Untitled - Notepad |
        """
        logger.info(f"检查控件是否存在: 定位器={locator}, 窗口标题={window_title}, 应用别名={app_alias}, 超时={timeout}")
        return self.control_service.is_control_exists(locator, window_title, app_alias, timeout)
    
    @keyword(name='控件是否可见', tags=['控件管理'])
    def is_control_visible(self, locator, window_title=None, app_alias=None, timeout=None):
        """检查控件是否可见
        
        检查指定的控件是否可见
        
        参数:
            locator: 控件定位器，格式为"类型:属性=值"
            window_title: 窗口标题，可以是完整标题或正则表达式
            app_alias: 应用程序的别名
            timeout: 查找超时时间，单位为秒
        
        返回:
            True如果控件可见，否则返回False
        
        示例:
            | ${visible} | 控件是否可见 | Button:name=确定 | 窗口标题=Untitled - Notepad |
        """
        logger.info(f"检查控件是否可见: 定位器={locator}, 窗口标题={window_title}, 应用别名={app_alias}, 超时={timeout}")
        return self.control_service.is_control_visible(locator, window_title, app_alias, timeout)
    
    @keyword(name='控件是否启用', tags=['控件管理'])
    def is_control_enabled(self, locator, window_title=None, app_alias=None, timeout=None):
        """检查控件是否启用
        
        检查指定的控件是否启用
        
        参数:
            locator: 控件定位器，格式为"类型:属性=值"
            window_title: 窗口标题，可以是完整标题或正则表达式
            app_alias: 应用程序的别名
            timeout: 查找超时时间，单位为秒
        
        返回:
            True如果控件启用，否则返回False
        
        示例:
            | ${enabled} | 控件是否启用 | Button:name=确定 | 窗口标题=Untitled - Notepad |
        """
        logger.info(f"检查控件是否启用: 定位器={locator}, 窗口标题={window_title}, 应用别名={app_alias}, 超时={timeout}")
        return self.control_service.is_control_enabled(locator, window_title, app_alias, timeout)
    
    @keyword(name='获取控件属性', tags=['控件管理'])
    def get_control_property(self, locator, property_name, window_title=None, app_alias=None, timeout=None):
        """获取控件属性
        
        获取指定控件的指定属性值
        
        参数:
            locator: 控件定位器，格式为"类型:属性=值"
            property_name: 属性名称
            window_title: 窗口标题，可以是完整标题或正则表达式
            app_alias: 应用程序的别名
            timeout: 查找超时时间，单位为秒
        
        返回:
            控件属性值
        
        示例:
            | ${value} | 获取控件属性 | Edit:name=文本编辑框 | value | 窗口标题=Untitled - Notepad |
        """
        logger.info(f"获取控件属性: 定位器={locator}, 属性名={property_name}, 窗口标题={window_title}, 应用别名={app_alias}, 超时={timeout}")
        return self.control_service.get_control_property(locator, property_name, window_title, app_alias, timeout)
    
    @keyword(name='设置控件属性', tags=['控件管理'])
    def set_control_property(self, locator, property_name, value, window_title=None, app_alias=None, timeout=None):
        """设置控件属性
        
        设置指定控件的指定属性值
        
        参数:
            locator: 控件定位器，格式为"类型:属性=值"
            property_name: 属性名称
            value: 要设置的属性值
            window_title: 窗口标题，可以是完整标题或正则表达式
            app_alias: 应用程序的别名
            timeout: 查找超时时间，单位为秒
        
        示例:
            | 设置控件属性 | Edit:name=文本编辑框 | value | New Value | 窗口标题=Untitled - Notepad |
        """
        logger.info(f"设置控件属性: 定位器={locator}, 属性名={property_name}, 值={value}, 窗口标题={window_title}, 应用别名={app_alias}, 超时={timeout}")
        return self.control_service.set_control_property(locator, property_name, value, window_title, app_alias, timeout)
