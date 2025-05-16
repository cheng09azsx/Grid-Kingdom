# /grid_kingdom/ui/components/button.py
"""
通用按钮 (Button) UI组件
"""
import pygame
from typing import Callable, Optional, Tuple

from grid_kingdom.utils.logger import logger

class Button:
    """
    一个简单的可点击按钮组件。
    """
    def __init__(self,
                 rect: pygame.Rect,
                 text: str,
                 font: pygame.font.Font,
                 on_click: Optional[Callable] = None,
                 text_color: Tuple[int, int, int] = (255, 255, 255),
                 bg_color: Tuple[int, int, int] = (100, 100, 100),
                 hover_bg_color: Optional[Tuple[int, int, int]] = (120, 120, 120),
                 disabled_bg_color: Optional[Tuple[int, int, int]] = (50, 50, 50),
                 border_color: Optional[Tuple[int, int, int]] = (150, 150, 150),
                 border_width: int = 1,
                 disabled: bool = False):
        """
        初始化按钮。

        Args:
            rect (pygame.Rect): 按钮的矩形区域和位置。
            text (str): 按钮上显示的文本。
            font (pygame.font.Font): 用于渲染文本的字体。
            on_click (Optional[Callable]): 点击按钮时调用的回调函数。
            text_color (Tuple[int, int, int]): 文本颜色。
            bg_color (Tuple[int, int, int]): 背景颜色。
            hover_bg_color (Optional[Tuple[int, int, int]]): 鼠标悬停时的背景颜色。
            disabled_bg_color (Optional[Tuple[int, int, int]]): 禁用时的背景颜色。
            border_color (Optional[Tuple[int, int, int]]): 边框颜色。
            border_width (int): 边框宽度。
            disabled (bool): 按钮是否禁用。
        """
        self.rect = rect
        self.text = text
        self.font = font
        self.on_click_callback = on_click
        self.text_color = text_color
        self.bg_color = bg_color
        self.hover_bg_color = hover_bg_color if hover_bg_color else bg_color # 如果没有悬停色，则使用背景色
        self.disabled_bg_color = disabled_bg_color if disabled_bg_color else (50,50,50) # 默认禁用色
        self.border_color = border_color
        self.border_width = border_width
        self.is_hovered: bool = False
        self.is_pressed: bool = False # 可选：用于按下时的视觉效果
        self.disabled: bool = disabled

        self._text_surface: Optional[pygame.Surface] = None
        self._text_rect: Optional[pygame.Rect] = None
        self._render_text()

    def _render_text(self) -> None:
        """预渲染文本，以提高性能。"""
        try:
            self._text_surface = self.font.render(self.text, True, self.text_color)
            self._text_rect = self._text_surface.get_rect(center=self.rect.center)
        except Exception as e:
            logger.error(f"Error rendering button text '{self.text}': {e}")
            self._text_surface = None # 确保出错时不会使用旧的surface
            self._text_rect = None

    def set_text(self, new_text: str) -> None:
        """更新按钮文本并重新渲染。"""
        if self.text != new_text:
            self.text = new_text
            self._render_text()

    def set_disabled(self, disabled_status: bool) -> None:
        """设置按钮的禁用状态。"""
        if self.disabled != disabled_status:
            self.disabled = disabled_status
            logger.debug(f"Button '{self.text}' disabled status set to {self.disabled}")

    def handle_event(self, event: pygame.event.Event) -> None:
        """处理输入事件，检查按钮是否被点击。"""
        if self.disabled:
            self.is_hovered = False
            self.is_pressed = False
            return

        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.is_hovered:
                self.is_pressed = True
                logger.debug(f"Button '{self.text}' pressed.")
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and self.is_pressed and self.is_hovered: # 确保在按钮内释放
                logger.info(f"Button '{self.text}' clicked.")
                if self.on_click_callback:
                    try:
                        self.on_click_callback()
                    except Exception as e:
                        logger.error(f"Error in button '{self.text}' on_click callback: {e}", exc_info=True)
            self.is_pressed = False # 无论如何都重置按下状态

    def draw(self, surface: pygame.Surface) -> None:
        """在指定的surface上绘制按钮。"""
        current_bg_color = self.bg_color
        if self.disabled:
            current_bg_color = self.disabled_bg_color
        elif self.is_pressed and self.is_hovered: # 按下时的视觉效果可以和悬停一样或更深
            current_bg_color = self.hover_bg_color # 或者一个更深的颜色
        elif self.is_hovered:
            current_bg_color = self.hover_bg_color
        
        pygame.draw.rect(surface, current_bg_color, self.rect)

        if self.border_color and self.border_width > 0:
            pygame.draw.rect(surface, self.border_color, self.rect, self.border_width)

        if self._text_surface and self._text_rect:
            surface.blit(self._text_surface, self._text_rect)
        elif self.text: # 如果文本surface渲染失败，尝试动态渲染一次（性能较低）
            try:
                fallback_text_surface = self.font.render(self.text, True, self.text_color)
                fallback_text_rect = fallback_text_surface.get_rect(center=self.rect.center)
                surface.blit(fallback_text_surface, fallback_text_rect)
            except Exception as e:
                logger.error(f"Fallback text rendering failed for button '{self.text}': {e}")

