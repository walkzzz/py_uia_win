# 全局配置模块
# 定义库的默认配置，可通过环境变量或局部配置覆盖

from typing import Dict, Any

class GlobalConfig:
    """全局配置类"""
    
    def __init__(self):
        # 超时配置（秒）
        self.timeout: int = 10
        # 重试次数
        self.retry: int = 1
        # 重试间隔（秒）
        self.retry_interval: float = 1.0
        # 默认后端（auto: 自动适配, pywinauto: 使用pywinauto, uiautomation: 使用UIAutomation）
        self.default_backend: str = "auto"
        # 默认pywinauto后端类型（win32, uia）
        self.pywinauto_backend: str = "uia"
        # 截图保存路径
        self.screenshot_path: str = "./screenshots/"
        # 截图格式（png, jpg）
        self.screenshot_format: str = "png"
        # 截图压缩质量（0-100，仅jpg）
        self.screenshot_quality: int = 90
        # 日志级别（debug, info, warn, error）
        self.log_level: str = "info"
        # 日志文件路径
        self.log_file: str = "./logs/rf_win.log"
        # 自动捕获失败截图
        self.auto_screenshot_on_fail: bool = True
        # 高DPI适配开关
        self.high_dpi_adapter: bool = True
        # 控件缓存过期时间（秒）
        self.cache_expire_time: int = 10
        # 最大缓存数量
        self.max_cache_size: int = 100
        # 语言（zh-CN, en-US）
        self.language: str = "zh-CN"
    
    def update(self, **kwargs: Any) -> None:
        """更新配置"""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

# 创建全局配置实例
global_config = GlobalConfig()

# 配置键映射，用于从环境变量或RF变量加载配置
CONFIG_KEY_MAP: Dict[str, str] = {
    "RF_WIN_TIMEOUT": "timeout",
    "RF_WIN_RETRY": "retry",
    "RF_WIN_RETRY_INTERVAL": "retry_interval",
    "RF_WIN_DEFAULT_BACKEND": "default_backend",
    "RF_WIN_PYWINAUTO_BACKEND": "pywinauto_backend",
    "RF_WIN_SCREENSHOT_PATH": "screenshot_path",
    "RF_WIN_SCREENSHOT_FORMAT": "screenshot_format",
    "RF_WIN_SCREENSHOT_QUALITY": "screenshot_quality",
    "RF_WIN_LOG_LEVEL": "log_level",
    "RF_WIN_LOG_FILE": "log_file",
    "RF_WIN_AUTO_SCREENSHOT": "auto_screenshot_on_fail",
    "RF_WIN_HIGH_DPI": "high_dpi_adapter",
    "RF_WIN_CACHE_EXPIRE": "cache_expire_time",
    "RF_WIN_MAX_CACHE": "max_cache_size",
    "RF_WIN_LANGUAGE": "language"
}
