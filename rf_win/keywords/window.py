#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
窗口管理关键字模块
提供窗口的获取、激活、最大化、最小化等关键字
"""

from robot.api.deco import keyword, library
from ..services.window_service import WindowService
from ..utils.logger import logger

@library(scope='GLOBAL', version='1.0.0')
class WindowKeywords:
    """窗口管理关键字类
    
    提供窗口的获取、激活、最大化、最小化等关键字，用于Robot Framework测试用例
    """
    
    def __init__(self):
        """初始化窗口服务实例"""
        self.window_service = WindowService()
    
    @keyword(name='获取当前窗口', tags=['窗口管理'])
    def get_current_window(self, app_alias=None):
        """获取当前活动窗口
        
        获取指定应用程序的当前活动窗口，如果不指定应用别名，则获取当前活动应用的窗口
        
        参数:
            app_alias: 应用程序的别名
        
        返回:
            窗口实例
        
        示例:
            | ${window} | 获取当前窗口 | 别名=notepad++ |
        """
        logger.info(f"获取当前窗口: 应用别名={app_alias}")
        return self.window_service.get_current_window(app_alias)
    
    @keyword(name='获取所有窗口', tags=['窗口管理'])
    def get_all_windows(self, app_alias=None):
        """获取所有窗口
        
        获取指定应用程序的所有窗口，如果不指定应用别名，则获取当前活动应用的所有窗口
        
        参数:
            app_alias: 应用程序的别名
        
        返回:
            窗口实例列表
        
        示例:
            | ${windows} | 获取所有窗口 | 别名=notepad++ |
        """
        logger.info(f"获取所有窗口: 应用别名={app_alias}")
        return self.window_service.get_all_windows(app_alias)
    
    @keyword(name='切换窗口', tags=['窗口管理'])
    def switch_window(self, window_title=None, app_alias=None, index=0):
        """切换窗口
        
        切换到指定标题或索引的窗口
        
        参数:
            window_title: 窗口标题，可以是完整标题或正则表达式
            app_alias: 应用程序的别名
            index: 窗口索引，默认为0
        
        返回:
            切换后的窗口实例
        
        示例:
            | ${window} | 切换窗口 | 窗口标题=Untitled - Notepad |
            | ${window} | 切换窗口 | 索引=1 | 别名=notepad++ |
        """
        logger.info(f"切换窗口: 窗口标题={window_title}, 应用别名={app_alias}, 索引={index}")
        return self.window_service.switch_window(window_title, app_alias, index)
    
    @keyword(name='激活窗口', tags=['窗口管理'])
    def activate_window(self, window_title=None, app_alias=None, index=0):
        """激活窗口
        
        激活指定标题或索引的窗口
        
        参数:
            window_title: 窗口标题，可以是完整标题或正则表达式
            app_alias: 应用程序的别名
            index: 窗口索引，默认为0
        
        示例:
            | 激活窗口 | 窗口标题=Untitled - Notepad |
        """
        logger.info(f"激活窗口: 窗口标题={window_title}, 应用别名={app_alias}, 索引={index}")
        return self.window_service.activate_window(window_title, app_alias, index)
    
    @keyword(name='关闭窗口', tags=['窗口管理'])
    def close_window(self, window_title=None, app_alias=None, index=0):
        """关闭窗口
        
        关闭指定标题或索引的窗口
        
        参数:
            window_title: 窗口标题，可以是完整标题或正则表达式
            app_alias: 应用程序的别名
            index: 窗口索引，默认为0
        
        示例:
            | 关闭窗口 | 窗口标题=Untitled - Notepad |
        """
        logger.info(f"关闭窗口: 窗口标题={window_title}, 应用别名={app_alias}, 索引={index}")
        return self.window_service.close_window(window_title, app_alias, index)
    
    @keyword(name='窗口最大化', tags=['窗口管理'])
    def maximize_window(self, window_title=None, app_alias=None, index=0):
        """窗口最大化
        
        将指定标题或索引的窗口最大化
        
        参数:
            window_title: 窗口标题，可以是完整标题或正则表达式
            app_alias: 应用程序的别名
            index: 窗口索引，默认为0
        
        示例:
            | 窗口最大化 | 窗口标题=Untitled - Notepad |
        """
        logger.info(f"窗口最大化: 窗口标题={window_title}, 应用别名={app_alias}, 索引={index}")
        return self.window_service.maximize_window(window_title, app_alias, index)
    
    @keyword(name='窗口最小化', tags=['窗口管理'])
    def minimize_window(self, window_title=None, app_alias=None, index=0):
        """窗口最小化
        
        将指定标题或索引的窗口最小化
        
        参数:
            window_title: 窗口标题，可以是完整标题或正则表达式
            app_alias: 应用程序的别名
            index: 窗口索引，默认为0
        
        示例:
            | 窗口最小化 | 窗口标题=Untitled - Notepad |
        """
        logger.info(f"窗口最小化: 窗口标题={window_title}, 应用别名={app_alias}, 索引={index}")
        return self.window_service.minimize_window(window_title, app_alias, index)
    
    @keyword(name='窗口还原', tags=['窗口管理'])
    def restore_window(self, window_title=None, app_alias=None, index=0):
        """窗口还原
        
        将指定标题或索引的窗口还原到正常大小
        
        参数:
            window_title: 窗口标题，可以是完整标题或正则表达式
            app_alias: 应用程序的别名
            index: 窗口索引，默认为0
        
        示例:
            | 窗口还原 | 窗口标题=Untitled - Notepad |
        """
        logger.info(f"窗口还原: 窗口标题={window_title}, 应用别名={app_alias}, 索引={index}")
        return self.window_service.restore_window(window_title, app_alias, index)
    
    @keyword(name='移动窗口', tags=['窗口管理'])
    def move_window(self, x, y, window_title=None, app_alias=None, index=0):
        """移动窗口
        
        将指定标题或索引的窗口移动到指定位置
        
        参数:
            x: 目标x坐标
            y: 目标y坐标
            window_title: 窗口标题，可以是完整标题或正则表达式
            app_alias: 应用程序的别名
            index: 窗口索引，默认为0
        
        示例:
            | 移动窗口 | 100 | 200 | 窗口标题=Untitled - Notepad |
        """
        logger.info(f"移动窗口: x={x}, y={y}, 窗口标题={window_title}, 应用别名={app_alias}, 索引={index}")
        return self.window_service.move_window(x, y, window_title, app_alias, index)
    
    @keyword(name='调整窗口大小', tags=['窗口管理'])
    def resize_window(self, width, height, window_title=None, app_alias=None, index=0):
        """调整窗口大小
        
        调整指定标题或索引的窗口大小
        
        参数:
            width: 目标宽度
            height: 目标高度
            window_title: 窗口标题，可以是完整标题或正则表达式
            app_alias: 应用程序的别名
            index: 窗口索引，默认为0
        
        示例:
            | 调整窗口大小 | 800 | 600 | 窗口标题=Untitled - Notepad |
        """
        logger.info(f"调整窗口大小: 宽度={width}, 高度={height}, 窗口标题={window_title}, 应用别名={app_alias}, 索引={index}")
        return self.window_service.resize_window(width, height, window_title, app_alias, index)
    
    @keyword(name='获取窗口标题', tags=['窗口管理'])
    def get_window_title(self, window_title=None, app_alias=None, index=0):
        """获取窗口标题
        
        获取指定标题或索引的窗口标题
        
        参数:
            window_title: 窗口标题，可以是完整标题或正则表达式
            app_alias: 应用程序的别名
            index: 窗口索引，默认为0
        
        返回:
            窗口标题
        
        示例:
            | ${title} | 获取窗口标题 | 窗口标题=Untitled - Notepad |
        """
        logger.info(f"获取窗口标题: 窗口标题={window_title}, 应用别名={app_alias}, 索引={index}")
        return self.window_service.get_window_title(window_title, app_alias, index)
    
    @keyword(name='获取窗口位置', tags=['窗口管理'])
    def get_window_position(self, window_title=None, app_alias=None, index=0):
        """获取窗口位置
        
        获取指定标题或索引的窗口位置
        
        参数:
            window_title: 窗口标题，可以是完整标题或正则表达式
            app_alias: 应用程序的别名
            index: 窗口索引，默认为0
        
        返回:
            包含x和y坐标的字典
        
        示例:
            | ${pos} | 获取窗口位置 | 窗口标题=Untitled - Notepad |
        """
        logger.info(f"获取窗口位置: 窗口标题={window_title}, 应用别名={app_alias}, 索引={index}")
        return self.window_service.get_window_position(window_title, app_alias, index)
    
    @keyword(name='获取窗口大小', tags=['窗口管理'])
    def get_window_size(self, window_title=None, app_alias=None, index=0):
        """获取窗口大小
        
        获取指定标题或索引的窗口大小
        
        参数:
            window_title: 窗口标题，可以是完整标题或正则表达式
            app_alias: 应用程序的别名
            index: 窗口索引，默认为0
        
        返回:
            包含宽度和高度的字典
        
        示例:
            | ${size} | 获取窗口大小 | 窗口标题=Untitled - Notepad |
        """
        logger.info(f"获取窗口大小: 窗口标题={window_title}, 应用别名={app_alias}, 索引={index}")
        return self.window_service.get_window_size(window_title, app_alias, index)
    
    @keyword(name='窗口是否存在', tags=['窗口管理'])
    def is_window_exists(self, window_title, app_alias=None):
        """检查窗口是否存在
        
        检查指定标题的窗口是否存在
        
        参数:
            window_title: 窗口标题，可以是完整标题或正则表达式
            app_alias: 应用程序的别名
        
        返回:
            True如果窗口存在，否则返回False
        
        示例:
            | ${exists} | 窗口是否存在 | 窗口标题=Untitled - Notepad | 别名=notepad++ |
        """
        logger.info(f"检查窗口是否存在: 窗口标题={window_title}, 应用别名={app_alias}")
        return self.window_service.is_window_exists(window_title, app_alias)
