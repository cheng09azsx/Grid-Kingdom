# file/grid_kingdom/game_objects/building.py
"""
建筑 (Building) 类定义
代表游戏世界中可以放置在网格上的各种建筑。
"""
import pygame
from typing import Tuple, Dict, Optional, List
from uuid import uuid4 # 用于生成唯一ID

from grid_kingdom.utils.logger import logger
from grid_kingdom.systems.resource_system import ResourceType # 需要资源类型定义
from grid_kingdom.utils import constants as C

class Building:
    """
    建筑的基类。
    所有具体建筑都应继承此类。
    """
    def __init__(self, building_type: str, grid_x: int, grid_y: int, tile_size: int,
                 name: str = "未命名建筑",
                 build_cost: Optional[Dict[ResourceType, int]] = None,
                 maintenance_cost: Optional[Dict[ResourceType, int]] = None,
                 produces: Optional[Dict[ResourceType, int]] = None, # 每回合产出
                 production_interval: int = 1): # 生产间隔（回合数）
        """
        初始化一个建筑。

        Args:
            building_type (str): 建筑的唯一类型标识符 (e.g., "woodcutter_hut", "mana_well").
            grid_x (int): 建筑所占据的左上角地块在网格中的X坐标。
            grid_y (int): 建筑所占据的左上角地块在网格中的Y坐标。
            tile_size (int): 单个地块的像素大小，用于计算建筑的屏幕矩形。
            name (str, optional): 建筑的显示名称。
            build_cost (Optional[Dict[ResourceType, int]], optional): 建造所需的资源。
            maintenance_cost (Optional[Dict[ResourceType, int]], optional): 每回合维持所需的资源。
            produces (Optional[Dict[ResourceType, int]], optional): 每生产周期产出的资源。
            production_interval (int, optional): 多少个回合生产一次。默认为1（每回合）。
        """
        self.id: str = str(uuid4()) # 每个建筑实例都有一个唯一ID
        self.building_type: str = building_type
        self.name: str = name
        self.grid_x: int = grid_x
        self.grid_y: int = grid_y
        
        # 假设所有建筑都只占1x1地块 (初期简化)
        # 未来可以扩展为size_x, size_y来支持多格建筑
        self.size_tiles_x: int = 1 
        self.size_tiles_y: int = 1

        self.tile_size = tile_size # 保存tile_size用于计算rect
        self.rect = pygame.Rect(
            self.grid_x * self.tile_size,
            self.grid_y * self.tile_size,
            self.size_tiles_x * self.tile_size,
            self.size_tiles_y * self.tile_size
        )

        self.build_cost: Dict[ResourceType, int] = build_cost if build_cost else {}
        self.maintenance_cost: Dict[ResourceType, int] = maintenance_cost if maintenance_cost else {}
        self.produces: Dict[ResourceType, int] = produces if produces else {}
        self.production_interval: int = max(1, production_interval) # 至少为1
        self.turns_since_last_production: int = 0 # 追踪生产周期
        self.is_active: bool = True # 建筑是否在工作 (例如，因为缺少维护费而暂停)

        # 插件槽等概念可以在后续阶段添加
        # self.plugin_slots: List[Optional[Plugin]] = []

        logger.info(f"建筑 '{self.name}' (ID: {self.id}, 类型: {self.building_type}) 创建于网格 ({self.grid_x},{self.grid_y}).")

    def __repr__(self) -> str:
        return f"Building(id='{self.id}', type='{self.building_type}', name='{self.name}', grid=({self.grid_x},{self.grid_y}))"

    def update_production(self) -> Optional[Dict[ResourceType, int]]:
        """
        更新建筑的生产逻辑。如果建筑在本回合生产了资源，则返回产出的资源字典。
        此方法应在每回合开始时被调用。
        """
        if not self.is_active or not self.produces:
            return None

        self.turns_since_last_production += 1
        if self.turns_since_last_production >= self.production_interval:
            self.turns_since_last_production = 0 # 重置计数器
            logger.info(f"Building '{self.name}' (ID: {self.id}) produced: {self.produces}")
            return self.produces.copy() # 返回副本以防外部修改
        return None

    def pay_maintenance(self, resource_system) -> bool:
        """
        尝试支付维护费用。如果支付成功或无需支付，则保持激活状态。
        如果支付失败，则设为非激活状态。
        此方法应在每回合（通常在生产之后）被调用。
        Args:
            resource_system: ResourceSystem的实例。
        Returns:
            bool: 是否成功支付或无需支付。
        """
        if not self.maintenance_cost: # 没有维护费
            if not self.is_active: # 如果之前是暂停的，现在恢复
                self.is_active = True
                logger.info(f"Building '{self.name}' (ID: {self.id}) re-activated (no maintenance).")
            return True

        if resource_system.spend_multiple_resources(self.maintenance_cost):
            if not self.is_active: # 如果之前是暂停的，现在恢复
                self.is_active = True
                logger.info(f"Building '{self.name}' (ID: {self.id}) maintenance paid, re-activated.")
            # logger.debug(f"Building '{self.name}' (ID: {self.id}) maintenance paid.")
            return True
        else:
            if self.is_active:
                self.is_active = False
                logger.warning(f"Building '{self.name}' (ID: {self.id}) failed to pay maintenance. Deactivated.")
            return False
            
    def get_occupied_tiles(self) -> List[Tuple[int, int]]:
        """返回建筑占据的所有地块的网格坐标列表。"""
        occupied = []
        for dx in range(self.size_tiles_x):
            for dy in range(self.size_tiles_y):
                occupied.append((self.grid_x + dx, self.grid_y + dy))
        return occupied

    def draw(self, surface: pygame.Surface,
             font_for_char: Optional[pygame.font.Font], # <--- 确保这个参数存在
             camera_offset_x: int = 0,
             camera_offset_y: int = 0) -> None:
        """
        在指定的surface上绘制建筑的简单表示。
        Args:
            surface: 目标Surface。
            font_for_char (Optional[pygame.font.Font]): 用于绘制建筑标识字符的字体。
            camera_offset_x: 相机X轴偏移。
            camera_offset_y: 相机Y轴偏移。
        """
        color = C.COLOR_GREY # 默认灰色
        if self.building_type == "mana_well":
            color = C.COLOR_BLUE
        elif self.building_type == "woodcutter_hut":
            color = (139, 69, 19) # SaddleBrown
        if not self.is_active:
            color = C.COLOR_DARK_GREY
        screen_rect = self.rect.move(-camera_offset_x, -camera_offset_y)
        pygame.draw.rect(surface, color, screen_rect)
        if font_for_char: 
            try:
                text_char = self.name[0] if self.name else "?"
                char_color = C.COLOR_WHITE if self.is_active else C.COLOR_GREY
                text_surface = font_for_char.render(text_char, True, char_color)
                text_rect = text_surface.get_rect(center=screen_rect.center)
                surface.blit(text_surface, text_rect)
            except Exception as e:
                logger.error(f"Error drawing building text char for {self.name} with provided font: {e}")
        elif self.name : # 只有在有名字且没有字体时才警告，避免不必要的日志
             logger.debug(f"Font not provided for drawing char on building {self.name}, char not drawn.")


# --- 具体建筑示例 ---

class ManaWell(Building):
    """一个简单的魔法井，生产法力水晶。"""
    CHINESE_NAME = "魔法井"
    def __init__(self, grid_x: int, grid_y: int, tile_size: int):
        super().__init__(
            building_type="mana_well",
            grid_x=grid_x,
            grid_y=grid_y,
            tile_size=tile_size,
            name="魔法井",
            build_cost={ResourceType.STONE: 20, ResourceType.WOOD: 5},
            maintenance_cost={ResourceType.FOOD: 1}, # 每回合消耗1食物维持
            produces={ResourceType.MANA: 5},
            production_interval=2 # 每2回合生产一次
        )

class WoodcutterHut(Building):
    """伐木工小屋，生产木材。"""
    CHINESE_NAME = "伐木小屋"
    def __init__(self, grid_x: int, grid_y: int, tile_size: int):
        super().__init__(
            building_type="woodcutter_hut",
            grid_x=grid_x,
            grid_y=grid_y,
            tile_size=tile_size,
            name="伐木小屋",
            build_cost={ResourceType.WOOD: 15},
            maintenance_cost={}, # 无维持费用
            produces={ResourceType.WOOD: 10},
            production_interval=1 # 每回合生产
        )

# 之后可以添加建筑工厂类 (BuildingFactory) 来根据类型字符串创建建筑实例。