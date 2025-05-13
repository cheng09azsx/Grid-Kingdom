# src/systems/grid_system.py
"""
网格系统 - 负责管理游戏的网格数据结构和交互
该模块实现网格的数据存储、状态管理和交互功能，是游戏地图的基础。
"""
import logging
from typing import Dict, List, Tuple, Any, Optional, Callable
import pygame

from src.utils.constants import (
    GRID_ROWS, GRID_COLS, GRID_CELL_SIZE, GRID_LINE_COLOR, 
    GRID_BG_COLOR, COLOR_WHITE, COLOR_GREEN, COLOR_RED, COLOR_GRAY,
    GRID_HIGHLIGHT_COLOR, GRID_INVALID_COLOR, GRID_VALID_COLOR
)

class GridCell:
    """网格单元格类，表示网格中的一个单元格及其状态"""
    
    def __init__(self, x: int, y: int) -> None:
        """
        初始化一个网格单元格
        
        Args:
            x: 单元格的横坐标
            y: 单元格的纵坐标
        """
        self.x: int = x
        self.y: int = y
        self.content: Optional[Any] = None  # 格子内容(通常是建筑物)
        self.state: str = "default"         # 格子状态: default, hover, selected, invalid, valid
        self.resource_bonus: Dict[str, float] = {}  # 资源加成
        self.metadata: Dict[str, Any] = {}  # 额外元数据
    
    def is_occupied(self) -> bool:
        """检查单元格是否被占用"""
        return self.content is not None
    
    def set_content(self, content: Any) -> None:
        """
        设置单元格内容
        
        Args:
            content: 要放置在单元格中的内容
        """
        self.content = content
    
    def clear(self) -> None:
        """清空单元格内容"""
        self.content = None
    
    def set_state(self, state: str) -> None:
        """
        设置单元格状态
        
        Args:
            state: 单元格的新状态
        """
        self.state = state
    
    def __repr__(self) -> str:
        """返回单元格的字符串表示"""
        return f"GridCell({self.x}, {self.y}, content={self.content}, state={self.state})"

class GridSystem:
    """网格系统类，管理整个游戏网格"""
    
    def __init__(self, rows: int = GRID_ROWS, cols: int = GRID_COLS, y_offset: int = 0) -> None:
        """
        初始化网格系统

        Args:
            rows: 网格行数
            cols: 网格列数
            y_offset: 网格Y轴偏移量
        """
        self.logger = logging.getLogger("grid_kingdom.grid")
        self.logger.info(f"初始化网格系统: {rows}行 x {cols}列")

        self.rows: int = rows
        self.cols: int = cols
        self.cell_size: int = GRID_CELL_SIZE
        self.y_offset: int = y_offset  # 添加Y轴偏移

        # 创建网格数据结构
        self.grid: List[List[GridCell]] = [
            [GridCell(x, y) for x in range(cols)]
            for y in range(rows)
        ]

        # 当前选中和悬停的单元格
        self.selected_cell: Optional[Tuple[int, int]] = None
        self.hovered_cell: Optional[Tuple[int, int]] = None

        # 事件回调字典
        self.event_callbacks: Dict[str, List[Callable]] = {
            "cell_selected": [],
            "cell_hover": [],
            "cell_click": [],
            "cell_right_click": [],
        }

    
    def is_valid_position(self, x: int, y: int) -> bool:
        """
        检查位置是否在网格范围内
        
        Args:
            x: 横坐标
            y: 纵坐标
        
        Returns:
            bool: 如果位置在网格范围内，则为True
        """
        return 0 <= x < self.cols and 0 <= y < self.rows
    
    def get_cell(self, x: int, y: int) -> Optional[GridCell]:
        """
        获取指定位置的单元格
        
        Args:
            x: 横坐标
            y: 纵坐标
        
        Returns:
            Optional[GridCell]: 单元格对象，如果坐标无效则为None
        """
        if not self.is_valid_position(x, y):
            return None
        return self.grid[y][x]
    
    def set_cell_content(self, x: int, y: int, content: Any) -> bool:
        """
        设置指定位置单元格的内容
        
        Args:
            x: 横坐标
            y: 纵坐标
            content: 要设置的内容
        
        Returns:
            bool: 设置是否成功
        """
        cell = self.get_cell(x, y)
        if not cell:
            return False
        
        cell.set_content(content)
        self.logger.debug(f"单元格({x}, {y})设置内容: {content}")
        return True
    
    def clear_cell(self, x: int, y: int) -> bool:
        """
        清空指定位置单元格的内容
        
        Args:
            x: 横坐标
            y: 纵坐标
        
        Returns:
            bool: 清除是否成功
        """
        cell = self.get_cell(x, y)
        if not cell:
            return False
        
        cell.clear()
        self.logger.debug(f"单元格({x}, {y})内容已清空")
        return True
    
    def select_cell(self, x: int, y: int) -> None:
        """
        选择指定位置的单元格
        
        Args:
            x: 横坐标
            y: 纵坐标
        """
        # 清除之前选中单元格的状态
        if self.selected_cell:
            old_x, old_y = self.selected_cell
            old_cell = self.get_cell(old_x, old_y)
            if old_cell:
                old_cell.set_state("default")
        
        # 设置新选中的单元格
        if self.is_valid_position(x, y):
            self.selected_cell = (x, y)
            cell = self.get_cell(x, y)
            if cell:
                cell.set_state("selected")
                self.logger.debug(f"选择单元格: ({x}, {y})")
                
                # 触发选中事件回调
                for callback in self.event_callbacks.get("cell_selected", []):
                    callback(x, y, cell)
        else:
            self.selected_cell = None
    
    def deselect_cell(self) -> None:
        """取消选中当前单元格"""
        if self.selected_cell:
            x, y = self.selected_cell
            cell = self.get_cell(x, y)
            if cell:
                cell.set_state("default")
            self.selected_cell = None
            self.logger.debug("取消选中单元格")
    
    def handle_mouse_event(self, event: pygame.event.Event) -> None:
        """
        处理鼠标事件（移动、点击）
        
        Args:
            event: Pygame事件对象
        """
        # 处理鼠标移动
        if event.type == pygame.MOUSEMOTION:
            mouse_pos = pygame.mouse.get_pos()
            grid_x = mouse_pos[0] // self.cell_size
            grid_y = (mouse_pos[1] - self.y_offset) // self.cell_size
 
            # 确保在有效范围内
            if not self.is_valid_position(grid_x, grid_y):
                # 如果鼠标不在网格区域上，清除悬停
                if self.hovered_cell:
                    old_x, old_y = self.hovered_cell
                    old_cell = self.get_cell(old_x, old_y)
                    if old_cell and old_cell.state == "hover":
                        old_cell.set_state("default")
                    self.hovered_cell = None
                return

            # 更新悬停单元格
            if self.is_valid_position(grid_x, grid_y):
                # 如果不是之前悬停的单元格
                if self.hovered_cell != (grid_x, grid_y):
                    # 重置旧悬停单元格
                    if self.hovered_cell:
                        old_x, old_y = self.hovered_cell
                        old_cell = self.get_cell(old_x, old_y)
                        if old_cell and old_cell.state == "hover":
                            old_cell.set_state("default")
                    
                    # 设置新悬停单元格
                    self.hovered_cell = (grid_x, grid_y)
                    cell = self.get_cell(grid_x, grid_y)
                    if cell and cell.state != "selected":
                        cell.set_state("hover")
                    
                    # 触发悬停事件回调
                    for callback in self.event_callbacks.get("cell_hover", []):
                        callback(grid_x, grid_y, cell)
        
        # 处理鼠标点击
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            grid_x = mouse_pos[0] // self.cell_size
            grid_y = (mouse_pos[1] - self.y_offset) // self.cell_size
            
            if self.is_valid_position(grid_x, grid_y):
                cell = self.get_cell(grid_x, grid_y)
                
                # 左键点击
                if event.button == 1:
                    self.select_cell(grid_x, grid_y)
                    # 触发点击事件回调
                    for callback in self.event_callbacks.get("cell_click", []):
                        callback(grid_x, grid_y, cell)
                
                # 右键点击
                elif event.button == 3:
                    # 触发右键点击事件回调
                    for callback in self.event_callbacks.get("cell_right_click", []):
                        callback(grid_x, grid_y, cell)
        
    
    def register_event_callback(self, event_type: str, callback: Callable) -> None:
        """
        注册事件回调函数
        
        Args:
            event_type: 事件类型
            callback: 回调函数
        """
        if event_type in self.event_callbacks:
            self.event_callbacks[event_type].append(callback)
        else:
            self.logger.warning(f"尝试注册未知事件类型回调: {event_type}")
    
    def render(self, screen: pygame.Surface) -> None:
        """
        渲染网格系统
        
        Args:
            screen: Pygame屏幕对象
        """
        # 绘制网格背景
        grid_width = self.cols * self.cell_size
        grid_height = self.rows * self.cell_size
        pygame.draw.rect(screen, GRID_BG_COLOR, (0, self.y_offset, grid_width, grid_height))
        
        # 绘制单元格内容和状态
        for y in range(self.rows):
            for x in range(self.cols):
                cell = self.grid[y][x]
                cell_rect = pygame.Rect(
                    x * self.cell_size,
                    y * self.cell_size + self.y_offset,  # 考虑Y轴偏移
                    self.cell_size,
                    self.cell_size
                )
                
                # 根据单元格状态绘制不同的效果
                if cell.state == "selected":
                    pygame.draw.rect(screen, GRID_HIGHLIGHT_COLOR, cell_rect, 3)
                elif cell.state == "hover":
                    pygame.draw.rect(screen, COLOR_GRAY, cell_rect, 2)
                elif cell.state == "valid":
                    pygame.draw.rect(screen, GRID_VALID_COLOR, cell_rect, 2)
                elif cell.state == "invalid":
                    pygame.draw.rect(screen, GRID_INVALID_COLOR, cell_rect, 2)
                
                # 如果单元格有内容，绘制内容
                if cell.content:
                    # 这里将来会调用内容对象的渲染方法
                    # 暂时用一个简单的表示方式
                    center_x = cell_rect.centerx
                    center_y = cell_rect.centery
                    pygame.draw.circle(screen, COLOR_WHITE, (center_x, center_y), self.cell_size // 3)
        
        # 绘制网格线
        for y in range(self.rows + 1):
            pygame.draw.line(
                screen,
                GRID_LINE_COLOR,
                (0, y * self.cell_size + self.y_offset),  # 考虑Y轴偏移
                (grid_width, y * self.cell_size + self.y_offset)  # 考虑Y轴偏移
            )
        
        for x in range(self.cols + 1):
            pygame.draw.line(
                screen,
                GRID_LINE_COLOR,
                (x * self.cell_size, self.y_offset),  # 考虑Y轴偏移
                (x * self.cell_size, grid_height + self.y_offset)  # 考虑Y轴偏移
            )
