# 后端适配层初始化文件

from .backend_factory import backend_factory, Backend
from .pywinauto_backend import PywinautoBackend, PywinautoApplication, PywinautoWindow, PywinautoControl, PywinautoOperation

# 尝试导入UIAutomation后端，处理导入错误
try:
    from .uiautomation_backend import UIAutomationBackend
    __all__ = [
        "backend_factory",
        "Backend",
        "PywinautoBackend",
        "PywinautoApplication",
        "PywinautoWindow",
        "PywinautoControl",
        "PywinautoOperation",
        "UIAutomationBackend"
    ]
except ImportError:
    __all__ = [
        "backend_factory",
        "Backend",
        "PywinautoBackend",
        "PywinautoApplication",
        "PywinautoWindow",
        "PywinautoControl",
        "PywinautoOperation"
    ]
