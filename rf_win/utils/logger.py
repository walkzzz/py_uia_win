# 日志工具模块
# 提供详细的日志记录功能，方便调试和监控自动化执行过程

import logging
import os
from datetime import datetime
from typing import Optional, Dict, Any

class Logger:
    """日志工具类"""
    
    def __init__(self, name: str = "rf-win", level: str = "info", log_file: Optional[str] = None):
        """初始化日志工具
        
        Args:
            name: 日志名称
            level: 日志级别（debug, info, warn, error）
            log_file: 日志文件路径，如果为None则只输出到控制台
        """
        self.name = name
        self.level = level.upper()
        self.log_file = log_file
        
        # 创建日志记录器
        self.logger = logging.getLogger(name)
        self.logger.setLevel(self.level)
        self.logger.handlers.clear()
        
        # 创建日志格式
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
        )
        
        # 控制台处理器
        console_handler = logging.StreamHandler()
        console_handler.setLevel(self.level)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
        
        # 文件处理器
        if self.log_file:
            # 创建日志目录
            log_dir = os.path.dirname(self.log_file)
            if log_dir and not os.path.exists(log_dir):
                os.makedirs(log_dir)
            
            file_handler = logging.FileHandler(self.log_file, encoding='utf-8')
            file_handler.setLevel(self.level)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)
    
    def debug(self, message: str, **context: Any) -> None:
        """记录调试日志
        
        Args:
            message: 日志消息
            **context: 上下文信息
        """
        self._log(logging.DEBUG, message, **context)
    
    def info(self, message: str, **context: Any) -> None:
        """记录信息日志
        
        Args:
            message: 日志消息
            **context: 上下文信息
        """
        self._log(logging.INFO, message, **context)
    
    def warn(self, message: str, **context: Any) -> None:
        """记录警告日志
        
        Args:
            message: 日志消息
            **context: 上下文信息
        """
        self._log(logging.WARNING, message, **context)
    
    def error(self, message: str, **context: Any) -> None:
        """记录错误日志
        
        Args:
            message: 日志消息
            **context: 上下文信息
        """
        self._log(logging.ERROR, message, **context)
    
    def exception(self, message: str, **context: Any) -> None:
        """记录异常日志
        
        Args:
            message: 日志消息
            **context: 上下文信息
        """
        self.logger.exception(self._format_message(message, **context))
    
    def _log(self, level: int, message: str, **context: Any) -> None:
        """记录日志
        
        Args:
            level: 日志级别
            message: 日志消息
            **context: 上下文信息
        """
        formatted_message = self._format_message(message, **context)
        self.logger.log(level, formatted_message)
    
    def _format_message(self, message: str, **context: Any) -> str:
        """格式化日志消息
        
        Args:
            message: 日志消息
            **context: 上下文信息
            
        Returns:
            格式化后的日志消息
        """
        if not context:
            return message
        
        # 格式化上下文信息
        context_str = " | ".join([f"{k}={v}" for k, v in context.items()])
        return f"{message} | {context_str}"
    
    def set_level(self, level: str) -> None:
        """设置日志级别
        
        Args:
            level: 日志级别（debug, info, warn, error）
        """
        self.level = level.upper()
        self.logger.setLevel(self.level)
        
        # 更新所有处理器的日志级别
        for handler in self.logger.handlers:
            handler.setLevel(self.level)
    
    def add_file_handler(self, log_file: str) -> None:
        """添加文件处理器
        
        Args:
            log_file: 日志文件路径
        """
        # 创建日志目录
        log_dir = os.path.dirname(log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        # 创建文件处理器
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
        )
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(self.level)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
    
    def remove_file_handler(self) -> None:
        """移除所有文件处理器"""
        handlers = self.logger.handlers[:]
        for handler in handlers:
            if isinstance(handler, logging.FileHandler):
                self.logger.removeHandler(handler)
    
    def get_logger(self) -> logging.Logger:
        """获取原始日志记录器
        
        Returns:
            原始日志记录器
        """
        return self.logger

# 创建默认日志实例
# 从环境变量获取日志配置
log_level = os.environ.get("RF_WIN_LOG_LEVEL", "info")
log_file = os.environ.get("RF_WIN_LOG_FILE", None)

if log_file is None:
    # 默认日志文件路径
    log_file = os.path.join(os.getcwd(), "logs", "rf_win.log")

# 创建日志目录
log_dir = os.path.dirname(log_file)
if log_dir and not os.path.exists(log_dir):
    os.makedirs(log_dir)

# 创建日志实例
logger = Logger(name="rf-win", level=log_level, log_file=log_file)
