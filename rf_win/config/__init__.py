# 配置模块初始化文件

from .global_config import global_config, CONFIG_KEY_MAP
from .local_config import local_config

__all__ = [
    "global_config",
    "local_config",
    "CONFIG_KEY_MAP"
]
