# 高DPI适配器模块
# 处理不同DPI缩放比例下的坐标和尺寸适配

from typing import Tuple, Optional
import ctypes

class DPIAdapter:
    """高DPI适配器类"""
    
    def __init__(self):
        """初始化高DPI适配器"""
        # 获取系统DPI缩放比例
        self._dpi_scale = self._get_system_dpi_scale()
    
    def _get_system_dpi_scale(self) -> float:
        """获取系统DPI缩放比例
        
        Returns:
            DPI缩放比例（如1.0, 1.25, 1.5）
        """
        try:
            # 设置进程为DPI感知
            user32 = ctypes.windll.user32
            user32.SetProcessDPIAware()
            
            # 获取系统DPI
            dpi = user32.GetDpiForSystem()
            return dpi / 96.0
        except Exception:
            # 默认返回1.0
            return 1.0
    
    def get_dpi_scale(self) -> float:
        """获取当前DPI缩放比例
        
        Returns:
            DPI缩放比例
        """
        return self._dpi_scale
    
    def adapt_coordinate(self, x: int, y: int) -> Tuple[int, int]:
        """将逻辑坐标适配到当前DPI
        
        Args:
            x: 逻辑X坐标
            y: 逻辑Y坐标
            
        Returns:
            适配后的物理坐标 (x, y)
        """
        return (int(x * self._dpi_scale), int(y * self._dpi_scale))
    
    def adapt_size(self, width: int, height: int) -> Tuple[int, int]:
        """将逻辑尺寸适配到当前DPI
        
        Args:
            width: 逻辑宽度
            height: 逻辑高度
            
        Returns:
            适配后的物理尺寸 (width, height)
        """
        return (int(width * self._dpi_scale), int(height * self._dpi_scale))
    
    def reverse_coordinate(self, x: int, y: int) -> Tuple[int, int]:
        """将物理坐标转换为逻辑坐标
        
        Args:
            x: 物理X坐标
            y: 物理Y坐标
            
        Returns:
            转换后的逻辑坐标 (x, y)
        """
        return (int(x / self._dpi_scale), int(y / self._dpi_scale))
    
    def reverse_size(self, width: int, height: int) -> Tuple[int, int]:
        """将物理尺寸转换为逻辑尺寸
        
        Args:
            width: 物理宽度
            height: 物理高度
            
        Returns:
            转换后的逻辑尺寸 (width, height)
        """
        return (int(width / self._dpi_scale), int(height / self._dpi_scale))
    
    def adapt_rect(self, rect: Tuple[int, int, int, int]) -> Tuple[int, int, int, int]:
        """适配矩形区域（x, y, width, height）
        
        Args:
            rect: 逻辑矩形 (x, y, width, height)
            
        Returns:
            适配后的物理矩形 (x, y, width, height)
        """
        x, y, width, height = rect
        adapted_x, adapted_y = self.adapt_coordinate(x, y)
        adapted_width, adapted_height = self.adapt_size(width, height)
        return (adapted_x, adapted_y, adapted_width, adapted_height)
    
    def reverse_rect(self, rect: Tuple[int, int, int, int]) -> Tuple[int, int, int, int]:
        """将物理矩形转换为逻辑矩形
        
        Args:
            rect: 物理矩形 (x, y, width, height)
            
        Returns:
            转换后的逻辑矩形 (x, y, width, height)
        """
        x, y, width, height = rect
        reversed_x, reversed_y = self.reverse_coordinate(x, y)
        reversed_width, reversed_height = self.reverse_size(width, height)
        return (reversed_x, reversed_y, reversed_width, reversed_height)
    
    def is_high_dpi(self) -> bool:
        """检查当前是否为高DPI显示
        
        Returns:
            是否为高DPI显示（DPI缩放比例 > 1.0）
        """
        return self._dpi_scale > 1.0
    
    def get_dpi_level(self) -> str:
        """获取DPI级别
        
        Returns:
            DPI级别字符串
        """
        if self._dpi_scale == 1.0:
            return "100%"
        elif self._dpi_scale == 1.25:
            return "125%"
        elif self._dpi_scale == 1.5:
            return "150%"
        elif self._dpi_scale == 1.75:
            return "175%"
        elif self._dpi_scale == 2.0:
            return "200%"
        else:
            return f"{int(self._dpi_scale * 100)}%"

# 创建高DPI适配器实例
dpi_adapter = DPIAdapter()
