"""
游戏引擎 - 核心引擎，负责游戏主循环及状态管理
实现游戏的主循环、初始化pygame环境、处理用户输入和管理游戏状态。
"""
import os
import sys
import logging
import pygame
from typing import Optional, Dict, Any, List
from pygame.locals import *

from src.core.game_state import GameState
from src.utils.constants import (
    WINDOW_WIDTH, WINDOW_HEIGHT, FPS, GAME_TITLE, 
    COLOR_BLACK, COLOR_WHITE, FONT_NAME, ASSETS_DIR, FONT_FILE
)

class GameEngine:
    """游戏引擎类，负责管理游戏主循环和状态"""
    
    def __init__(self) -> None:
        """初始化游戏引擎，设置pygame环境和基础游戏状态"""
        self.logger = logging.getLogger("grid_kingdom.engine")
        self.logger.info("初始化游戏引擎")
        
        # 初始化Pygame
        pygame.init()
        
        # 初始化字体系统
        pygame.font.init()
        self._init_fonts()
        
        # 创建游戏窗口
        pygame.display.set_caption(GAME_TITLE)
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        
        # 初始化时钟
        self.clock = pygame.time.Clock()
        
        # 游戏状态与运行标志
        self.running: bool = True
        self.game_state: GameState = GameState()
        
        # 性能监控变量
        self.fps_history: List[float] = []
        self.show_fps: bool = True  # 开发模式下显示FPS
        
        # 加载基本资源
        self._load_resources()
        
        self.logger.info("游戏引擎初始化完成")
    
    def _init_fonts(self) -> None:
        """初始化字体系统"""
        self.fonts = {}
        
        # 尝试加载内置字体
        font_path = os.path.join(ASSETS_DIR, "fonts", FONT_FILE)
        if os.path.exists(font_path):
            self.logger.info(f"加载内置字体: {font_path}")
            # 预加载几种常用大小的字体
            for size in [16, 24, 36, 48]:
                if "default" not in self.fonts:
                    self.fonts["default"] = {}
                self.fonts["default"][size] = pygame.font.Font(font_path, size)
        else:
            # 如果内置字体不存在，回退到系统字体
            self.logger.warning(f"内置字体不存在: {font_path}，尝试使用系统字体")
            self._load_system_fonts()

    
    def get_font(self, name: str = None, size: int = 24) -> pygame.font.Font:
        """
        获取指定名称和大小的字体，如不存在则返回默认字体
        
        Args:
            name: 字体名称，默认为None使用配置字体
            size: 字体大小，默认24
            
        Returns:
            pygame.font.Font: 请求的字体对象
        """
        font_name = name if name else FONT_NAME
        
        # 如果请求的字体不存在，尝试加载
        if font_name not in self.fonts or size not in self.fonts[font_name]:
            try:
                if font_name not in self.fonts:
                    self.fonts[font_name] = {}
                self.fonts[font_name][size] = pygame.font.SysFont(font_name, size)
            except Exception:
                # 如果加载失败，回退到默认字体
                if "default" not in self.fonts:
                    self.fonts["default"] = {}
                if size not in self.fonts["default"]:
                    self.fonts["default"][size] = pygame.font.SysFont(None, size)
                font_name = "default"
        
        return self.fonts.get(font_name, {}).get(size, pygame.font.SysFont(None, size))
    
    def _load_resources(self) -> None:
        """加载游戏基本资源，如图像、音效等"""
        self.logger.info("加载游戏资源")
        # 这里将在后续实现资源加载，目前为占位
    
    def process_events(self) -> None:
        """处理游戏事件，如键盘和鼠标输入"""
        for event in pygame.event.get():
            # 处理退出事件
            if event.type == pygame.QUIT:
                self.running = False
                return
            
            # 处理按键事件
            if event.type == pygame.KEYDOWN:
                # ESC键退出游戏
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                    return
                # F3显示/隐藏FPS
                elif event.key == pygame.K_F3:
                    self.show_fps = not self.show_fps
                    self.logger.debug(f"FPS显示状态切换为: {self.show_fps}")
            
            # 将事件传递给当前游戏状态处理
            self.game_state.handle_event(event)
    
    def update(self) -> None:
        """更新游戏状态，包括游戏逻辑和状态转换"""
        # 更新当前游戏状态
        self.game_state.update()
        
        # 计算并记录FPS
        current_fps = self.clock.get_fps()
        self.fps_history.append(current_fps)
        # 只保留最近100帧的FPS记录
        if len(self.fps_history) > 100:
            self.fps_history.pop(0)
    
    def render(self) -> None:
        """渲染游戏画面，包括UI和游戏元素"""
        # 清空屏幕
        self.screen.fill(COLOR_BLACK)
        
        # 渲染当前游戏状态
        self.game_state.render(self.screen, self)
        
        # 显示FPS信息（开发模式）
        if self.show_fps:
            fps_avg = sum(self.fps_history) / max(1, len(self.fps_history))
            fps_text = f"FPS: {fps_avg:.1f}"
            fps_surface = self.get_font(size=16).render(fps_text, True, COLOR_WHITE)
            self.screen.blit(fps_surface, (WINDOW_WIDTH - fps_surface.get_width() - 10, 10))
        
        # 更新屏幕显示
        pygame.display.flip()
    
    def run(self) -> int:
        """
        运行游戏主循环
        
        Returns:
            int: 退出代码 (0 表示正常退出)
        """
        self.logger.info("开始游戏主循环")
        
        try:
            # 游戏主循环
            while self.running:
                self.process_events()  # 处理用户输入
                self.update()          # 更新游戏状态
                self.render()          # 渲染游戏界面
                self.clock.tick(FPS)   # 控制帧率
        
        except Exception as e:
            self.logger.error(f"游戏运行出错: {e}", exc_info=True)
            return 1
        finally:
            self.cleanup()
        
        self.logger.info("游戏正常退出")
        return 0
    
    def cleanup(self) -> None:
        """清理资源，关闭pygame环境"""
        self.logger.info("清理游戏资源")
        pygame.font.quit()
        pygame.quit()
