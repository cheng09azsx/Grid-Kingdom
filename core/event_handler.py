# core/event_handler.py
"""
事件处理器，负责处理游戏中的各种事件
"""
import pygame
import logging
from utils.constants import GRID_OFFSET_X, GRID_OFFSET_Y, CELL_WIDTH, CELL_HEIGHT

logger = logging.getLogger(__name__)

class EventHandler:
    """
    事件处理器类
    """
    def __init__(self, grid_manager):
        """
        初始化事件处理器
        
        Args:
            grid_manager (GridManager): 网格管理器实例
        """
        self.grid_manager = grid_manager
    
    def handle_events(self):
        """
        处理所有游戏事件
        
        Returns:
            bool: 游戏是否应该继续运行
        """
        for event in pygame.event.get():
            # 退出游戏
            if event.type == pygame.QUIT:
                logger.info("退出游戏")
                return False
            
            # 鼠标点击事件
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # 左键单击
                if event.button == 1:
                    self._handle_left_click(event.pos)
            
            # 键盘按键事件
            elif event.type == pygame.KEYDOWN:
                # ESC键退出游戏
                if event.key == pygame.K_ESCAPE:
                    logger.info("按下ESC键，退出游戏")
                    return False
        
        return True
    
    def _handle_left_click(self, pos):
        """
        处理鼠标左键点击事件
        
        Args:
            pos (tuple): 鼠标点击位置坐标 (x, y)
        """
        # 获取鼠标点击位置对应的网格坐标
        x, y = pos
        # 调整坐标以考虑网格偏移
        adjusted_x = x - GRID_OFFSET_X
        adjusted_y = y - GRID_OFFSET_Y
        
        cell = self.grid_manager.get_cell_at_position(
            adjusted_x, adjusted_y, CELL_WIDTH, CELL_HEIGHT
        )
        
        if cell:
            row, col = cell
            self.grid_manager.select_cell(row, col)
