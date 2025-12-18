#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
核心抽象类测试

测试rf_win.core模块中的抽象类，确保它们的接口设计合理，能够正确地被子类实现
"""

import unittest
from unittest.mock import Mock
from rf_win.core.base_application import BaseApplication
from rf_win.core.base_window import BaseWindow
from rf_win.core.base_control import BaseControl
from rf_win.core.base_operation import BaseOperation


class TestBaseApplication(unittest.TestCase):
    """测试BaseApplication抽象类"""
    
    def test_base_application_is_abstract(self):
        """测试BaseApplication是抽象类，不能直接实例化"""
        with self.assertRaises(TypeError):
            BaseApplication()
    
    def test_base_application_methods(self):
        """测试BaseApplication的方法签名"""
        # 创建一个具体子类来测试
        class ConcreteApplication(BaseApplication):
            def start(self, **kwargs):
                pass
            
            def connect(self, **kwargs):
                pass
            
            def close(self, **kwargs):
                pass
            
            def get_main_window(self):
                pass
            
            def get_windows(self):
                return []
            
            def switch_to_window(self, window):
                pass
            
            def get_app_info(self):
                return {}
        
        app = ConcreteApplication()
        self.assertTrue(hasattr(app, 'start'))
        self.assertTrue(hasattr(app, 'connect'))
        self.assertTrue(hasattr(app, 'close'))
        self.assertTrue(hasattr(app, 'get_main_window'))
        self.assertTrue(hasattr(app, 'get_windows'))
        self.assertTrue(hasattr(app, 'switch_to_window'))
        self.assertTrue(hasattr(app, 'get_app_info'))
        
        # 测试get_windows方法返回空列表
        self.assertEqual(app.get_windows(), [])


class TestBaseWindow(unittest.TestCase):
    """测试BaseWindow抽象类"""
    
    def test_base_window_is_abstract(self):
        """测试BaseWindow是抽象类，不能直接实例化"""
        with self.assertRaises(TypeError):
            BaseWindow()
    
    def test_base_window_methods(self):
        """测试BaseWindow的方法签名"""
        # 创建一个具体子类来测试
        class ConcreteWindow(BaseWindow):
            def get_title(self):
                return "Test Window"
            
            def set_title(self, title):
                pass
            
            def activate(self):
                pass
            
            def close(self):
                pass
            
            def maximize(self):
                pass
            
            def minimize(self):
                pass
            
            def restore(self):
                pass
            
            def get_position(self):
                return (0, 0)
            
            def set_position(self, x, y):
                pass
            
            def get_size(self):
                return (100, 100)
            
            def set_size(self, width, height):
                pass
            
            def get_client_rect(self):
                return (0, 0, 100, 100)
            
            def find_control(self, locator, **kwargs):
                return None
            
            def find_controls(self, locator, **kwargs):
                return []
            
            def get_controls(self):
                return []
            
            def is_visible(self):
                return True
            
            def is_enabled(self):
                return True
        
        window = ConcreteWindow()
        self.assertTrue(hasattr(window, 'get_title'))
        self.assertTrue(hasattr(window, 'set_title'))
        self.assertTrue(hasattr(window, 'activate'))
        self.assertTrue(hasattr(window, 'close'))
        self.assertTrue(hasattr(window, 'maximize'))
        self.assertTrue(hasattr(window, 'minimize'))
        self.assertTrue(hasattr(window, 'restore'))
        self.assertTrue(hasattr(window, 'get_position'))
        self.assertTrue(hasattr(window, 'set_position'))
        self.assertTrue(hasattr(window, 'get_size'))
        self.assertTrue(hasattr(window, 'set_size'))
        self.assertTrue(hasattr(window, 'get_client_rect'))
        self.assertTrue(hasattr(window, 'find_control'))
        self.assertTrue(hasattr(window, 'find_controls'))
        self.assertTrue(hasattr(window, 'get_controls'))
        self.assertTrue(hasattr(window, 'is_visible'))
        self.assertTrue(hasattr(window, 'is_enabled'))
        
        # 测试具体方法
        self.assertEqual(window.get_title(), "Test Window")
        self.assertEqual(window.get_position(), (0, 0))
        self.assertEqual(window.get_size(), (100, 100))
        self.assertEqual(window.get_client_rect(), (0, 0, 100, 100))
        self.assertTrue(window.is_visible())
        self.assertTrue(window.is_enabled())
        self.assertEqual(window.find_controls(Mock()), [])


class TestBaseControl(unittest.TestCase):
    """测试BaseControl抽象类"""
    
    def test_base_control_is_abstract(self):
        """测试BaseControl是抽象类，不能直接实例化"""
        with self.assertRaises(TypeError):
            BaseControl()
    
    def test_base_control_methods(self):
        """测试BaseControl的方法签名"""
        # 创建一个具体子类来测试
        class ConcreteControl(BaseControl):
            def click(self, **kwargs):
                pass
            
            def right_click(self, **kwargs):
                pass
            
            def double_click(self, **kwargs):
                pass
            
            def get_text(self):
                return ""
            
            def set_text(self, text, **kwargs):
                pass
            
            def clear_text(self):
                pass
            
            def get_name(self):
                return ""
            
            def get_class_name(self):
                return ""
            
            def get_control_type(self):
                return ""
            
            def get_position(self):
                return (0, 0)
            
            def get_size(self):
                return (0, 0)
            
            def is_visible(self):
                return True
            
            def is_enabled(self):
                return True
            
            def is_exists(self):
                return True
            
            def get_property(self, property_name):
                return None
            
            def set_property(self, property_name, value):
                pass
            
            def wait_for(self, condition, **kwargs):
                return True
        
        control = ConcreteControl()
        self.assertTrue(hasattr(control, 'click'))
        self.assertTrue(hasattr(control, 'right_click'))
        self.assertTrue(hasattr(control, 'double_click'))
        self.assertTrue(hasattr(control, 'get_text'))
        self.assertTrue(hasattr(control, 'set_text'))
        self.assertTrue(hasattr(control, 'clear_text'))
        self.assertTrue(hasattr(control, 'get_name'))
        self.assertTrue(hasattr(control, 'get_class_name'))
        self.assertTrue(hasattr(control, 'get_control_type'))
        self.assertTrue(hasattr(control, 'get_position'))
        self.assertTrue(hasattr(control, 'get_size'))
        self.assertTrue(hasattr(control, 'is_visible'))
        self.assertTrue(hasattr(control, 'is_enabled'))
        self.assertTrue(hasattr(control, 'is_exists'))
        self.assertTrue(hasattr(control, 'get_property'))
        self.assertTrue(hasattr(control, 'set_property'))
        self.assertTrue(hasattr(control, 'wait_for'))
        
        # 测试具体方法
        self.assertEqual(control.get_text(), "")
        self.assertEqual(control.get_name(), "")
        self.assertEqual(control.get_class_name(), "")
        self.assertEqual(control.get_control_type(), "")
        self.assertEqual(control.get_position(), (0, 0))
        self.assertEqual(control.get_size(), (0, 0))
        self.assertTrue(control.is_visible())
        self.assertTrue(control.is_enabled())
        self.assertTrue(control.is_exists())
        self.assertIsNone(control.get_property("test"))
        self.assertTrue(control.wait_for("visible"))


class TestBaseOperation(unittest.TestCase):
    """测试BaseOperation抽象类"""
    
    def test_base_operation_is_abstract(self):
        """测试BaseOperation是抽象类，不能直接实例化"""
        with self.assertRaises(TypeError):
            BaseOperation()
    
    def test_base_operation_methods(self):
        """测试BaseOperation的方法签名"""
        # 创建一个具体子类来测试
        class ConcreteOperation(BaseOperation):
            def click(self, x, y, button='left', **kwargs):
                pass
            
            def right_click(self, x, y, **kwargs):
                pass
            
            def double_click(self, x, y, **kwargs):
                pass
            
            def move_mouse(self, x, y, **kwargs):
                pass
            
            def drag_drop(self, from_x, from_y, to_x, to_y, **kwargs):
                pass
            
            def scroll(self, x, y, delta, **kwargs):
                pass
            
            def press_key(self, key, **kwargs):
                pass
            
            def release_key(self, key, **kwargs):
                pass
            
            def type_keys(self, keys, **kwargs):
                pass
            
            def get_mouse_position(self):
                return (0, 0)
            
            def capture_screenshot(self, filename=None, window=None, **kwargs):
                return ""
        
        operation = ConcreteOperation()
        self.assertTrue(hasattr(operation, 'click'))
        self.assertTrue(hasattr(operation, 'right_click'))
        self.assertTrue(hasattr(operation, 'double_click'))
        self.assertTrue(hasattr(operation, 'move_mouse'))
        self.assertTrue(hasattr(operation, 'drag_drop'))
        self.assertTrue(hasattr(operation, 'scroll'))
        self.assertTrue(hasattr(operation, 'press_key'))
        self.assertTrue(hasattr(operation, 'release_key'))
        self.assertTrue(hasattr(operation, 'type_keys'))
        self.assertTrue(hasattr(operation, 'get_mouse_position'))
        self.assertTrue(hasattr(operation, 'capture_screenshot'))
        
        # 测试具体方法
        self.assertEqual(operation.get_mouse_position(), (0, 0))
        self.assertEqual(operation.capture_screenshot(), "")


if __name__ == '__main__':
    unittest.main(verbosity=2)
