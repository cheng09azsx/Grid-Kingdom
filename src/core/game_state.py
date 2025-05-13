# src/core/game_state.py
"""
游戏状态 - 管理游戏当前状态和场景
该模块处理游戏状态管理，包括初始游戏状态、用户输入处理和场景渲染。
"""
import logging
import pygame
from typing import Dict, List, Tuple, Any, Optional
from pygame.locals import *

from src.utils.constants import (
    GRID_ROWS, GRID_COLS, GRID_CELL_SIZE, GRID_LINE_COLOR, 
    GRID_BG_COLOR, COLOR_WHITE, COLOR_GREEN, COLOR_RED, RESOURCE_PANEL_HEIGHT,
    WINDOW_WIDTH, WINDOW_HEIGHT
)
from src.systems.grid_system import GridSystem
from src.systems.resource_system import ResourceManager, ResourceType
from src.ui.resource_ui import ResourceUI

class GameState:
    """游戏状态基类，管理游戏的当前状态"""
    
    def __init__(self) -> None:
        """初始化游戏状态"""
        self.logger = logging.getLogger("grid_kingdom.state")
        self.logger.info("初始化游戏状态")
        
        # 初始化资源系统
        self.resource_manager = ResourceManager()
        self.resource_ui = ResourceUI(self.resource_manager)
        
        # 游戏回合
        self.turn: int = 1
        
        # 初始化网格系统 - 调整网格位置，为资源面板留出空间
        grid_y_offset = RESOURCE_PANEL_HEIGHT
        self.grid_system = GridSystem(GRID_ROWS, GRID_COLS, y_offset=grid_y_offset)
        
        # 注册网格事件回调
        self.grid_system.register_event_callback("cell_selected", self._on_cell_selected)
        self.grid_system.register_event_callback("cell_click", self._on_cell_click)
        self.grid_system.register_event_callback("cell_right_click", self._on_cell_right_click)
        
        # 测试用：添加"下一回合"按钮
        button_width, button_height = 150, 40
        grid_width = GRID_COLS * GRID_CELL_SIZE
        grid_height = GRID_ROWS * GRID_CELL_SIZE
        self.next_turn_button = pygame.Rect(
            grid_width - button_width - 20,
            grid_y_offset + grid_height + 20,
            button_width,
            button_height
        )
        
        # 测试文字显示
        self.test_messages: List[str] = [
            "方格王国测试文本",
            "Grid Kingdom Test Text",
            "这是一个中文测试"
        ]
    
    def _on_cell_selected(self, x: int, y: int, cell: Any) -> None:
        """
        单元格选中事件回调
        
        Args:
            x: 单元格x坐标
            y: 单元格y坐标
            cell: 单元格对象
        """
        self.logger.info(f"选择网格坐标: ({x}, {y})")
    
    def _on_cell_click(self, x: int, y: int, cell: Any) -> None:
        """
        单元格点击事件回调
        
        Args:
            x: 单元格x坐标
            y: 单元格y坐标
            cell: 单元格对象
        """
        self.logger.debug(f"点击网格坐标: ({x}, {y})")
        
        # 测试: 点击单元格时增加一些资源
        if not cell.is_occupied():
            # 随机增加一些资源
            self.resource_manager.add_resource(ResourceType.WOOD, 10)
            self.resource_manager.add_resource(ResourceType.STONE, 5)
            
            # 设置单元格内容为简单标记
            cell.set_content("resource_spot")
            cell.metadata["resource_type"] = ResourceType.WOOD
    
    def _on_cell_right_click(self, x: int, y: int, cell: Any) -> None:
        """
        单元格右键点击事件回调
        
        Args:
            x: 单元格x坐标
            y: 单元格y坐标
            cell: 单元格对象
        """
        self.logger.debug(f"右键点击网格坐标: ({x}, {y})")
        # 右击移除单元格内容（测试功能）
        if cell.is_occupied():
            cell.clear()
    
    def handle_event(self, event: pygame.event.Event) -> None:
        """
        处理游戏事件
        
        Args:
            event: Pygame事件对象
        """
        # 将鼠标事件传递给网格系统处理
        self.grid_system.handle_mouse_event(event)
        
        # 处理"下一回合"按钮点击
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.next_turn_button.collidepoint(event.pos):
                self._next_turn()
    
    def _next_turn(self) -> None:
        """处理下一回合逻辑"""
        self.turn += 1
        self.logger.info(f"进入回合 {self.turn}")
        
        # 资源生产逻辑：遍历网格，让有建筑的单元格产生资源
        for y in range(self.grid_system.rows):
            for x in range(self.grid_system.cols):
                cell = self.grid_system.get_cell(x, y)
                if cell and cell.is_occupied():
                    if cell.content == "resource_spot":
                        # 根据单元格元数据中的资源类型产生资源
                        resource_type = cell.metadata.get("resource_type", ResourceType.WOOD)
                        amount = 5  # 简单固定产量，后续可以根据建筑类型等因素调整
                        self.resource_manager.add_resource(resource_type, amount)
        
        # 资源消耗逻辑：每回合固定消耗一定资源
        self.resource_manager.consume_resource(ResourceType.FOOD, 2)
    
    def update(self) -> None:
        """更新游戏状态"""
        # 这里将添加更多的游戏状态更新逻辑
        pass
    
    def render(self, screen: pygame.Surface, engine: Any) -> None:
        """
        渲染游戏画面
        
        Args:
            screen: Pygame屏幕对象
            engine: 游戏引擎对象，提供字体等资源
        """
        # 绘制资源UI面板
        self.resource_ui.render(screen, engine.get_font(size=18))
        
        # 绘制网格系统
        self.grid_system.render(screen)
        
        # 获取网格系统的尺寸以确定其他UI的位置
        grid_width = GRID_COLS * GRID_CELL_SIZE
        grid_height = GRID_ROWS * GRID_CELL_SIZE
        grid_y_offset = RESOURCE_PANEL_HEIGHT
        
        # 绘制"下一回合"按钮
        pygame.draw.rect(screen, (100, 100, 180), self.next_turn_button)
        button_text = engine.get_font(size=20).render("下一回合", True, COLOR_WHITE)
        button_x = self.next_turn_button.centerx - button_text.get_width() // 2
        button_y = self.next_turn_button.centery - button_text.get_height() // 2
        screen.blit(button_text, (button_x, button_y))
        
        # 绘制回合信息
        font = engine.get_font(size=24)
        turn_text = f"回合: {self.turn}"
        turn_surface = font.render(turn_text, True, COLOR_WHITE)
        screen.blit(turn_surface, (20, grid_y_offset + grid_height + 20))
        
        # 绘制当前选中的网格坐标信息
        if self.grid_system.selected_cell:
            x, y = self.grid_system.selected_cell
            cell_info = f"选中单元格: ({x}, {y})"
            cell_surface = font.render(cell_info, True, COLOR_GREEN)
            screen.blit(cell_surface, (20, grid_y_offset + grid_height + 60))
        
        # 测试多种字体大小渲染
        test_y = grid_y_offset + grid_height + 100
        for i, message in enumerate(self.test_messages):
            size = 16 + i * 8  # 16, 24, 32
            text_surface = engine.get_font(size=size).render(message, True, COLOR_WHITE)
            screen.blit(text_surface, (20, test_y + i * 40))