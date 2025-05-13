# main.py
"""
方格王国 (Grid Kingdom) 主入口
"""
import pygame
import sys
import logging
from core.grid_manager import GridManager
from core.event_handler import EventHandler
from rendering.renderer import Renderer
from utils.constants import WINDOW_WIDTH, WINDOW_HEIGHT, GRID_ROWS, GRID_COLS
from utils.logger import setup_logger

# 设置日志系统
logger = setup_logger()

class Game:
    """
    游戏主类，负责初始化和运行游戏
    """
    def __init__(self):
        """
        初始化游戏
        """
        # 初始化Pygame
        pygame.init()
        
        # 创建游戏窗口
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("方格王国 (Grid Kingdom)")
        
        # 创建时钟对象，用于控制游戏帧率
        self.clock = pygame.time.Clock()
        
        # 初始化网格管理器
        self.grid_manager = GridManager(GRID_ROWS, GRID_COLS)
        
        # 初始化事件处理器
        self.event_handler = EventHandler(self.grid_manager)
        
        # 初始化渲染器
        self.renderer = Renderer(self.screen, self.grid_manager)
        
        # 游戏运行标志
        self.running = True
        
        logger.info("游戏初始化完成")
    
    def run(self):
        """
        游戏主循环
        """
        logger.info("游戏开始运行")
        
        while self.running:
            # 处理事件
            self.running = self.event_handler.handle_events()
            
            # 更新游戏状态
            self.update()
            
            # 渲染游戏画面
            self.renderer.render()
            
            # 更新显示
            pygame.display.flip()
            
            # 控制帧率为60FPS
            self.clock.tick(60)
        
        # 退出游戏
        pygame.quit()
        sys.exit()
    
    def update(self):
        """
        更新游戏状态
        """
        pass

if __name__ == "__main__":
    game = Game()
    game.run()
