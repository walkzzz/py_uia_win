# 智能等待策略模块
# 提供多种等待策略，如等待控件存在、可交互、属性变化等

from typing import Callable, Any, Optional
import time

class WaitStrategy:
    """智能等待策略类"""
    
    @staticmethod
    def wait_for_exists(condition_func: Callable[[], bool], timeout: float = 10.0, interval: float = 0.5) -> bool:
        """等待条件函数返回True，表示元素存在
        
        Args:
            condition_func: 条件函数，返回True表示条件满足
            timeout: 超时时间（秒）
            interval: 检查间隔（秒）
        
        Returns:
            条件是否在超时内满足
        """
        return WaitStrategy._wait_until(condition_func, timeout, interval)
    
    @staticmethod
    def wait_for_enabled(condition_func: Callable[[], bool], timeout: float = 10.0, interval: float = 0.5) -> bool:
        """等待条件函数返回True，表示元素可交互
        
        Args:
            condition_func: 条件函数，返回True表示条件满足
            timeout: 超时时间（秒）
            interval: 检查间隔（秒）
        
        Returns:
            条件是否在超时内满足
        """
        return WaitStrategy._wait_until(condition_func, timeout, interval)
    
    @staticmethod
    def wait_for_visible(condition_func: Callable[[], bool], timeout: float = 10.0, interval: float = 0.5) -> bool:
        """等待条件函数返回True，表示元素可见
        
        Args:
            condition_func: 条件函数，返回True表示条件满足
            timeout: 超时时间（秒）
            interval: 检查间隔（秒）
        
        Returns:
            条件是否在超时内满足
        """
        return WaitStrategy._wait_until(condition_func, timeout, interval)
    
    @staticmethod
    def wait_for_text_change(condition_func: Callable[[], str], expected_text: str, timeout: float = 10.0, interval: float = 0.5) -> bool:
        """等待文本变化为预期值
        
        Args:
            condition_func: 条件函数，返回当前文本
            expected_text: 预期文本
            timeout: 超时时间（秒）
            interval: 检查间隔（秒）
        
        Returns:
            文本是否在超时内变为预期值
        """
        def text_condition():
            try:
                return condition_func() == expected_text
            except Exception:
                return False
        
        return WaitStrategy._wait_until(text_condition, timeout, interval)
    
    @staticmethod
    def wait_for_text_contains(condition_func: Callable[[], str], expected_substring: str, timeout: float = 10.0, interval: float = 0.5) -> bool:
        """等待文本包含预期子串
        
        Args:
            condition_func: 条件函数，返回当前文本
            expected_substring: 预期子串
            timeout: 超时时间（秒）
            interval: 检查间隔（秒）
        
        Returns:
            文本是否在超时内包含预期子串
        """
        def text_condition():
            try:
                text = condition_func()
                return expected_substring in text
            except Exception:
                return False
        
        return WaitStrategy._wait_until(text_condition, timeout, interval)
    
    @staticmethod
    def wait_for_attribute_change(condition_func: Callable[[], Any], expected_value: Any, timeout: float = 10.0, interval: float = 0.5) -> bool:
        """等待属性变化为预期值
        
        Args:
            condition_func: 条件函数，返回当前属性值
            expected_value: 预期属性值
            timeout: 超时时间（秒）
            interval: 检查间隔（秒）
        
        Returns:
            属性值是否在超时内变为预期值
        """
        def attribute_condition():
            try:
                return condition_func() == expected_value
            except Exception:
                return False
        
        return WaitStrategy._wait_until(attribute_condition, timeout, interval)
    
    @staticmethod
    def wait_for_disappearance(condition_func: Callable[[], bool], timeout: float = 10.0, interval: float = 0.5) -> bool:
        """等待元素消失
        
        Args:
            condition_func: 条件函数，返回True表示元素存在
            timeout: 超时时间（秒）
            interval: 检查间隔（秒）
        
        Returns:
            元素是否在超时内消失
        """
        def disappearance_condition():
            try:
                return not condition_func()
            except Exception:
                return True
        
        return WaitStrategy._wait_until(disappearance_condition, timeout, interval)
    
    @staticmethod
    def wait_for_element_count(condition_func: Callable[[], int], expected_count: int, timeout: float = 10.0, interval: float = 0.5) -> bool:
        """等待元素数量达到预期值
        
        Args:
            condition_func: 条件函数，返回当前元素数量
            expected_count: 预期元素数量
            timeout: 超时时间（秒）
            interval: 检查间隔（秒）
        
        Returns:
            元素数量是否在超时内达到预期值
        """
        def count_condition():
            try:
                return condition_func() == expected_count
            except Exception:
                return False
        
        return WaitStrategy._wait_until(count_condition, timeout, interval)
    
    @staticmethod
    def _wait_until(condition_func: Callable[[], bool], timeout: float, interval: float) -> bool:
        """等待直到条件满足或超时
        
        Args:
            condition_func: 条件函数，返回True表示条件满足
            timeout: 超时时间（秒）
            interval: 检查间隔（秒）
        
        Returns:
            条件是否在超时内满足
        """
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            try:
                if condition_func():
                    return True
            except Exception:
                # 忽略异常，继续等待
                pass
            time.sleep(interval)
        
        return False
    
    @staticmethod
    def wait_until(condition_func: Callable[[], bool], timeout: float = 30.0, error_message: str = "条件未满足") -> bool:
        """等待直到条件满足或超时
        
        Args:
            condition_func: 条件函数，返回True表示条件满足
            timeout: 超时时间（秒）
            error_message: 超时错误信息
        
        Returns:
            条件是否在超时内满足
        """
        result = WaitStrategy._wait_until(condition_func, timeout, 0.5)
        if not result:
            from ..utils.logger import logger
            logger.error(error_message)
        return result
    
    @staticmethod
    def wait(seconds: float) -> None:
        """等待指定时长
        
        Args:
            seconds: 等待时长（秒）
        """
        time.sleep(seconds)
    
    @staticmethod
    def smart_wait(target: Any, strategy: str, timeout: float = 10.0, interval: float = 0.5, **kwargs: Any) -> bool:
        """智能等待，根据策略等待目标满足条件
        
        Args:
            target: 目标对象
            strategy: 等待策略
            timeout: 超时时间（秒）
            interval: 检查间隔（秒）
            **kwargs: 策略相关参数
        
        Returns:
            目标是否在超时内满足条件
        
        Supported strategies:
            - exists: 等待对象存在
            - enabled: 等待对象可交互
            - visible: 等待对象可见
            - text_change: 等待文本变化
            - text_contains: 等待文本包含指定内容
            - attribute_change: 等待属性变化
            - disappearance: 等待对象消失
            - element_count: 等待元素数量达到预期
        """
        # 根据策略选择等待方法
        if strategy == "exists":
            return WaitStrategy.wait_for_exists(lambda: target is not None, timeout, interval)
        elif strategy == "enabled":
            return WaitStrategy.wait_for_enabled(lambda: target.is_enabled(), timeout, interval)
        elif strategy == "visible":
            return WaitStrategy.wait_for_visible(lambda: target.is_visible(), timeout, interval)
        elif strategy == "text_change":
            expected_text = kwargs.get("expected_text", "")
            return WaitStrategy.wait_for_text_change(lambda: target.get_text(), expected_text, timeout, interval)
        elif strategy == "text_contains":
            expected_substring = kwargs.get("expected_substring", "")
            return WaitStrategy.wait_for_text_contains(lambda: target.get_text(), expected_substring, timeout, interval)
        elif strategy == "attribute_change":
            attribute_name = kwargs.get("attribute_name", "")
            expected_value = kwargs.get("expected_value", "")
            return WaitStrategy.wait_for_attribute_change(lambda: target.get_attribute(attribute_name), expected_value, timeout, interval)
        elif strategy == "disappearance":
            return WaitStrategy.wait_for_disappearance(lambda: target.is_visible(), timeout, interval)
        elif strategy == "element_count":
            expected_count = kwargs.get("expected_count", 0)
            return WaitStrategy.wait_for_element_count(lambda: len(target), expected_count, timeout, interval)
        
        raise ValueError(f"Unknown wait strategy: {strategy}")

# 创建智能等待策略实例
wait_strategy = WaitStrategy()
