#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动化驱动测试

测试rf_win.drivers模块中的自动化驱动，确保它们能够正确地创建和管理驱动实例
"""

import unittest
from unittest.mock import Mock, patch
from rf_win.drivers import AutomationDriver, DriverFactory, PywinautoDriver


class TestAutomationDriver(unittest.TestCase):
    """测试AutomationDriver抽象类"""
    
    def test_automation_driver_is_abstract(self):
        """测试AutomationDriver是抽象类，不能直接实例化"""
        with self.assertRaises(TypeError):
            AutomationDriver()
    
    def test_automation_driver_methods(self):
        """测试AutomationDriver的方法签名"""
        # 创建一个具体子类来测试
        class ConcreteAutomationDriver(AutomationDriver):
            def start_application(self, app_path, **kwargs):
                pass
            
            def attach_to_application(self, **kwargs):
                pass
            
            def close_application(self, app_instance=None):
                pass
            
            def get_main_window(self, app_instance=None):
                pass
            
            def locate_window(self, **kwargs):
                pass
            
            def activate_window(self, window_instance):
                pass
            
            def close_window(self, window_instance):
                pass
            
            def find_element(self, window_instance, locator, **kwargs):
                pass
            
            def find_elements(self, window_instance, locator, **kwargs):
                return []
            
            def click_element(self, element_instance, **kwargs):
                pass
            
            def right_click_element(self, element_instance, **kwargs):
                pass
            
            def double_click_element(self, element_instance, **kwargs):
                pass
            
            def set_element_text(self, element_instance, text, **kwargs):
                pass
            
            def get_element_text(self, element_instance):
                return ""
            
            def clear_element_text(self, element_instance):
                pass
            
            def click_mouse(self, x, y, button='left', **kwargs):
                pass
            
            def right_click_mouse(self, x, y, **kwargs):
                pass
            
            def double_click_mouse(self, x, y, **kwargs):
                pass
            
            def move_mouse(self, x, y, **kwargs):
                pass
            
            def drag_drop_mouse(self, from_x, from_y, to_x, to_y, **kwargs):
                pass
            
            def type_text(self, text, **kwargs):
                pass
            
            def press_key(self, key, **kwargs):
                pass
            
            def release_key(self, key, **kwargs):
                pass
            
            def capture_screenshot(self, filename=None, window_instance=None, **kwargs):
                return ""
            
            def wait_for_condition(self, condition, **kwargs):
                return True
        
        driver = ConcreteAutomationDriver()
        self.assertTrue(hasattr(driver, 'start_application'))
        self.assertTrue(hasattr(driver, 'attach_to_application'))
        self.assertTrue(hasattr(driver, 'close_application'))
        self.assertTrue(hasattr(driver, 'get_main_window'))
        self.assertTrue(hasattr(driver, 'locate_window'))
        self.assertTrue(hasattr(driver, 'activate_window'))
        self.assertTrue(hasattr(driver, 'close_window'))
        self.assertTrue(hasattr(driver, 'find_element'))
        self.assertTrue(hasattr(driver, 'find_elements'))
        self.assertTrue(hasattr(driver, 'click_element'))
        self.assertTrue(hasattr(driver, 'right_click_element'))
        self.assertTrue(hasattr(driver, 'double_click_element'))
        self.assertTrue(hasattr(driver, 'set_element_text'))
        self.assertTrue(hasattr(driver, 'get_element_text'))
        self.assertTrue(hasattr(driver, 'clear_element_text'))
        self.assertTrue(hasattr(driver, 'click_mouse'))
        self.assertTrue(hasattr(driver, 'right_click_mouse'))
        self.assertTrue(hasattr(driver, 'double_click_mouse'))
        self.assertTrue(hasattr(driver, 'move_mouse'))
        self.assertTrue(hasattr(driver, 'drag_drop_mouse'))
        self.assertTrue(hasattr(driver, 'type_text'))
        self.assertTrue(hasattr(driver, 'press_key'))
        self.assertTrue(hasattr(driver, 'release_key'))
        self.assertTrue(hasattr(driver, 'capture_screenshot'))
        self.assertTrue(hasattr(driver, 'wait_for_condition'))
        
        # 测试具体方法
        self.assertEqual(driver.get_element_text(Mock()), "")
        self.assertEqual(driver.find_elements(Mock(), "locator"), [])
        self.assertTrue(driver.wait_for_condition(Mock()))


class TestPywinautoDriver(unittest.TestCase):
    """测试PywinautoDriver类"""
    
    def test_pywinauto_driver_initialization(self):
        """测试PywinautoDriver初始化"""
        driver = PywinautoDriver()
        self.assertIsInstance(driver, PywinautoDriver)
    
    def test_pywinauto_driver_inherits_automation_driver(self):
        """测试PywinautoDriver继承自AutomationDriver"""
        driver = PywinautoDriver()
        self.assertIsInstance(driver, AutomationDriver)
    
    def test_pywinauto_driver_methods(self):
        """测试PywinautoDriver实现了所有必要的方法"""
        driver = PywinautoDriver()
        self.assertTrue(hasattr(driver, 'start_application'))
        self.assertTrue(hasattr(driver, 'attach_to_application'))
        self.assertTrue(hasattr(driver, 'close_application'))
        self.assertTrue(hasattr(driver, 'get_main_window'))
        self.assertTrue(hasattr(driver, 'locate_window'))
        self.assertTrue(hasattr(driver, 'activate_window'))
        self.assertTrue(hasattr(driver, 'close_window'))
        self.assertTrue(hasattr(driver, 'find_element'))
        self.assertTrue(hasattr(driver, 'find_elements'))
        self.assertTrue(hasattr(driver, 'click_element'))
        self.assertTrue(hasattr(driver, 'right_click_element'))
        self.assertTrue(hasattr(driver, 'double_click_element'))
        self.assertTrue(hasattr(driver, 'set_element_text'))
        self.assertTrue(hasattr(driver, 'get_element_text'))
        self.assertTrue(hasattr(driver, 'clear_element_text'))
        self.assertTrue(hasattr(driver, 'click_mouse'))
        self.assertTrue(hasattr(driver, 'right_click_mouse'))
        self.assertTrue(hasattr(driver, 'double_click_mouse'))
        self.assertTrue(hasattr(driver, 'move_mouse'))
        self.assertTrue(hasattr(driver, 'drag_drop_mouse'))
        self.assertTrue(hasattr(driver, 'type_text'))
        self.assertTrue(hasattr(driver, 'press_key'))
        self.assertTrue(hasattr(driver, 'release_key'))
        self.assertTrue(hasattr(driver, 'capture_screenshot'))
        self.assertTrue(hasattr(driver, 'wait_for_condition'))


class TestDriverFactory(unittest.TestCase):
    """测试DriverFactory类"""
    
    def test_driver_factory_initialization(self):
        """测试驱动工厂初始化"""
        factory = DriverFactory()
        self.assertIsInstance(factory, DriverFactory)
    
    @patch('rf_win.drivers.automation_driver.PywinautoDriver')
    def test_create_driver_pywinauto(self, mock_pywinauto_driver):
        """测试创建pywinauto驱动"""
        mock_instance = Mock()
        mock_pywinauto_driver.return_value = mock_instance
        
        factory = DriverFactory()
        driver = factory.create_driver("pywinauto")
        self.assertEqual(driver, mock_instance)
        mock_pywinauto_driver.assert_called_once()
    
    def test_create_driver_invalid(self):
        """测试创建无效驱动时抛出异常"""
        factory = DriverFactory()
        with self.assertRaises(ValueError):
            factory.create_driver("invalid_driver")
    
    @patch('rf_win.drivers.automation_driver.PywinautoDriver')
    def test_driver_singleton(self, mock_pywinauto_driver):
        """测试驱动工厂返回单例实例"""
        mock_instance = Mock()
        mock_pywinauto_driver.return_value = mock_instance
        
        factory = DriverFactory()
        driver1 = factory.create_driver("pywinauto")
        driver2 = factory.create_driver("pywinauto")
        self.assertIs(driver1, driver2)
        mock_pywinauto_driver.assert_called_once()
    
    def test_get_supported_drivers(self):
        """测试获取支持的驱动列表"""
        factory = DriverFactory()
        supported_drivers = factory.get_supported_drivers()
        self.assertIsInstance(supported_drivers, list)
        self.assertIn("pywinauto", supported_drivers)
        self.assertIn("uiautomation", supported_drivers)


if __name__ == '__main__':
    unittest.main(verbosity=2)
