# 简化的测试脚本，不依赖Robot Framework
# 仅验证库的基本结构和关键字注册

import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 模拟Robot Framework的logger和BuiltIn，避免导入错误
class MockLogger:
    def info(self, msg):
        print(f"INFO: {msg}")
    def warn(self, msg):
        print(f"WARN: {msg}")
    def error(self, msg):
        print(f"ERROR: {msg}")
    def set_level(self, level):
        pass

class MockBuiltIn:
    def get_variable_value(self, var):
        return None

class MockBuiltInClass:
    def __call__(self, *args, **kwargs):
        return MockBuiltIn()

# 模拟驱动和驱动工厂
class MockDriver:
    def start_application(self, path, args=None, backend="pywinauto"):
        return "mock_app"
    def attach_to_application(self, identifier, backend="pywinauto"):
        return "mock_app"
    def close_application(self, app, timeout=10.0):
        return True
    def kill_application(self, app):
        return True
    def check_application_running(self, app):
        return True
    def get_application_process_id(self, app):
        return 123
    def wait_for_application_main_window(self, app, timeout=10.0):
        return "mock_window"

class MockDriverFactory:
    def get_driver(self, name=None):
        return MockDriver()
    def get_available_drivers(self):
        return ["pywinauto", "uiautomation"]
    def set_default_driver(self, name):
        pass

# 猴子补丁，替换Robot Framework的导入
sys.modules['robot'] = type('robot', (), {'__path__': []})()
sys.modules['robot.api'] = type('robot.api', (), {'logger': MockLogger()})()
sys.modules['robot.libraries'] = type('robot.libraries', (), {'__path__': []})()
sys.modules['robot.libraries.BuiltIn'] = type('robot.libraries.BuiltIn', (), {'BuiltIn': MockBuiltInClass()})()

# 先创建模拟驱动和驱动工厂
class MockAutomationDriver:
    @property
    def name(self):
        return "pywinauto"
    
    def start_application(self, path, args=None, backend="uia"):
        return "mock_app"
    
    def connect_to_application(self, identifier, backend="uia"):
        return "mock_app"
    
    def close_application(self, app, timeout=10.0):
        return True
    
    def find_window(self, app, window_identifier):
        return "mock_window"
    
    def find_element(self, parent, locator, timeout=10.0):
        return "mock_element"
    
    def find_elements(self, parent, locator, timeout=10.0):
        return ["mock_element"]
    
    def click_element(self, element, button="left", clicks=1, interval=0.0, x_offset=0, y_offset=0):
        return True
    
    def type_text(self, element, text, clear_first=True, delay=0.0):
        return True
    
    def clear_element_text(self, element):
        return True
    
    def get_element_text(self, element):
        return "mock_text"
    
    def get_element_attribute(self, element, attribute):
        return "mock_attribute"
    
    def is_element_valid(self, element):
        return True
    
    def is_element_enabled(self, element):
        return True
    
    def is_element_visible(self, element):
        return True
    
    def hover_element(self, element):
        return True
    
    def drag_element_to(self, source_element, target_element):
        return True
    
    def select_element(self, element, value=None, text=None, index=-1):
        return True
    
    def deselect_element(self, element, value=None, text=None, index=-1):
        return True
    
    def is_element_selected(self, element):
        return True

class MockDriverFactory:
    def __init__(self):
        self._drivers = {"pywinauto": MockAutomationDriver()}
        self._default_driver = "pywinauto"
    
    def get_driver(self, name=None):
        return self._drivers["pywinauto"]
    
    def get_available_drivers(self):
        return ["pywinauto", "uiautomation"]
    
    def set_default_driver(self, name):
        self._default_driver = name

# 猴子补丁，在导入库之前替换driver_factory
# 首先创建一个模拟的drivers.automation_driver模块
sys.modules['rf_win.drivers'] = type('rf_win.drivers', (), {'__path__': []})()
sys.modules['rf_win.drivers.automation_driver'] = type('rf_win.drivers.automation_driver', (), {
    'driver_factory': MockDriverFactory(),
    'AutomationDriver': type('AutomationDriver', (), {}),
    'PywinautoDriver': type('PywinautoDriver', (), {}),
    'UIAutomationDriver': type('UIAutomationDriver', (), {})
})()

try:
    # 现在尝试导入我们的库
    from rf_win import RFWinLibrary
    
    print("✓ 成功导入RFWinLibrary")
    
    # 创建库实例
    library = RFWinLibrary()
    print("✓ 成功创建RFWinLibrary实例")
    
    # 检查关键字是否正确注册
    keywords = [
        'start_application',
        'attach_to_application',
        'close_application',
        'get_main_window',
        'activate_window',
        'find_element',
        'click_element',
        'type_text',
        'get_element_text'
    ]
    
    missing_keywords = []
    for keyword in keywords:
        if not hasattr(library, keyword):
            missing_keywords.append(keyword)
    
    if missing_keywords:
        print(f"✗ 缺少关键字: {missing_keywords}")
    else:
        print("✓ 所有关键字已正确注册")
    
    print("\n测试完成！")
    sys.exit(0)
    
except Exception as e:
    print(f"✗ 测试失败: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
