# /grid_kingdom/ui/renderer.py
"""
渲染器模块
负责绘制游戏世界的所有可见元素，如网格、地块、建筑、UI等。
"""
import pygame
from typing import List, Tuple, Optional

from grid_kingdom.utils.logger import logger
from grid_kingdom.game_objects.tile import Tile # 导入 Tile 类

# --- 渲染常量 (可以移到更全局的配置文件或constants.py) ---
GRID_LINE_COLOR = (50, 50, 50)  # 网格线颜色 (深灰)
TILE_DEFAULT_COLOR = (100, 100, 100) # 地块默认颜色 (中灰)
TILE_HIGHLIGHT_COLOR = (255, 255, 0) # 鼠标悬停地块高亮颜色 (黄色)

class Renderer:
    """
    游戏渲染器类。
    """
    def __init__(self, screen_width: int, screen_height: int):
        self.screen_width = screen_width
        self.screen_height = screen_height
        # logger.info(f"Renderer initialized for screen size {screen_width}x{screen_height}.")
        # 未来可以有相机/视口 (viewport) 的概念，支持地图滚动
        self.camera_offset_x = 0
        self.camera_offset_y = 0

    def draw_grid(self, surface: pygame.Surface, grid_size_w: int, grid_size_h: int, tile_size: int) -> None:
        """
        在指定的surface上绘制网格线。

        Args:
            surface (pygame.Surface): 要绘制的目标Surface。
            grid_size_w (int): 网格的宽度（多少个地块）。
            grid_size_h (int): 网格的高度（多少个地块）。
            tile_size (int): 每个地块的边长（像素）。
        """
        # 绘制垂直线
        for x in range(grid_size_w + 1):
            start_pos = (x * tile_size - self.camera_offset_x, 0 - self.camera_offset_y)
            end_pos = (x * tile_size - self.camera_offset_x, grid_size_h * tile_size - self.camera_offset_y)
            pygame.draw.line(surface, GRID_LINE_COLOR, start_pos, end_pos)

        # 绘制水平线
        for y in range(grid_size_h + 1):
            start_pos = (0 - self.camera_offset_x, y * tile_size - self.camera_offset_y)
            end_pos = (grid_size_w * tile_size - self.camera_offset_x, y * tile_size - self.camera_offset_y)
            pygame.draw.line(surface, GRID_LINE_COLOR, start_pos, end_pos)

    def draw_tiles(self, surface: pygame.Surface, tiles: List[List[Tile]]) -> None:
        """
        绘制所有地块。目前只是简单填充颜色。

        Args:
            surface (pygame.Surface): 目标Surface。
            tiles (List[List[Tile]]): 二维列表，包含所有Tile对象。
        """
        if not tiles or not tiles[0]:
            return

        for row in tiles:
            for tile_obj in row:
                # 根据地块类型选择颜色 (简单示例)
                color = TILE_DEFAULT_COLOR
                if tile_obj.tile_type == "grass":
                    color = (0, 150, 0) # 绿色
                elif tile_obj.tile_type == "water":
                    color = (0, 0, 150) # 蓝色
                
                # 考虑相机偏移
                tile_rect_on_screen = tile_obj.rect.move(-self.camera_offset_x, -self.camera_offset_y)
                pygame.draw.rect(surface, color, tile_rect_on_screen)
                # 未来：在这里绘制地块的纹理而不是纯色

    def draw_highlighted_tile(self, surface: pygame.Surface, tile: Optional[Tile]) -> None:
        """如果存在高亮地块，则绘制其高亮边框。"""
        if tile:
            # 考虑相机偏移
            highlight_rect = tile.rect.move(-self.camera_offset_x, -self.camera_offset_y)
            pygame.draw.rect(surface, TILE_HIGHLIGHT_COLOR, highlight_rect, 2) # 2是边框厚度

    # 未来可以添加:
    # def draw_buildings(self, surface, buildings_list): ...
    # def draw_ui_elements(self, surface, ui_elements): ...
