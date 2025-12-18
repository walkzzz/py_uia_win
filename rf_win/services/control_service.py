# 控件服务模块
# 封装控件操作的核心业务逻辑

from typing import Any, Dict, List, Optional
from ..drivers.automation_driver import driver_factory
from ..utils.cache_manager import cache_manager
from ..utils.logger import logger
from .application_service import ApplicationService
from .window_service import WindowService

class ControlService:
    """控件服务，负责控件操作的核心业务逻辑"""
    
    def __init__(self):
        self._driver = driver_factory.get_driver()
        # 创建应用服务和窗口服务实例
        self.app_service = ApplicationService()
        self.window_service = WindowService()
        # 简单的控件缓存
        self._control_cache: Dict[str, Any] = {}
    
    def find_control(self, locator, window_title=None, app_alias=None, timeout=None):
        """查找控件
        
        根据定位器查找指定窗口中的控件
        
        参数:
            locator: 控件定位器，格式为"类型:属性=值"
            window_title: 窗口标题，可以是完整标题或正则表达式
            app_alias: 应用程序的别名
            timeout: 查找超时时间，单位为秒
        
        返回:
            控件实例
        """
        logger.info(f"查找控件: 定位器={locator}, 窗口标题={window_title}, 应用别名={app_alias}, 超时={timeout}")
        
        # 获取窗口实例
        window = self.window_service.switch_window(window_title, app_alias)
        if not window:
            logger.error(f"未找到窗口: {window_title}")
            return None
        
        # 调用驱动的查找控件方法
        return self._driver.find_element(window, locator, timeout or 10.0)
    
    def find_all_controls(self, locator, window_title=None, app_alias=None, timeout=None):
        """查找所有匹配的控件
        
        根据定位器查找指定窗口中的所有匹配控件
        
        参数:
            locator: 控件定位器，格式为"类型:属性=值"
            window_title: 窗口标题，可以是完整标题或正则表达式
            app_alias: 应用程序的别名
            timeout: 查找超时时间，单位为秒
        
        返回:
            控件实例列表
        """
        logger.info(f"查找所有控件: 定位器={locator}, 窗口标题={window_title}, 应用别名={app_alias}, 超时={timeout}")
        
        # 获取窗口实例
        window = self.window_service.switch_window(window_title, app_alias)
        if not window:
            logger.error(f"未找到窗口: {window_title}")
            return []
        
        # 调用驱动的查找所有控件方法
        return self._driver.find_elements(window, locator, timeout or 10.0)
    
    def click_control(self, locator, window_title=None, app_alias=None, button='left', double=False, timeout=None):
        """点击控件
        
        点击指定的控件
        
        参数:
            locator: 控件定位器，格式为"类型:属性=值"
            window_title: 窗口标题，可以是完整标题或正则表达式
            app_alias: 应用程序的别名
            button: 鼠标按钮，可选值为'left'、'right'、'middle'
            double: 是否双击，默认为False
            timeout: 查找超时时间，单位为秒
        
        返回:
            是否成功
        """
        logger.info(f"点击控件: 定位器={locator}, 窗口标题={window_title}, 应用别名={app_alias}, 按钮={button}, 双击={double}, 超时={timeout}")
        
        # 查找控件
        control = self.find_control(locator, window_title, app_alias, timeout)
        if not control:
            return False
        
        # 调用驱动的点击方法
        clicks = 2 if double else 1
        return self._driver.click_element(control, button, clicks, 0.1 if double else 0.0)
    
    def set_control_text(self, locator, text, window_title=None, app_alias=None, timeout=None, clear_first=True):
        """控件输入文本
        
        向指定控件输入文本
        
        参数:
            locator: 控件定位器，格式为"类型:属性=值"
            text: 要输入的文本
            window_title: 窗口标题，可以是完整标题或正则表达式
            app_alias: 应用程序的别名
            timeout: 查找超时时间，单位为秒
            clear_first: 是否先清空控件内容，默认为True
        
        返回:
            是否成功
        """
        logger.info(f"控件输入文本: 定位器={locator}, 文本={text}, 窗口标题={window_title}, 应用别名={app_alias}, 超时={timeout}, 清空={clear_first}")
        
        # 查找控件
        control = self.find_control(locator, window_title, app_alias, timeout)
        if not control:
            return False
        
        # 调用驱动的输入文本方法
        if clear_first:
            self._driver.clear_element_text(control)
        return self._driver.type_text(control, text, 0.0)
    
    def get_control_text(self, locator, window_title=None, app_alias=None, timeout=None):
        """获取控件文本
        
        获取指定控件的文本内容
        
        参数:
            locator: 控件定位器，格式为"类型:属性=值"
            window_title: 窗口标题，可以是完整标题或正则表达式
            app_alias: 应用程序的别名
            timeout: 查找超时时间，单位为秒
        
        返回:
            控件的文本内容
        """
        logger.info(f"获取控件文本: 定位器={locator}, 窗口标题={window_title}, 应用别名={app_alias}, 超时={timeout}")
        
        # 查找控件
        control = self.find_control(locator, window_title, app_alias, timeout)
        if not control:
            return None
        
        # 调用驱动的获取文本方法
        return self._driver.get_element_text(control)
    
    def clear_control_text(self, locator, window_title=None, app_alias=None, timeout=None):
        """清空控件文本
        
        清空指定控件的文本内容
        
        参数:
            locator: 控件定位器，格式为"类型:属性=值"
            window_title: 窗口标题，可以是完整标题或正则表达式
            app_alias: 应用程序的别名
            timeout: 查找超时时间，单位为秒
        
        返回:
            是否成功
        """
        logger.info(f"清空控件文本: 定位器={locator}, 窗口标题={window_title}, 应用别名={app_alias}, 超时={timeout}")
        
        # 查找控件
        control = self.find_control(locator, window_title, app_alias, timeout)
        if not control:
            return False
        
        # 调用驱动的清空文本方法
        return self._driver.clear_element_text(control)
    
    def select_control_item(self, locator, item, window_title=None, app_alias=None, timeout=None):
        """选择控件项
        
        选择下拉列表或列表框中的项
        
        参数:
            locator: 控件定位器，格式为"类型:属性=值"
            item: 要选择的项，可以是文本或索引
            window_title: 窗口标题，可以是完整标题或正则表达式
            app_alias: 应用程序的别名
            timeout: 查找超时时间，单位为秒
        
        返回:
            是否成功
        """
        logger.info(f"选择控件项: 定位器={locator}, 项={item}, 窗口标题={window_title}, 应用别名={app_alias}, 超时={timeout}")
        
        # 查找控件
        control = self.find_control(locator, window_title, app_alias, timeout)
        if not control:
            return False
        
        # 调用驱动的选择方法
        return self._driver.select_element(control, text=item if isinstance(item, str) else None, index=int(item) if isinstance(item, (int, str)) and str(item).isdigit() else -1)
    
    def get_control_items(self, locator, window_title=None, app_alias=None, timeout=None):
        """获取控件项列表
        
        获取下拉列表或列表框中的所有项
        
        参数:
            locator: 控件定位器，格式为"类型:属性=值"
            window_title: 窗口标题，可以是完整标题或正则表达式
            app_alias: 应用程序的别名
            timeout: 查找超时时间，单位为秒
        
        返回:
            控件项列表
        """
        logger.info(f"获取控件项: 定位器={locator}, 窗口标题={window_title}, 应用别名={app_alias}, 超时={timeout}")
        
        # 查找控件
        control = self.find_control(locator, window_title, app_alias, timeout)
        if not control:
            return []
        
        # 这里需要根据控件类型实现获取项的逻辑
        # 由于驱动可能没有直接支持，这里返回一个空列表
        # 实际实现需要根据具体的驱动和控件类型进行调整
        return []
    
    def is_control_exists(self, locator, window_title=None, app_alias=None, timeout=None):
        """检查控件是否存在
        
        检查指定的控件是否存在
        
        参数:
            locator: 控件定位器，格式为"类型:属性=值"
            window_title: 窗口标题，可以是完整标题或正则表达式
            app_alias: 应用程序的别名
            timeout: 查找超时时间，单位为秒
        
        返回:
            True如果控件存在，否则返回False
        """
        logger.info(f"检查控件是否存在: 定位器={locator}, 窗口标题={window_title}, 应用别名={app_alias}, 超时={timeout}")
        
        # 尝试查找控件，如果找到则返回True，否则返回False
        control = self.find_control(locator, window_title, app_alias, timeout or 0.1)
        return control is not None
    
    def is_control_visible(self, locator, window_title=None, app_alias=None, timeout=None):
        """检查控件是否可见
        
        检查指定的控件是否可见
        
        参数:
            locator: 控件定位器，格式为"类型:属性=值"
            window_title: 窗口标题，可以是完整标题或正则表达式
            app_alias: 应用程序的别名
            timeout: 查找超时时间，单位为秒
        
        返回:
            True如果控件可见，否则返回False
        """
        logger.info(f"检查控件是否可见: 定位器={locator}, 窗口标题={window_title}, 应用别名={app_alias}, 超时={timeout}")
        
        # 查找控件
        control = self.find_control(locator, window_title, app_alias, timeout)
        if not control:
            return False
        
        # 调用驱动的检查可见性方法
        return self._driver.is_element_visible(control)
    
    def is_control_enabled(self, locator, window_title=None, app_alias=None, timeout=None):
        """检查控件是否启用
        
        检查指定的控件是否启用
        
        参数:
            locator: 控件定位器，格式为"类型:属性=值"
            window_title: 窗口标题，可以是完整标题或正则表达式
            app_alias: 应用程序的别名
            timeout: 查找超时时间，单位为秒
        
        返回:
            True如果控件启用，否则返回False
        """
        logger.info(f"检查控件是否启用: 定位器={locator}, 窗口标题={window_title}, 应用别名={app_alias}, 超时={timeout}")
        
        # 查找控件
        control = self.find_control(locator, window_title, app_alias, timeout)
        if not control:
            return False
        
        # 调用驱动的检查启用状态方法
        return self._driver.is_element_enabled(control)
    
    def get_control_property(self, locator, property_name, window_title=None, app_alias=None, timeout=None):
        """获取控件属性
        
        获取指定控件的指定属性值
        
        参数:
            locator: 控件定位器，格式为"类型:属性=值"
            property_name: 属性名称
            window_title: 窗口标题，可以是完整标题或正则表达式
            app_alias: 应用程序的别名
            timeout: 查找超时时间，单位为秒
        
        返回:
            控件属性值
        """
        logger.info(f"获取控件属性: 定位器={locator}, 属性名={property_name}, 窗口标题={window_title}, 应用别名={app_alias}, 超时={timeout}")
        
        # 查找控件
        control = self.find_control(locator, window_title, app_alias, timeout)
        if not control:
            return None
        
        # 调用驱动的获取属性方法
        return self._driver.get_element_attribute(control, property_name)
    
    def set_control_property(self, locator, property_name, value, window_title=None, app_alias=None, timeout=None):
        """设置控件属性
        
        设置指定控件的指定属性值
        
        参数:
            locator: 控件定位器，格式为"类型:属性=值"
            property_name: 属性名称
            value: 要设置的属性值
            window_title: 窗口标题，可以是完整标题或正则表达式
            app_alias: 应用程序的别名
            timeout: 查找超时时间，单位为秒
        
        返回:
            是否成功
        """
        logger.info(f"设置控件属性: 定位器={locator}, 属性名={property_name}, 值={value}, 窗口标题={window_title}, 应用别名={app_alias}, 超时={timeout}")
        
        # 查找控件
        control = self.find_control(locator, window_title, app_alias, timeout)
        if not control:
            return False
        
        # 调用驱动的设置属性方法
        # 注意：不是所有控件都支持直接设置属性，这里可能需要根据具体情况调整
        return self._driver.set_element_text(control, value) if property_name.lower() == 'text' or property_name.lower() == 'value' else False
    
    def find_element(self, parent: Any, locator: Any, timeout: float = 10.0) -> Any:
        """查找单个控件
        
        Args:
            parent: 父控件或窗口对象
            locator: 控件定位器
            timeout: 超时时间
        
        Returns:
            控件对象
        
        Raises:
            TimeoutError: 如果超时
        """
        logger.info(f"Finding element: parent={parent}, locator={locator}, timeout={timeout}")
        
        # 尝试从缓存中获取
        cache_key = f"{id(parent)}:{str(locator)}:{timeout}"
        cached_element = self._cache.get(cache_key)
        if cached_element and self._driver.is_element_valid(cached_element):
            logger.info(f"Found element from cache: {cached_element}")
            return cached_element
        
        # 缓存未命中，执行查找
        element = self._driver.find_element(parent, locator, timeout)
        
        # 缓存结果
        self._cache.set(cache_key, element, ttl=300)  # 缓存5分钟
        
        logger.info(f"Found element: {element}")
        return element
    
    def find_elements(self, parent: Any, locator: Any, timeout: float = 10.0) -> List[Any]:
        """查找多个控件
        
        Args:
            parent: 父控件或窗口对象
            locator: 控件定位器
            timeout: 超时时间
        
        Returns:
            控件对象列表
        """
        logger.info(f"Finding elements: parent={parent}, locator={locator}, timeout={timeout}")
        return self._driver.find_elements(parent, locator, timeout)
    
    def click_element(self, element: Any, button: str = "left", clicks: int = 1, interval: float = 0.0) -> bool:
        """点击控件
        
        Args:
            element: 控件对象
            button: 鼠标按钮，可选值：left, right, middle
            clicks: 点击次数
            interval: 点击间隔（秒）
        
        Returns:
            是否成功
        """
        logger.info(f"Clicking element: {element}, button={button}, clicks={clicks}, interval={interval}")
        try:
            self._driver.click_element(element, button, clicks, interval)
            return True
        except Exception as e:
            logger.error(f"Failed to click element: {e}")
            return False
    
    def right_click_element(self, element: Any) -> bool:
        """右键点击控件
        
        Args:
            element: 控件对象
        
        Returns:
            是否成功
        """
        return self.click_element(element, button="right")
    
    def double_click_element(self, element: Any) -> bool:
        """双击控件
        
        Args:
            element: 控件对象
        
        Returns:
            是否成功
        """
        return self.click_element(element, clicks=2, interval=0.1)
    
    def type_text(self, element: Any, text: str, clear_first: bool = True, delay: float = 0.0) -> bool:
        """向控件输入文本
        
        Args:
            element: 控件对象
            text: 要输入的文本
            clear_first: 是否先清空控件内容
            delay: 输入延迟（秒）
        
        Returns:
            是否成功
        """
        logger.info(f"Typing text into element: {element}, text={text}, clear_first={clear_first}, delay={delay}")
        try:
            if clear_first:
                self.clear_element_text(element)
            self._driver.type_text(element, text, delay)
            return True
        except Exception as e:
            logger.error(f"Failed to type text: {e}")
            return False
    
    def clear_element_text(self, element: Any) -> bool:
        """清空控件文本
        
        Args:
            element: 控件对象
        
        Returns:
            是否成功
        """
        logger.info(f"Clearing text from element: {element}")
        try:
            self._driver.clear_element_text(element)
            return True
        except Exception as e:
            logger.error(f"Failed to clear text: {e}")
            return False
    
    def get_element_text(self, element: Any) -> Optional[str]:
        """获取控件文本
        
        Args:
            element: 控件对象
        
        Returns:
            控件文本
        """
        logger.info(f"Getting text from element: {element}")
        try:
            return self._driver.get_element_text(element)
        except Exception as e:
            logger.error(f"Failed to get element text: {e}")
            return None
    
    def set_element_text(self, element: Any, text: str) -> bool:
        """设置控件文本（直接设置，不模拟输入）
        
        Args:
            element: 控件对象
            text: 要设置的文本
        
        Returns:
            是否成功
        """
        logger.info(f"Setting text for element: {element}, text={text}")
        try:
            self._driver.set_element_text(element, text)
            return True
        except Exception as e:
            logger.error(f"Failed to set element text: {e}")
            return False
    
    def get_element_attribute(self, element: Any, attribute: str) -> Optional[Any]:
        """获取控件属性
        
        Args:
            element: 控件对象
            attribute: 属性名称
        
        Returns:
            属性值
        """
        logger.info(f"Getting attribute from element: {element}, attribute={attribute}")
        try:
            return self._driver.get_element_attribute(element, attribute)
        except Exception as e:
            logger.error(f"Failed to get element attribute: {e}")
            return None
    
    def is_element_enabled(self, element: Any) -> bool:
        """检查控件是否可用
        
        Args:
            element: 控件对象
        
        Returns:
            是否可用
        """
        logger.info(f"Checking if element is enabled: {element}")
        try:
            return self._driver.is_element_enabled(element)
        except Exception as e:
            logger.error(f"Failed to check if element is enabled: {e}")
            return False
    
    def is_element_visible(self, element: Any) -> bool:
        """检查控件是否可见
        
        Args:
            element: 控件对象
        
        Returns:
            是否可见
        """
        logger.info(f"Checking if element is visible: {element}")
        try:
            return self._driver.is_element_visible(element)
        except Exception as e:
            logger.error(f"Failed to check if element is visible: {e}")
            return False
    
    def hover_element(self, element: Any) -> bool:
        """鼠标悬停在控件上
        
        Args:
            element: 控件对象
        
        Returns:
            是否成功
        """
        logger.info(f"Hovering over element: {element}")
        try:
            self._driver.hover_element(element)
            return True
        except Exception as e:
            logger.error(f"Failed to hover over element: {e}")
            return False
    
    def drag_element_to(self, source_element: Any, target_element: Any) -> bool:
        """拖拽控件到目标位置
        
        Args:
            source_element: 源控件对象
            target_element: 目标控件对象
        
        Returns:
            是否成功
        """
        logger.info(f"Dragging element: {source_element} to: {target_element}")
        try:
            self._driver.drag_element_to(source_element, target_element)
            return True
        except Exception as e:
            logger.error(f"Failed to drag element: {e}")
            return False
    
    def select_element(self, element: Any, value: Any = None, text: Optional[str] = None, index: int = -1) -> bool:
        """选择控件选项（适用于下拉列表、单选按钮等）
        
        Args:
            element: 控件对象
            value: 选项值
            text: 选项文本
            index: 选项索引
        
        Returns:
            是否成功
        """
        logger.info(f"Selecting element: {element}, value={value}, text={text}, index={index}")
        try:
            self._driver.select_element(element, value, text, index)
            return True
        except Exception as e:
            logger.error(f"Failed to select element: {e}")
            return False
    
    def deselect_element(self, element: Any, value: Any = None, text: Optional[str] = None, index: int = -1) -> bool:
        """取消选择控件选项（适用于复选框等）
        
        Args:
            element: 控件对象
            value: 选项值
            text: 选项文本
            index: 选项索引
        
        Returns:
            是否成功
        """
        logger.info(f"Deselecting element: {element}, value={value}, text={text}, index={index}")
        try:
            self._driver.deselect_element(element, value, text, index)
            return True
        except Exception as e:
            logger.error(f"Failed to deselect element: {e}")
            return False
    
    def is_element_selected(self, element: Any) -> bool:
        """检查控件是否被选中
        
        Args:
            element: 控件对象
        
        Returns:
            是否被选中
        """
        logger.info(f"Checking if element is selected: {element}")
        try:
            return self._driver.is_element_selected(element)
        except Exception as e:
            logger.error(f"Failed to check if element is selected: {e}")
            return False
