# 控件操作关键字模块
# 实现控件相关的Robot Framework关键字

from typing import Any, List, Optional
from robot.api import logger

from ..core.base_control import BaseControl

class ControlOperationsKeywords:
    """控件操作关键字类
    
    提供控件相关的关键字，包括：
    - 查找控件
    - 点击控件
    - 双击控件
    - 右键点击控件
    - 向控件输入文本
    - 获取控件文本
    - 选中/取消选中控件
    - 检查控件状态
    - 获取/设置控件属性
    - 鼠标悬停
    - 拖拽控件
    """
    
    def __init__(self, library):
        """初始化控件操作关键字
        
        Args:
            library: 主库实例，用于访问应用、窗口、控件管理器
        """
        self._library = library
        self._windows = library._windows
        self._controls = library._controls
        self._get_backend = library._get_backend
        self._get_window = library._get_window
        self._get_control = library._get_control
        self._add_control = library._add_control
        self._remove_control = library._remove_control
        self._control_service = library._control_service
        
    def find_element(self, window_id: str, locator: str, control_id: Optional[str] = None) -> str:
        """查找窗口中的控件
        
        Args:
            window_id: 窗口ID
            locator: 控件定位器
                     - id=xxx: 自动化ID定位
                     - name=xxx: 名称定位
                     - class=xxx: 类名定位
                     - xpath=xxx: XPath定位
                     - 默认为标题定位
            control_id: 控件ID，用于后续操作，如果为None则自动生成
        
        Returns:
            控件ID
        
        Example:
            | ${btn_id} | Find Element | notepad_window | id=btn_login | control_id=login_button |
            | ${edit_id} | Find Element | notepad_window | name=用户名 | control_id=username_edit |
        """
        import time
        from ..config.global_config import global_config
        
        window = self._get_window(window_id)
        if not window:
            raise ValueError(f"Window not found: {window_id}")
        
        # 使用服务层查找元素
        element = self._control_service.find_element(window._window, locator, global_config.timeout)
        if not element:
            raise RuntimeError(f"Failed to find element with locator: {locator} in window: {window_id}")
        
        if control_id is None:
            control_id = f"control_{int(time.time())}"
        
        backend_instance = self._get_backend()
        control = backend_instance.create_control(element, window)
        self._add_control(control_id, control)
        
        logger.info(f"Found element with locator: {locator} in window: {window_id}, control_id: {control_id}")
        return control_id
    
    def click_element(self, control_id: str, button: str = "left", count: int = 1, x_offset: int = 0, y_offset: int = 0) -> bool:
        """点击控件
        
        Args:
            control_id: 控件ID
            button: 鼠标按钮（left, right, middle），默认left
            count: 点击次数（1: 单击, 2: 双击），默认1
            x_offset: 相对控件左上角的X偏移（像素），默认0
            y_offset: 相对控件左上角的Y偏移（像素），默认0
        
        Returns:
            是否点击成功
        
        Example:
            | Click Element | login_button |
            | Click Element | menu_button | button=right |
            | Click Element | open_button | count=2 |
            | Click Element | btn | x_offset=10 | y_offset=10 |
        """
        control = self._get_control(control_id)
        if not control:
            raise ValueError(f"Control not found: {control_id}")
        
        result = self._control_service.click_element(control._control, button, count, 0.0)
        logger.info(f"Click element {control_id}: button={button}, count={count}, offset=({x_offset}, {y_offset}): {result}")
        return result
    
    def right_click_element(self, control_id: str, x_offset: int = 0, y_offset: int = 0) -> bool:
        """右键点击控件
        
        Args:
            control_id: 控件ID
            x_offset: 相对控件左上角的X偏移（像素），默认0
            y_offset: 相对控件左上角的Y偏移（像素），默认0
        
        Returns:
            是否点击成功
        
        Example:
            | Right Click Element | menu_item |
        """
        return self.click_element(control_id, button="right", x_offset=x_offset, y_offset=y_offset)
    
    def double_click_element(self, control_id: str, x_offset: int = 0, y_offset: int = 0) -> bool:
        """双击控件
        
        Args:
            control_id: 控件ID
            x_offset: 相对控件左上角的X偏移（像素），默认0
            y_offset: 相对控件左上角的Y偏移（像素），默认0
        
        Returns:
            是否点击成功
        
        Example:
            | Double Click Element | file_icon |
        """
        return self.click_element(control_id, count=2, x_offset=x_offset, y_offset=y_offset)
    
    def type_text(self, control_id: str, text: str, clear_first: bool = True, slow: bool = False, interval: float = 0.05) -> bool:
        """在控件中输入文本
        
        Args:
            control_id: 控件ID
            text: 要输入的文本
            clear_first: 是否先清空控件，默认True
            slow: 是否慢速输入，默认False
            interval: 慢速输入的间隔（秒），默认0.05
        
        Returns:
            是否输入成功
        
        Example:
            | Type Text | username_edit | test_user |
            | Type Text | password_edit | 123456 | clear_first=False |
            | Type Text | search_edit | hello world | slow=True | interval=0.1 |
        """
        control = self._get_control(control_id)
        if not control:
            raise ValueError(f"Control not found: {control_id}")
        
        # 使用服务层输入文本
        result = self._control_service.type_text(control._control, text, clear_first, interval if slow else 0.0)
        logger.info(f"Type text into element {control_id}: {text}, clear_first={clear_first}, slow={slow}: {result}")
        return result
    
    def clear_element_text(self, control_id: str) -> bool:
        """清空控件内容
        
        Args:
            control_id: 控件ID
        
        Returns:
            是否清空成功
        
        Example:
            | Clear Element Text | username_edit |
        """
        control = self._get_control(control_id)
        if not control:
            raise ValueError(f"Control not found: {control_id}")
        
        result = self._control_service.clear_element_text(control._control)
        logger.info(f"Clear element {control_id} text: {result}")
        return result
    
    def get_element_text(self, control_id: str) -> Optional[str]:
        """获取控件文本
        
        Args:
            control_id: 控件ID
        
        Returns:
            控件文本，如果控件不可访问则返回None
        
        Example:
            | ${text} | Get Element Text | title_label |
        """
        control = self._get_control(control_id)
        if not control:
            raise ValueError(f"Control not found: {control_id}")
        
        return control.get_text()
    
    def set_element_text(self, control_id: str, text: str) -> bool:
        """设置控件文本
        
        Args:
            control_id: 控件ID
            text: 要设置的文本
        
        Returns:
            是否设置成功
        
        Example:
            | Set Element Text | username_edit | new_user |
        """
        control = self._get_control(control_id)
        if not control:
            raise ValueError(f"Control not found: {control_id}")
        
        result = self._control_service.set_element_text(control._control, text)
        logger.info(f"Set element {control_id} text to: {text}: {result}")
        return result
    
    def select_element(self, control_id: str) -> bool:
        """选中控件（适用于复选框、单选按钮等）
        
        Args:
            control_id: 控件ID
        
        Returns:
            是否选中成功
        
        Example:
            | Select Element | checkbox_remember |
        """
        control = self._get_control(control_id)
        if not control:
            raise ValueError(f"Control not found: {control_id}")
        
        result = self._control_service.select_element(control._control)
        logger.info(f"Select element {control_id}: {result}")
        return result
    
    def deselect_element(self, control_id: str) -> bool:
        """取消选中控件（适用于复选框等）
        
        Args:
            control_id: 控件ID
        
        Returns:
            是否取消选中成功
        
        Example:
            | Deselect Element | checkbox_remember |
        """
        control = self._get_control(control_id)
        if not control:
            raise ValueError(f"Control not found: {control_id}")
        
        result = self._control_service.deselect_element(control._control)
        logger.info(f"Deselect element {control_id}: {result}")
        return result
    
    def is_element_selected(self, control_id: str) -> bool:
        """检查控件是否被选中
        
        Args:
            control_id: 控件ID
        
        Returns:
            是否被选中
        
        Example:
            | ${is_selected} | Is Element Selected | checkbox_remember |
        """
        control = self._get_control(control_id)
        if not control:
            raise ValueError(f"Control not found: {control_id}")
        
        return self._control_service.is_element_selected(control._control)
    
    def is_element_enabled(self, control_id: str) -> bool:
        """检查控件是否启用
        
        Args:
            control_id: 控件ID
        
        Returns:
            是否启用
        
        Example:
            | ${is_enabled} | Is Element Enabled | btn_login |
        """
        control = self._get_control(control_id)
        if not control:
            raise ValueError(f"Control not found: {control_id}")
        
        return self._control_service.is_element_enabled(control._control)
    
    def is_element_visible(self, control_id: str) -> bool:
        """检查控件是否可见
        
        Args:
            control_id: 控件ID
        
        Returns:
            是否可见
        
        Example:
            | ${is_visible} | Is Element Visible | loading_panel |
        """
        control = self._get_control(control_id)
        if not control:
            raise ValueError(f"Control not found: {control_id}")
        
        return self._control_service.is_element_visible(control._control)
    
    def get_element_attribute(self, control_id: str, attribute: str) -> Optional[Any]:
        """获取控件属性
        
        Args:
            control_id: 控件ID
            attribute: 属性名
        
        Returns:
            属性值，如果属性不存在则返回None
        
        Example:
            | ${value} | Get Element Attribute | btn_login | enabled |
            | ${text} | Get Element Attribute | label_title | text |
        """
        control = self._get_control(control_id)
        if not control:
            raise ValueError(f"Control not found: {control_id}")
        
        return self._control_service.get_element_attribute(control._control, attribute)
    
    def set_element_attribute(self, control_id: str, attribute: str, value: Any) -> bool:
        """设置控件属性
        
        Args:
            control_id: 控件ID
            attribute: 属性名
            value: 属性值
        
        Returns:
            是否设置成功
        
        Example:
            | Set Element Attribute | btn_login | enabled | True |
        """
        control = self._get_control(control_id)
        if not control:
            raise ValueError(f"Control not found: {control_id}")
        
        result = control.set_attribute(attribute, value)
        logger.info(f"Set element {control_id} attribute {attribute} to {value}: {result}")
        return result
    
    def hover_element(self, control_id: str, x_offset: int = 0, y_offset: int = 0, duration: float = 0) -> bool:
        """鼠标悬停在控件上
        
        Args:
            control_id: 控件ID
            x_offset: 相对控件左上角的X偏移（像素），默认0
            y_offset: 相对控件左上角的Y偏移（像素），默认0
            duration: 悬停时长（秒），默认0
        
        Returns:
            是否悬停成功
        
        Example:
            | Hover Element | menu_item | duration=1 |
        """
        control = self._get_control(control_id)
        if not control:
            raise ValueError(f"Control not found: {control_id}")
        
        result = self._control_service.hover_element(control._control)
        logger.info(f"Hover element {control_id} at offset ({x_offset}, {y_offset}) for {duration}s: {result}")
        return result
    
    def drag_element_to(self, source_control_id: str, target: Any, duration: float = 1.0) -> bool:
        """将控件拖拽到目标位置
        
        Args:
            source_control_id: 源控件ID
            target: 目标对象（控件ID或坐标 [x, y]）
            duration: 拖拽时长（秒），默认1.0
        
        Returns:
            是否拖拽成功
        
        Example:
            | Drag Element To | slider | [500, 300] | duration=0.5 |
            | Drag Element To | source_item | target_item |
        """
        source_control = self._get_control(source_control_id)
        if not source_control:
            raise ValueError(f"Source control not found: {source_control_id}")
        
        # 处理目标
        if isinstance(target, str):
            # 目标是控件ID
            target_control = self._get_control(target)
            if not target_control:
                raise ValueError(f"Target control not found: {target}")
            target_obj = target_control._control
        else:
            # 目标是坐标，暂不支持
            raise NotImplementedError("Drag to coordinates is not supported yet")
        
        result = self._control_service.drag_element_to(source_control._control, target_obj)
        logger.info(f"Drag element {source_control_id} to {target} with duration {duration}s: {result}")
        return result
