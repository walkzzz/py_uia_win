# 定位器助手模块
# 提供定位器解析、生成和图形化拾取功能

from typing import Dict, Any, Optional, Tuple
import re

class LocatorHelper:
    """定位器助手类"""
    
    # 定位器类型映射
    LOCATOR_TYPES = {
        "id": "automation_id",
        "name": "name",
        "class": "class_name",
        "xpath": "xpath",
        "title": "title"
    }
    
    @staticmethod
    def parse_locator(locator: str) -> Dict[str, Any]:
        """解析定位器字符串
        
        将定位器字符串（如id=btn_login, name=登录）转换为定位器字典
        
        Args:
            locator: 定位器字符串
            
        Returns:
            定位器字典，包含type和value键
        
        Examples:
            >>> LocatorHelper.parse_locator("id=btn_login")
            {'type': 'id', 'value': 'btn_login', 'backend_key': 'automation_id'}
            >>> LocatorHelper.parse_locator("name=登录")
            {'type': 'name', 'value': '登录', 'backend_key': 'name'}
        """
        if not locator:
            raise ValueError("Locator cannot be empty")
        
        # 检查是否包含定位器类型前缀
        if "=" in locator:
            # 解析定位器类型和值
            locator_type, value = locator.split("=", 1)
            locator_type = locator_type.strip().lower()
            value = value.strip()
            
            if locator_type not in LocatorHelper.LOCATOR_TYPES:
                raise ValueError(f"Unknown locator type: {locator_type}")
            
            return {
                "type": locator_type,
                "value": value,
                "backend_key": LocatorHelper.LOCATOR_TYPES[locator_type]
            }
        else:
            # 默认使用title定位
            return {
                "type": "title",
                "value": locator,
                "backend_key": "title"
            }
    
    @staticmethod
    def generate_locator(locator_type: str, value: str) -> str:
        """生成定位器字符串
        
        Args:
            locator_type: 定位器类型
            value: 定位器值
            
        Returns:
            定位器字符串
            
        Examples:
            >>> LocatorHelper.generate_locator("id", "btn_login")
            "id=btn_login"
            >>> LocatorHelper.generate_locator("name", "登录")
            "name=登录"
        """
        if locator_type not in LocatorHelper.LOCATOR_TYPES:
            raise ValueError(f"Unknown locator type: {locator_type}")
        
        return f"{locator_type}={value}"
    
    @staticmethod
    def is_valid_locator(locator: str) -> bool:
        """检查定位器是否有效
        
        Args:
            locator: 定位器字符串
            
        Returns:
            定位器是否有效
        """
        try:
            LocatorHelper.parse_locator(locator)
            return True
        except ValueError:
            return False
    
    @staticmethod
    def extract_locator_type(locator: str) -> str:
        """提取定位器类型
        
        Args:
            locator: 定位器字符串
            
        Returns:
            定位器类型
        """
        parsed = LocatorHelper.parse_locator(locator)
        return parsed["type"]
    
    @staticmethod
    def extract_locator_value(locator: str) -> str:
        """提取定位器值
        
        Args:
            locator: 定位器字符串
            
        Returns:
            定位器值
        """
        parsed = LocatorHelper.parse_locator(locator)
        return parsed["value"]
    
    @staticmethod
    def convert_to_backend_locator(locator: str) -> Dict[str, str]:
        """将通用定位器转换为后端特定的定位器
        
        Args:
            locator: 通用定位器字符串
            
        Returns:
            后端特定的定位器字典
        """
        parsed = LocatorHelper.parse_locator(locator)
        return {
            parsed["backend_key"]: parsed["value"]
        }
    
    @staticmethod
    def merge_locators(*locators: str) -> str:
        """合并多个定位器
        
        Args:
            *locators: 定位器字符串列表
            
        Returns:
            合并后的定位器字符串
            
        Example:
            >>> LocatorHelper.merge_locators("id=btn_login", "name=登录")
            "id=btn_login,name=登录"
        """
        return ",".join(locators)
    
    @staticmethod
    def split_locators(locator: str) -> list:
        """分割合并的定位器
        
        Args:
            locator: 合并的定位器字符串
            
        Returns:
            定位器字符串列表
            
        Example:
            >>> LocatorHelper.split_locators("id=btn_login,name=登录")
            ["id=btn_login", "name=登录"]
        """
        return [l.strip() for l in locator.split(",")]
    
    @staticmethod
    def pick_element() -> Optional[Dict[str, Any]]:
        """图形化拾取控件
        
        启动图形化工具，允许用户通过鼠标选择控件，并返回控件的定位器信息
        
        Returns:
            控件定位器信息字典，如果拾取失败则返回None
        """
        try:
            # 尝试导入必要的库
            import tkinter as tk
            from tkinter import ttk, messagebox
            import win32gui
            import win32con
            import time
            
            class ElementPicker:
                """元素拾取器类"""
                
                def __init__(self):
                    self.root = tk.Tk()
                    self.root.title("元素拾取器")
                    self.root.geometry("500x300")
                    self.root.resizable(False, False)
                    
                    # 半透明效果
                    self.root.attributes("-alpha", 0.8)
                    
                    # 元素信息
                    self.element_info = {}
                    self.is_picking = False
                    
                    # 创建UI
                    self.create_ui()
                    
                def create_ui(self):
                    """创建UI"""
                    # 标题
                    title_label = ttk.Label(self.root, text="元素拾取器", font=("Arial", 14, "bold"))
                    title_label.pack(pady=10)
                    
                    # 提示信息
                    info_label = ttk.Label(self.root, text="按下Ctrl键并点击目标控件来拾取元素信息")
                    info_label.pack(pady=5)
                    
                    # 元素信息显示区域
                    self.info_text = tk.Text(self.root, width=60, height=10, wrap=tk.WORD)
                    self.info_text.pack(pady=10, padx=10)
                    self.info_text.config(state=tk.DISABLED)
                    
                    # 按钮
                    button_frame = ttk.Frame(self.root)
                    button_frame.pack(pady=10)
                    
                    pick_button = ttk.Button(button_frame, text="开始拾取", command=self.start_pick)
                    pick_button.pack(side=tk.LEFT, padx=5)
                    
                    copy_button = ttk.Button(button_frame, text="复制定位器", command=self.copy_locator)
                    copy_button.pack(side=tk.LEFT, padx=5)
                    
                    exit_button = ttk.Button(button_frame, text="退出", command=self.root.destroy)
                    exit_button.pack(side=tk.LEFT, padx=5)
                    
                def start_pick(self):
                    """开始拾取"""
                    self.is_picking = True
                    self.info_text.config(state=tk.NORMAL)
                    self.info_text.delete(1.0, tk.END)
                    self.info_text.insert(tk.END, "开始拾取元素...\n")
                    self.info_text.config(state=tk.DISABLED)
                    
                    # 注册全局热键
                    self.root.bind("<Control_L>", self.on_ctrl_press)
                    self.root.bind("<Button-1>", self.on_mouse_click)
                    
                def on_ctrl_press(self, event):
                    """Ctrl键按下事件"""
                    self.is_picking = True
                    
                def on_mouse_click(self, event):
                    """鼠标点击事件"""
                    if self.is_picking:
                        # 获取鼠标位置
                        x, y = self.root.winfo_pointerx(), self.root.winfo_pointery()
                        
                        # 获取窗口句柄
                        hwnd = win32gui.WindowFromPoint((x, y))
                        if hwnd:
                            # 获取窗口信息
                            title = win32gui.GetWindowText(hwnd)
                            class_name = win32gui.GetClassName(hwnd)
                            
                            # 获取控件信息
                            element_info = {
                                "title": title,
                                "class_name": class_name,
                                "hwnd": hwnd,
                                "position": (x, y)
                            }
                            
                            # 尝试获取自动化ID（需要uiautomation库）
                            try:
                                import uiautomation as auto
                                element = auto.ControlFromPoint(x, y)
                                automation_id = element.AutomationId
                                element_info["automation_id"] = automation_id
                                element_info["name"] = element.Name
                                element_info["control_type"] = element.ControlType
                            except ImportError:
                                pass
                            except Exception:
                                pass
                            
                            self.element_info = element_info
                            self.display_element_info(element_info)
                        
                        self.is_picking = False
                    
                def display_element_info(self, element_info: Dict[str, Any]):
                    """显示元素信息"""
                    self.info_text.config(state=tk.NORMAL)
                    self.info_text.delete(1.0, tk.END)
                    
                    info_str = "元素信息：\n"
                    for key, value in element_info.items():
                        info_str += f"{key}: {value}\n"
                    
                    # 生成定位器
                    locators = []
                    if "automation_id" in element_info and element_info["automation_id"]:
                        locators.append(f"id={element_info['automation_id']}")
                    if "name" in element_info and element_info["name"]:
                        locators.append(f"name={element_info['name']}")
                    if "class_name" in element_info and element_info["class_name"]:
                        locators.append(f"class={element_info['class_name']}")
                    if "title" in element_info and element_info["title"]:
                        locators.append(f"title={element_info['title']}")
                    
                    if locators:
                        info_str += "\n推荐定位器：\n"
                        info_str += "\n".join(locators)
                    
                    self.info_text.insert(tk.END, info_str)
                    self.info_text.config(state=tk.DISABLED)
                    
                def copy_locator(self):
                    """复制定位器到剪贴板"""
                    if not self.element_info:
                        messagebox.showinfo("提示", "请先拾取元素")
                        return
                    
                    # 生成定位器
                    locators = []
                    if "automation_id" in self.element_info and self.element_info["automation_id"]:
                        locators.append(f"id={self.element_info['automation_id']}")
                    elif "name" in self.element_info and self.element_info["name"]:
                        locators.append(f"name={self.element_info['name']}")
                    elif "title" in self.element_info and self.element_info["title"]:
                        locators.append(f"title={self.element_info['title']}")
                    
                    if locators:
                        locator = locators[0]
                        self.root.clipboard_clear()
                        self.root.clipboard_append(locator)
                        messagebox.showinfo("提示", f"定位器已复制到剪贴板：\n{locator}")
                    else:
                        messagebox.showinfo("提示", "无法生成定位器")
                    
                def run(self):
                    """运行拾取器"""
                    self.root.mainloop()
            
            # 启动拾取器
            picker = ElementPicker()
            picker.run()
            
            return picker.element_info
        except ImportError as e:
            print(f"Error importing required modules for element picking: {e}")
            return None
        except Exception as e:
            print(f"Error picking element: {e}")
            return None
    
    @staticmethod
    def validate_xpath(xpath: str) -> bool:
        """验证XPath表达式是否有效
        
        Args:
            xpath: XPath表达式
            
        Returns:
            XPath表达式是否有效
        """
        try:
            # 简单验证XPath格式
            if not xpath:
                return False
            
            # 检查是否包含基本XPath语法
            xpath = xpath.strip()
            if xpath.startswith("/") or xpath.startswith("//") or "[@" in xpath or "/" in xpath:
                return True
            return False
        except Exception:
            return False
    
    @staticmethod
    def generate_xpath(locator: str) -> str:
        """根据定位器生成XPath表达式
        
        Args:
            locator: 定位器字符串
            
        Returns:
            XPath表达式
        """
        parsed = LocatorHelper.parse_locator(locator)
        
        if parsed["type"] == "xpath":
            return parsed["value"]
        
        # 根据定位器类型生成XPath
        if parsed["type"] == "id":
            return f"//*[@AutomationId='{parsed['value']}']"
        elif parsed["type"] == "name":
            return f"//*[@Name='{parsed['value']}']"
        elif parsed["type"] == "class":
            return f"//{parsed['value']}"
        elif parsed["type"] == "title":
            return f"//*[contains(@Name, '{parsed['value']}')]"
        
        return f"//*[contains(@Name, '{parsed['value']}')]"

# 创建定位器助手实例
locator_helper = LocatorHelper()
