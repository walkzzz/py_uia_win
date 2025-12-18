# 工具模块初始化文件

from .locator_helper import LocatorHelper, locator_helper
from .wait_strategy import WaitStrategy, wait_strategy
from .cache_manager import CacheManager, application_cache, window_cache, control_cache, locator_cache
from .dpi_adapter import DPIAdapter, dpi_adapter
from .logger import Logger, logger

__all__ = [
    # 定位器助手
    "LocatorHelper",
    "locator_helper",
    # 智能等待策略
    "WaitStrategy",
    "wait_strategy",
    # 缓存管理器
    "CacheManager",
    "application_cache",
    "window_cache",
    "control_cache",
    "locator_cache",
    # 高DPI适配器
    "DPIAdapter",
    "dpi_adapter",
    # 日志工具
    "Logger",
    "logger"
]
