#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
服务层测试

测试rf_win.services模块中的服务类，确保它们能够正确地处理业务逻辑
"""

import unittest
from unittest.mock import Mock, patch
from rf_win.services.application_service import ApplicationService
from rf_win.services.window_service import WindowService
from rf_win.services.control_service import ControlService
from rf_win.services.operation_service import OperationService


class TestApplicationService(unittest.TestCase):
    """测试ApplicationService类"""
    
    def setUp(self):
        """初始化测试环境"""
        self.app_service = ApplicationService()
    
    def test_application_service_initialization(self):
        """测试ApplicationService初始化"""
        self.assertIsInstance(self.app_service, ApplicationService)
    
    def test_application_service_has_attributes(self):
        """测试ApplicationService具有所需的属性"""
        self.assertTrue(hasattr(self.app_service, '_app_instances'))
        self.assertIsInstance(self.app_service._app_instances, dict)
    
    @patch('rf_win.services.application_service.DriverFactory.create_driver')
    def test_start_application(self, mock_create_driver):
        """测试启动应用程序"""
        # 模拟驱动和应用实例
        mock_driver = Mock()
        mock_app_instance = Mock()
        mock_create_driver.return_value = mock_driver
        mock_driver.start_application.return_value = mock_app_instance
        
        # 调用start_application方法
        app_path = "C:/Windows/notepad.exe"
        app_alias = "notepad"
        app = self.app_service.start_application(app_path, app_alias)
        
        # 验证结果
        self.assertEqual(app, mock_app_instance)
        self.assertIn(app_alias, self.app_service._app_instances)
        mock_driver.start_application.assert_called_once_with(app_path)
    
    def test_get_application(self):
        """测试获取应用程序实例"""
        # 先添加一个应用实例
        mock_app = Mock()
        app_alias = "test_app"
        self.app_service._app_instances[app_alias] = mock_app
        
        # 调用get_application方法
        app = self.app_service.get_application(app_alias)
        
        # 验证结果
        self.assertEqual(app, mock_app)
    
    def test_get_application_not_found(self):
        """测试获取不存在的应用程序实例时返回None"""
        app = self.app_service.get_application("non_existent_app")
        self.assertIsNone(app)
    
    def test_close_application(self):
        """测试关闭应用程序"""
        # 先添加一个应用实例
        mock_app = Mock()
        app_alias = "test_app"
        self.app_service._app_instances[app_alias] = mock_app
        
        # 调用close_application方法
        self.app_service.close_application(app_alias)
        
        # 验证结果
        self.assertNotIn(app_alias, self.app_service._app_instances)
    
    def test_close_all_applications(self):
        """测试关闭所有应用程序"""
        # 先添加几个应用实例
        mock_app1 = Mock()
        mock_app2 = Mock()
        self.app_service._app_instances["app1"] = mock_app1
        self.app_service._app_instances["app2"] = mock_app2
        
        # 调用close_all_applications方法
        self.app_service.close_all_applications()
        
        # 验证结果
        self.assertEqual(len(self.app_service._app_instances), 0)


class TestWindowService(unittest.TestCase):
    """测试WindowService类"""
    
    def setUp(self):
        """初始化测试环境"""
        self.window_service = WindowService()
    
    def test_window_service_initialization(self):
        """测试WindowService初始化"""
        self.assertIsInstance(self.window_service, WindowService)
    
    @patch('rf_win.services.window_service.DriverFactory.create_driver')
    def test_get_main_window(self, mock_create_driver):
        """测试获取主窗口"""
        # 模拟驱动和窗口实例
        mock_driver = Mock()
        mock_window_instance = Mock()
        mock_create_driver.return_value = mock_driver
        mock_driver.get_main_window.return_value = mock_window_instance
        
        # 调用get_main_window方法
        mock_app = Mock()
        window = self.window_service.get_main_window(mock_app)
        
        # 验证结果
        self.assertEqual(window, mock_window_instance)
        mock_driver.get_main_window.assert_called_once_with(mock_app)
    
    @patch('rf_win.services.window_service.DriverFactory.create_driver')
    def test_locate_window(self, mock_create_driver):
        """测试定位窗口"""
        # 模拟驱动和窗口实例
        mock_driver = Mock()
        mock_window_instance = Mock()
        mock_create_driver.return_value = mock_driver
        mock_driver.locate_window.return_value = mock_window_instance
        
        # 调用locate_window方法
        window = self.window_service.locate_window(title="Test Window")
        
        # 验证结果
        self.assertEqual(window, mock_window_instance)
        mock_driver.locate_window.assert_called_once_with(title="Test Window")
    
    @patch('rf_win.services.window_service.DriverFactory.create_driver')
    def test_activate_window(self, mock_create_driver):
        """测试激活窗口"""
        # 模拟驱动
        mock_driver = Mock()
        mock_create_driver.return_value = mock_driver
        
        # 调用activate_window方法
        mock_window = Mock()
        self.window_service.activate_window(mock_window)
        
        # 验证结果
        mock_driver.activate_window.assert_called_once_with(mock_window)
    
    @patch('rf_win.services.window_service.DriverFactory.create_driver')
    def test_close_window(self, mock_create_driver):
        """测试关闭窗口"""
        # 模拟驱动
        mock_driver = Mock()
        mock_create_driver.return_value = mock_driver
        
        # 调用close_window方法
        mock_window = Mock()
        self.window_service.close_window(mock_window)
        
        # 验证结果
        mock_driver.close_window.assert_called_once_with(mock_window)


class TestControlService(unittest.TestCase):
    """测试ControlService类"""
    
    def setUp(self):
        """初始化测试环境"""
        self.control_service = ControlService()
    
    def test_control_service_initialization(self):
        """测试ControlService初始化"""
        self.assertIsInstance(self.control_service, ControlService)
    
    @patch('rf_win.services.control_service.DriverFactory.create_driver')
    def test_find_control(self, mock_create_driver):
        """测试查找控件"""
        # 模拟驱动和控件实例
        mock_driver = Mock()
        mock_control_instance = Mock()
        mock_create_driver.return_value = mock_driver
        mock_driver.find_element.return_value = mock_control_instance
        
        # 调用find_control方法
        mock_window = Mock()
        locator = "Edit:"
        control = self.control_service.find_control(mock_window, locator)
        
        # 验证结果
        self.assertEqual(control, mock_control_instance)
        mock_driver.find_element.assert_called_once_with(mock_window, locator)
    
    @patch('rf_win.services.control_service.DriverFactory.create_driver')
    def test_find_controls(self, mock_create_driver):
        """测试查找多个控件"""
        # 模拟驱动和控件实例
        mock_driver = Mock()
        mock_control_instance1 = Mock()
        mock_control_instance2 = Mock()
        mock_create_driver.return_value = mock_driver
        mock_driver.find_elements.return_value = [mock_control_instance1, mock_control_instance2]
        
        # 调用find_controls方法
        mock_window = Mock()
        locator = "Edit:"
        controls = self.control_service.find_controls(mock_window, locator)
        
        # 验证结果
        self.assertEqual(len(controls), 2)
        self.assertEqual(controls[0], mock_control_instance1)
        self.assertEqual(controls[1], mock_control_instance2)
        mock_driver.find_elements.assert_called_once_with(mock_window, locator)
    
    @patch('rf_win.services.control_service.DriverFactory.create_driver')
    def test_click_control(self, mock_create_driver):
        """测试点击控件"""
        # 模拟驱动
        mock_driver = Mock()
        mock_create_driver.return_value = mock_driver
        
        # 调用click_control方法
        mock_control = Mock()
        self.control_service.click_control(mock_control)
        
        # 验证结果
        mock_driver.click_element.assert_called_once_with(mock_control)
    
    @patch('rf_win.services.control_service.DriverFactory.create_driver')
    def test_set_control_text(self, mock_create_driver):
        """测试设置控件文本"""
        # 模拟驱动
        mock_driver = Mock()
        mock_create_driver.return_value = mock_driver
        
        # 调用set_control_text方法
        mock_control = Mock()
        text = "Test Text"
        self.control_service.set_control_text(mock_control, text)
        
        # 验证结果
        mock_driver.set_element_text.assert_called_once_with(mock_control, text)
    
    @patch('rf_win.services.control_service.DriverFactory.create_driver')
    def test_get_control_text(self, mock_create_driver):
        """测试获取控件文本"""
        # 模拟驱动
        mock_driver = Mock()
        mock_control = Mock()
        expected_text = "Test Text"
        mock_create_driver.return_value = mock_driver
        mock_driver.get_element_text.return_value = expected_text
        
        # 调用get_control_text方法
        actual_text = self.control_service.get_control_text(mock_control)
        
        # 验证结果
        self.assertEqual(actual_text, expected_text)
        mock_driver.get_element_text.assert_called_once_with(mock_control)
    
    @patch('rf_win.services.control_service.DriverFactory.create_driver')
    def test_clear_control_text(self, mock_create_driver):
        """测试清空控件文本"""
        # 模拟驱动
        mock_driver = Mock()
        mock_create_driver.return_value = mock_driver
        
        # 调用clear_control_text方法
        mock_control = Mock()
        self.control_service.clear_control_text(mock_control)
        
        # 验证结果
        mock_driver.clear_element_text.assert_called_once_with(mock_control)


class TestOperationService(unittest.TestCase):
    """测试OperationService类"""
    
    def setUp(self):
        """初始化测试环境"""
        self.operation_service = OperationService()
    
    def test_operation_service_initialization(self):
        """测试OperationService初始化"""
        self.assertIsInstance(self.operation_service, OperationService)
    
    @patch('rf_win.services.operation_service.DriverFactory.create_driver')
    def test_click_mouse(self, mock_create_driver):
        """测试点击鼠标"""
        # 模拟驱动
        mock_driver = Mock()
        mock_create_driver.return_value = mock_driver
        
        # 调用click_mouse方法
        x = 100
        y = 200
        button = "left"
        self.operation_service.click_mouse(x, y, button)
        
        # 验证结果
        mock_driver.click_mouse.assert_called_once_with(x, y, button)
    
    @patch('rf_win.services.operation_service.DriverFactory.create_driver')
    def test_move_mouse(self, mock_create_driver):
        """测试移动鼠标"""
        # 模拟驱动
        mock_driver = Mock()
        mock_create_driver.return_value = mock_driver
        
        # 调用move_mouse方法
        x = 100
        y = 200
        self.operation_service.move_mouse(x, y)
        
        # 验证结果
        mock_driver.move_mouse.assert_called_once_with(x, y)
    
    @patch('rf_win.services.operation_service.DriverFactory.create_driver')
    def test_type_text(self, mock_create_driver):
        """测试输入文本"""
        # 模拟驱动
        mock_driver = Mock()
        mock_create_driver.return_value = mock_driver
        
        # 调用type_text方法
        text = "Test Text"
        self.operation_service.type_text(text)
        
        # 验证结果
        mock_driver.type_text.assert_called_once_with(text)
    
    @patch('rf_win.services.operation_service.DriverFactory.create_driver')
    def test_capture_screenshot(self, mock_create_driver):
        """测试截图功能"""
        # 模拟驱动
        mock_driver = Mock()
        expected_filename = "screenshot.png"
        mock_create_driver.return_value = mock_driver
        mock_driver.capture_screenshot.return_value = expected_filename
        
        # 调用capture_screenshot方法
        actual_filename = self.operation_service.capture_screenshot(expected_filename)
        
        # 验证结果
        self.assertEqual(actual_filename, expected_filename)
        mock_driver.capture_screenshot.assert_called_once_with(expected_filename, None)
    
    @patch('rf_win.services.operation_service.DriverFactory.create_driver')
    def test_wait_for_condition(self, mock_create_driver):
        """测试等待条件"""
        # 模拟驱动
        mock_driver = Mock()
        expected_result = True
        mock_create_driver.return_value = mock_driver
        mock_driver.wait_for_condition.return_value = expected_result
        
        # 调用wait_for_condition方法
        actual_result = self.operation_service.wait_for_condition("visible", timeout=5)
        
        # 验证结果
        self.assertEqual(actual_result, expected_result)
        mock_driver.wait_for_condition.assert_called_once_with("visible", timeout=5)


if __name__ == '__main__':
    unittest.main(verbosity=2)
