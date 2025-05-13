# rendering/renderer.py
"""
渲染器，负责渲染游戏画面
"""
import pygame
import logging
from utils.constants import (
    WINDOW_WIDTH, WINDOW_HEIGHT, GRID_OFFSET_X, GRID_OFFSET_Y,
    CELL_WIDTH, CELL_HEIGHT, GRID_COLOR, SELECTED_CELL_COLOR,
    BACKGROUND_COLOR
)

logger = logging.getLogger(__name__)

class Renderer:
    """
    渲染器类
    """
    def __init__(self, screen, grid_manager):
        """
        初始化渲染器
        
        Args:
            screen (pygame.Surface): 游戏屏幕
            grid_manager (GridManager): 网格管理器实例
        """
        self.screen = screen
        self.grid_manager = grid_manager
    
    def render(self):
        """
        渲染游戏画面
        """
        # 清空屏幕
        self.screen.fill(BACKGROUND_COLOR)
        
        # 渲染网格
        self._render_grid()
        
        # 渲染选中的格子
        self._render_selected_cell()
    
    def _render_grid(self):
        """
        渲染网格
        """
        rows, cols = self.grid_manager.rows, self.grid_manager.cols
        
        # 绘制水平线
        for row in range(rows + 1):
            y = GRID_OFFSET_Y + row * CELL_HEIGHT
            pygame.draw.line(
                self.screen, 
                GRID_COLOR, 
                (GRID_OFFSET_X, y), 
                (GRID_OFFSET_X + cols * CELL_WIDTH, y),
                1
            )
        
        # 绘制垂直线
        for col in range(cols + 1):
            x = GRID_OFFSET_X + col * CELL_WIDTH
            pygame.draw.line(
                self.screen, 
                GRID_COLOR, 
                (x, GRID_OFFSET_Y), 
                (x, GRID_OFFSET_Y + rows * CELL_HEIGHT),
                1
            )
    
    def _render_selected_cell(self):
        """
        渲染选中的格子
        """
        if self.grid_manager.selected_cell:
            row, col = self.grid_manager.selected_cell
            x = GRID_OFFSET_X + col * CELL_WIDTH
            y = GRID_OFFSET_Y + row * CELL_HEIGHT
            
            # 绘制选中格子的高亮边框
            pygame.draw.rect(
                self.screen,
                SELECTED_CELL_COLOR,
                (x, y, CELL_WIDTH, CELL_HEIGHT),
                3
            )