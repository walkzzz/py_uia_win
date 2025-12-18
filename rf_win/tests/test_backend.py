#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
后端实现测试

测试rf_win.backend模块中的后端工厂和具体后端实现，确保它们能够正确地创建和管理后端实例
"""

import unittest
from unittest.mock import Mock, patch
from rf_win.backend.backend_factory import BackendFactory
from rf_win.backend.pywinauto_backend import PywinautoBackend


class TestBackendFactory(unittest.TestCase):
    """测试BackendFactory类"""
    
    def setUp(self):
        """初始化测试环境"""
        self.backend_factory = BackendFactory()
    
    def test_backend_factory_initialization(self):
        """测试后端工厂初始化"""
        self.assertIsInstance(self.backend_factory, BackendFactory)
    
    def test_get_backend_pywinauto(self):
        """测试获取pywinauto后端"""
        backend = self.backend_factory.get_backend("pywinauto")
        self.assertIsInstance(backend, PywinautoBackend)
    
    def test_get_backend_invalid(self):
        """测试获取无效后端时抛出异常"""
        with self.assertRaises(ValueError):
            self.backend_factory.get_backend("invalid_backend")
    
    def test_get_backend_default(self):
        """测试获取默认后端"""
        backend = self.backend_factory.get_backend()
        self.assertIsInstance(backend, PywinautoBackend)
    
    def test_backend_singleton(self):
        """测试后端工厂返回单例实例"""
        backend1 = self.backend_factory.get_backend("pywinauto")
        backend2 = self.backend_factory.get_backend("pywinauto")
        self.assertIs(backend1, backend2)
    
    def test_get_supported_backends(self):
        """测试获取支持的后端列表"""
        supported_backends = self.backend_factory.get_supported_backends()
        self.assertIsInstance(supported_backends, list)
        self.assertIn("pywinauto", supported_backends)
        self.assertIn("uiautomation", supported_backends)
    
    def test_is_backend_supported(self):
        """测试检查后端是否被支持"""
        self.assertTrue(self.backend_factory.is_backend_supported("pywinauto"))
        self.assertTrue(self.backend_factory.is_backend_supported("uiautomation"))
        self.assertFalse(self.backend_factory.is_backend_supported("invalid_backend"))


class TestPywinautoBackend(unittest.TestCase):
    """测试PywinautoBackend类"""
    
    def setUp(self):
        """初始化测试环境"""
        self.backend = PywinautoBackend()
    
    def test_pywinauto_backend_initialization(self):
        """测试pywinauto后端初始化"""
        self.assertIsInstance(self.backend, PywinautoBackend)
    
    def test_pywinauto_backend_has_attributes(self):
        """测试pywinauto后端具有所需的属性"""
        self.assertTrue(hasattr(self.backend, 'application'))
        self.assertTrue(hasattr(self.backend, 'window'))
        self.assertTrue(hasattr(self.backend, 'control'))
        self.assertTrue(hasattr(self.backend, 'operation'))
    
    @patch('rf_win.backend.pywinauto_backend.PywinautoApplication')
    def test_create_application(self, mock_pywinauto_app):
        """测试创建pywinauto应用实例"""
        mock_instance = Mock()
        mock_pywinauto_app.return_value = mock_instance
        
        app = self.backend.application
        self.assertEqual(app, mock_instance)
        mock_pywinauto_app.assert_called_once()
    
    @patch('rf_win.backend.pywinauto_backend.PywinautoWindow')
    def test_create_window(self, mock_pywinauto_window):
        """测试创建pywinauto窗口实例"""
        mock_instance = Mock()
        mock_pywinauto_window.return_value = mock_instance
        
        window = self.backend.window
        self.assertEqual(window, mock_instance)
        mock_pywinauto_window.assert_called_once()
    
    @patch('rf_win.backend.pywinauto_backend.PywinautoControl')
    def test_create_control(self, mock_pywinauto_control):
        """测试创建pywinauto控件实例"""
        mock_instance = Mock()
        mock_pywinauto_control.return_value = mock_instance
        
        control = self.backend.control
        self.assertEqual(control, mock_instance)
        mock_pywinauto_control.assert_called_once()
    
    @patch('rf_win.backend.pywinauto_backend.PywinautoOperation')
    def test_create_operation(self, mock_pywinauto_operation):
        """测试创建pywinauto操作实例"""
        mock_instance = Mock()
        mock_pywinauto_operation.return_value = mock_instance
        
        operation = self.backend.operation
        self.assertEqual(operation, mock_instance)
        mock_pywinauto_operation.assert_called_once()


if __name__ == '__main__':
    unittest.main(verbosity=2)
