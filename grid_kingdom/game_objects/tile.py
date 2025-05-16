# file/grid_kingdom/game_objects/tile.py
"""
地块 (Tile) 类定义
代表游戏世界中的一个方格单元。
"""
from typing import Tuple, Optional
import pygame # For Rect and potentially drawing individual tiles later

from grid_kingdom.utils.logger import logger

class Tile:
    """
    代表游戏地图上的一个地块。
    """
    def __init__(self, grid_x: int, grid_y: int, tile_size: int, tile_type: str = "empty"):
        """
        初始化一个地块。

        Args:
            grid_x (int): 地块在网格中的X坐标 (列)。
            grid_y (int): 地块在网格中的Y坐标 (行)。
            tile_size (int): 地块的边长（像素）。
            tile_type (str, optional): 地块的类型，默认为 "empty"。
                                      例如："grass", "water", "rock", or "occupied_by_building_id_xyz"
        """
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.tile_size = tile_size
        self.tile_type = tile_type
        self.is_occupied: bool = False # 该地块是否被建筑等占据
        self.occupying_entity_id: Optional[str] = None # 占据该地块的实体的ID

        # 计算地块在屏幕上的像素位置和矩形区域
        # 这对于渲染和碰撞检测很有用
        self.pixel_x = self.grid_x * self.tile_size
        self.pixel_y = self.grid_y * self.tile_size
        self.rect = pygame.Rect(self.pixel_x, self.pixel_y, self.tile_size, self.tile_size)

        # logger.debug(f"Tile created at ({self.grid_x}, {self.grid_y}) of type '{self.tile_type}'")

    def __repr__(self) -> str:
        return f"Tile(grid=({self.grid_x},{self.grid_y}), type='{self.tile_type}', occupied={self.is_occupied})"

    def set_type(self, new_type: str) -> None:
        """设置地块的新类型。"""
        logger.info(f"Tile ({self.grid_x},{self.grid_y}) type changed from '{self.tile_type}' to '{new_type}'.")
        self.tile_type = new_type

    def set_occupied(self, entity_id: str) -> None:
        """标记地块为被占据状态。"""
        if not self.is_occupied:
            self.is_occupied = True
            self.occupying_entity_id = entity_id
            logger.info(f"Tile ({self.grid_x},{self.grid_y}) is now occupied by '{entity_id}'.")
        else:
            logger.warning(f"Tile ({self.grid_x},{self.grid_y}) is already occupied by '{self.occupying_entity_id}', cannot be occupied by '{entity_id}'.")

    def set_vacant(self) -> None:
        """标记地块为空闲状态。"""
        if self.is_occupied:
            logger.info(f"Tile ({self.grid_x},{self.grid_y}) previously occupied by '{self.occupying_entity_id}' is now vacant.")
            self.is_occupied = False
            self.occupying_entity_id = None
        else:
            logger.debug(f"Tile ({self.grid_x},{self.grid_y}) is already vacant.")

    def draw_highlight(self, surface: pygame.Surface, color: Tuple[int, int, int], thickness: int = 2) -> None:
        """在地块边缘绘制高亮。"""
        pygame.draw.rect(surface, color, self.rect, thickness)

    # 之后可以添加更多方法，例如：
    # - get_neighbors()
    # - draw_self(surface, offset_x, offset_y) 如果每个地块有自己的纹理
