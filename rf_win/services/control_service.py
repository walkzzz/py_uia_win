# 控件服务模块
# 封装控件操作的核心业务逻辑

from typing import Any, Dict, List, Optional
from ..drivers.automation_driver import driver_factory
from ..utils.cache import ControlCache
from ..utils.logger import logger

class ControlService:
    """控件服务，负责控件操作的核心业务逻辑"""
    
    def __init__(self):
        self._driver = driver_factory.get_driver()
        self._cache = ControlCache()
    
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
