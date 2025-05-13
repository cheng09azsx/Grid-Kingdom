# core/grid_manager.py
"""
网格管理器，负责管理游戏中的网格
"""
import logging

logger = logging.getLogger(__name__)

class GridManager:
    """
    网格管理器类
    """
    def __init__(self, rows, cols):
        """
        初始化网格管理器
        
        Args:
            rows (int): 网格行数
            cols (int): 网格列数
        """
        self.rows = rows
        self.cols = cols
        # 初始化网格，用于存储每个格子的建筑
        self.grid = [[None for _ in range(cols)] for _ in range(rows)]
        # 记录当前选中的格子坐标
        self.selected_cell = None
        
        logger.info(f"网格管理器初始化完成，大小为 {rows}x{cols}")
    
    def get_cell_at_position(self, x, y, cell_width, cell_height):
        """
        根据屏幕坐标获取对应的网格坐标
        
        Args:
            x (int): 屏幕X坐标
            y (int): 屏幕Y坐标
            cell_width (int): 格子宽度
            cell_height (int): 格子高度
            
        Returns:
            tuple: (row, col) 网格坐标，如果坐标不在网格内则返回None
        """
        if x < 0 or y < 0:
            return None
        
        col = int(x // cell_width)
        row = int(y // cell_height)
        
        if row < 0 or row >= self.rows or col < 0 or col >= self.cols:
            return None
        
        return (row, col)
    
    def select_cell(self, row, col):
        """
        选中指定的格子
        
        Args:
            row (int): 行索引
            col (int): 列索引
            
        Returns:
            bool: 选中是否成功
        """
        if row < 0 or row >= self.rows or col < 0 or col >= self.cols:
            return False
        
        self.selected_cell = (row, col)
        logger.info(f"选中格子 ({row}, {col})")
        return True
