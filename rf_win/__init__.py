#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
rf-win - Windows Desktop Automation Robot Framework Library

一个基于pywinauto和UIAutomation的Robot Framework库，用于Windows桌面应用自动化测试
"""

# Robot Framework 7.x版本中，装饰器的导入方式有所不同
# 为了兼容不同版本，我们直接实现一个简单的装饰器系统

# 定义一个全局字典来存储关键字
_registered_keywords = {}

# 模拟library装饰器
def library(scope='GLOBAL', version='1.0.0', doc_format='reST'):
    """Robot Framework库装饰器"""
    def decorator(cls):
        return cls
    return decorator

# 模拟keyword装饰器
def keyword(name=None, tags=()):
    """Robot Framework关键字装饰器"""
    def decorator(func):
        # 为方法添加robot_name属性，用于关键字注册
        func.robot_name = name or func.__name__
        func.tags = tags
        func._rf_keyword = True
        # 将关键字添加到全局字典中
        _registered_keywords[func.robot_name] = func
        return func
    return decorator

from robot.libraries.BuiltIn import BuiltIn

from .keywords.application import ApplicationKeywords
from .keywords.window import WindowKeywords
from .keywords.control import ControlKeywords
from .keywords.operation import OperationKeywords
from .keywords.data_io import DataIOKeywords

@library(scope='GLOBAL', version='1.0.0', doc_format='reST')
class RFWin:
    """RFWin库类
    
    提供Windows桌面应用自动化测试的关键字，包括：
    - 应用管理：启动、关闭、连接应用等
    - 窗口管理：获取、切换、操作窗口等
    - 控件管理：查找、点击、输入控件等
    - 操作管理：鼠标、键盘、等待、截图等
    - 数据IO：读写文本、JSON、CSV、Excel等
    
    示例：
        | *** Settings ***
        | Library           rf_win
        | 
        | *** Test Cases ***
        | 测试记事本
        |     启动应用    C:/Windows/notepad.exe    别名=notepad
        |     控件输入文本    Edit:    Hello World    窗口标题=无标题 - 记事本
        |     截图    文件名=notepad_test
        |     关闭应用    别名=notepad
    """
    
    def __init__(self):
        """初始化RFWin库实例
        
        创建各个关键字模块的实例，用于提供关键字功能
        """
        self.app_keywords = ApplicationKeywords()
        self.window_keywords = WindowKeywords()
        self.control_keywords = ControlKeywords()
        self.operation_keywords = OperationKeywords()
        self.data_io_keywords = DataIOKeywords()
        
        # 将各个服务实例注册到RFWin实例上，以便关键字方法访问
        # 注意：这里假设各个关键字模块实例都有对应的服务属性
        # 例如：app_keywords实例有app_service属性
        # 如果关键字模块的服务属性命名不同，需要根据实际情况调整
        self.app_service = getattr(self.app_keywords, 'app_service', None)
        self.window_service = getattr(self.window_keywords, 'window_service', None)
        self.control_service = getattr(self.control_keywords, 'control_service', None)
        self.operation_service = getattr(self.operation_keywords, 'operation_service', None)
        self.data_io = getattr(self.data_io_keywords, 'data_io', None)
        
        # 注册关键字到Robot Framework
        self._register_keywords()
    
    def _register_keywords(self):
        """注册关键字到Robot Framework
        
        将各个关键字模块的关键字注册到Robot Framework
        """
        # 注册应用关键字
        self._register_module_keywords(self.app_keywords)
        
        # 注册窗口关键字
        self._register_module_keywords(self.window_keywords)
        
        # 注册控件关键字
        self._register_module_keywords(self.control_keywords)
        
        # 注册操作关键字
        self._register_module_keywords(self.operation_keywords)
        
        # 注册数据IO关键字
        self._register_module_keywords(self.data_io_keywords)
    
    def _register_module_keywords(self, module_instance):
        """注册模块关键字
        
        将指定模块实例的关键字注册到Robot Framework
        
        参数:
            module_instance: 关键字模块实例
        """
        # 获取模块的所有方法
        import inspect
        methods = inspect.getmembers(module_instance, inspect.ismethod)
        
        # 注册带有@keyword装饰器的方法
        for name, method in methods:
            # 检查方法是否有robot_name属性，这是关键字的标志
            if hasattr(method, 'robot_name'):
                # 将方法绑定到当前实例
                bound_method = method.__get__(self)
                # 注册关键字
                setattr(self, name, bound_method)

# 版本信息
__version__ = '1.0.0'

# 作者信息
__author__ = 'Your Name'
__email__ = 'your.email@example.com'

# 导出RFWin类
__all__ = ["RFWin"]
