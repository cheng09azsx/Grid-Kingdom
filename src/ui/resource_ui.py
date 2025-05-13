# src/ui/resource_ui.py
"""
资源UI - 负责显示游戏资源信息的UI组件
该模块提供资源面板的绘制和更新功能。
"""
import pygame
import logging
from typing import Dict, Tuple, List, Optional, Any

from src.systems.resource_system import ResourceManager, ResourceType
from src.utils.constants import (
    WINDOW_WIDTH, RESOURCE_PANEL_HEIGHT, RESOURCE_ICON_SIZE, 
    RESOURCE_TEXT_COLOR, RESOURCE_PANEL_BG_COLOR, RESOURCE_PANEL_BORDER_COLOR,
    RESOURCE_STORAGE_WARNING_THRESHOLD, COLOR_YELLOW, COLOR_RED
)

class ResourceUI:
    """资源UI类，负责绘制资源信息面板"""
    
    def __init__(self, resource_manager: ResourceManager) -> None:
        """
        初始化资源UI
        
        Args:
            resource_manager: 资源管理器实例
        """
        self.logger = logging.getLogger("grid_kingdom.ui.resource")
        self.resource_manager = resource_manager
        
        # 资源图标缓存
        self.icon_cache: Dict[ResourceType, Optional[pygame.Surface]] = {}
        
        # 尝试加载资源图标
        self._load_resource_icons()
        
        # 记录要显示的资源类型及顺序
        self.display_resources: List[ResourceType] = [
            ResourceType.WOOD,
            ResourceType.STONE,
            ResourceType.FOOD,
            ResourceType.GOLD,
            ResourceType.ENERGY,
            ResourceType.WOOD_PLANK
        ]
        
        # 布局参数
        self.panel_height = RESOURCE_PANEL_HEIGHT
        self.padding = 10
        self.item_spacing = 20
        
        self.logger.info("资源UI初始化完成")
    
    def _load_resource_icons(self) -> None:
        """加载所有资源类型的图标"""
        for resource_type in ResourceType:
            try:
                resource_info = self.resource_manager.get_resource_info(resource_type)
                if resource_info and resource_info.icon_path:
                    icon = pygame.image.load(resource_info.icon_path)
                    icon = pygame.transform.scale(icon, (RESOURCE_ICON_SIZE, RESOURCE_ICON_SIZE))
                    self.icon_cache[resource_type] = icon
                else:
                    self.icon_cache[resource_type] = None
            except Exception as e:
                self.logger.warning(f"加载资源图标失败: {resource_type.name}, 错误: {e}")
                self.icon_cache[resource_type] = None
    
    def _get_resource_color(self, current: int, limit: int) -> Tuple[int, int, int]:
        """
        根据资源数量与上限的比例，确定资源显示颜色
        
        Args:
            current: 当前资源数量
            limit: 资源上限
        
        Returns:
            Tuple[int, int, int]: RGB颜色值
        """
        if limit <= 0:
            return RESOURCE_TEXT_COLOR
        
        ratio = current / limit
        
        if ratio >= 0.95:  # 接近上限
            return COLOR_RED
        elif ratio >= RESOURCE_STORAGE_WARNING_THRESHOLD:  # 警告阈值
            return COLOR_YELLOW
        else:
            return RESOURCE_TEXT_COLOR
    
    def render(self, screen: pygame.Surface, font: pygame.font.Font) -> None:
        """
        渲染资源UI面板
        
        Args:
            screen: Pygame屏幕对象
            font: 文本字体
        """
        # 绘制资源面板背景
        panel_rect = pygame.Rect(0, 0, WINDOW_WIDTH, self.panel_height)
        pygame.draw.rect(screen, RESOURCE_PANEL_BG_COLOR, panel_rect)
        pygame.draw.line(screen, RESOURCE_PANEL_BORDER_COLOR, 
                         (0, self.panel_height), (WINDOW_WIDTH, self.panel_height), 2)
        
        # 计算每个资源显示的水平位置
        usable_width = WINDOW_WIDTH - 2 * self.padding
        item_width = usable_width // len(self.display_resources)
        
        # 渲染各类资源信息
        for i, resource_type in enumerate(self.display_resources):
            resource_info = self.resource_manager.get_resource_info(resource_type)
            if not resource_info:
                continue
            
            current_amount = self.resource_manager.get_resource_amount(resource_type)
            storage_limit = self.resource_manager.get_resource_storage_limit(resource_type)
            
            # 计算这个资源信息的显示位置
            x_pos = self.padding + i * item_width
            y_pos = self.panel_height // 2 - RESOURCE_ICON_SIZE // 2
            
            # 渲染资源图标（如果有）
            icon = self.icon_cache.get(resource_type)
            if icon:
                screen.blit(icon, (x_pos, y_pos))
                text_x = x_pos + RESOURCE_ICON_SIZE + 5
            else:
                # 如果没有图标，用颜色块代替
                color_block = pygame.Surface((RESOURCE_ICON_SIZE, RESOURCE_ICON_SIZE))
                try:
                    color_hex = resource_info.color_code.lstrip('#')
                    color_rgb = tuple(int(color_hex[i:i+2], 16) for i in (0, 2, 4))
                    color_block.fill(color_rgb)
                except:
                    color_block.fill((200, 200, 200))  # 默认灰色
                
                screen.blit(color_block, (x_pos, y_pos))
                text_x = x_pos + RESOURCE_ICON_SIZE + 5
            
            # 渲染资源名称和数量
            resource_color = self._get_resource_color(current_amount, storage_limit)
            resource_text = f"{resource_info.name}: {current_amount}/{storage_limit}"
            text_surface = font.render(resource_text, True, resource_color)
            screen.blit(text_surface, (text_x, y_pos + RESOURCE_ICON_SIZE // 2 - text_surface.get_height() // 2))
