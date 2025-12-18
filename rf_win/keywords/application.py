#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
应用管理关键字模块
提供应用程序的启动、关闭、连接等关键字
"""

from .. import keyword, library
from ..services.application_service import ApplicationService
from ..utils.logger import logger

@library(scope='GLOBAL', version='1.0.0')
class ApplicationKeywords:
    """应用管理关键字类
    
    提供应用程序的启动、关闭、连接等关键字，用于Robot Framework测试用例
    """
    
    def __init__(self):
        """初始化应用服务实例"""
        self.app_service = ApplicationService()
    
    @keyword(name='启动应用', tags=['应用管理'])
    def start_application(self, app_path, **kwargs):
        """启动应用程序
        
        启动指定路径的应用程序，并返回应用实例
        
        参数:
            app_path: 应用程序的完整路径
            别名: 应用程序的别名，用于后续操作引用
            后端: 后端类型，可选值为'pywinauto'或'uiautomation'
            **kwargs: 启动应用程序时的额外参数
        
        返回:
            应用程序实例
        
        示例:
            | 启动应用 | C:/Program Files/Notepad++/notepad++.exe | 别名=notepad++ |
        """
        # 处理中文参数名映射
        alias = kwargs.pop('别名', kwargs.pop('alias', None))
        backend = kwargs.pop('后端', kwargs.pop('backend', None))
        
        logger.info(f"启动应用: {app_path}, 别名: {alias}, 后端: {backend}")
        return self.app_service.start_application(app_path, alias, backend, **kwargs)
    
    @keyword(name='连接应用', tags=['应用管理'])
    def connect_application(self, **kwargs):
        """连接到已运行的应用程序
        
        通过进程ID或窗口标题连接到已运行的应用程序
        
        参数:
            进程ID: 应用程序的进程ID
            标题: 应用程序的窗口标题
            别名: 应用程序的别名，用于后续操作引用
            后端: 后端类型，可选值为'pywinauto'或'uiautomation'
            **kwargs: 连接应用程序时的额外参数
        
        返回:
            应用程序实例
        
        示例:
            | 连接应用 | 进程ID=1234 | 别名=notepad++ |
            | 连接应用 | 标题=Notepad++ | 别名=notepad++ |
        """
        # 处理中文参数名映射
        process_id = kwargs.pop('进程ID', kwargs.pop('process_id', None))
        title = kwargs.pop('标题', kwargs.pop('title', None))
        alias = kwargs.pop('别名', kwargs.pop('alias', None))
        backend = kwargs.pop('后端', kwargs.pop('backend', None))
        
        logger.info(f"连接应用: 进程ID={process_id}, 标题={title}, 别名={alias}, 后端={backend}")
        return self.app_service.connect_application(process_id, title, alias, backend, **kwargs)
    
    @keyword(name='关闭应用', tags=['应用管理'])
    def close_application(self, **kwargs):
        """关闭应用程序
        
        关闭指定别名的应用程序
        
        参数:
            别名: 应用程序的别名，如果不指定则关闭当前活动应用
        
        示例:
            | 关闭应用 | 别名=notepad++ |
        """
        # 处理中文参数名映射
        app_alias = kwargs.pop('别名', kwargs.pop('app_alias', None))
        
        logger.info(f"关闭应用: {app_alias}")
        return self.app_service.close_application(app_alias)
    
    @keyword(name='关闭所有应用', tags=['应用管理'])
    def close_all_applications(self):
        """关闭所有已连接的应用程序
        
        关闭所有通过关键字启动或连接的应用程序
        
        示例:
            | 关闭所有应用 |
        """
        logger.info("关闭所有应用")
        return self.app_service.close_all_applications()
    
    @keyword(name='获取当前应用', tags=['应用管理'])
    def get_current_application(self):
        """获取当前活动的应用程序
        
        返回当前活动的应用程序实例
        
        返回:
            当前活动的应用程序实例
        
        示例:
            | ${app} | 获取当前应用 |
        """
        logger.info("获取当前应用")
        return self.app_service.get_current_application()
    
    @keyword(name='切换应用', tags=['应用管理'])
    def switch_application(self, app_alias):
        """切换到指定别名的应用程序
        
        切换当前活动的应用程序为指定别名的应用
        
        参数:
            app_alias: 应用程序的别名
        
        示例:
            | 切换应用 | 别名=notepad++ |
        """
        logger.info(f"切换应用: {app_alias}")
        return self.app_service.switch_application(app_alias)
    
    @keyword(name='应用是否运行', tags=['应用管理'])
    def is_application_running(self, app_alias):
        """检查应用程序是否正在运行
        
        检查指定别名的应用程序是否正在运行
        
        参数:
            app_alias: 应用程序的别名
        
        返回:
            True如果应用程序正在运行，否则返回False
        
        示例:
            | ${is_running} | 应用是否运行 | 别名=notepad++ |
        """
        logger.info(f"检查应用是否运行: {app_alias}")
        return self.app_service.is_application_running(app_alias)
