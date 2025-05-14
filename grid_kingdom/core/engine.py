# grid_kingdom/core/engine.py
"""
游戏引擎核心
负责初始化Pygame，管理游戏主循环，处理全局事件，以及驱动状态管理器。
"""
import pygame
from grid_kingdom.utils.logger import logger
from grid_kingdom.core.game_state_manager import GameStateManager, PlaceholderState # 导入示例状态

# --- 游戏常量 (后续可以移到config或constants模块) ---
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60
WINDOW_TITLE = "方格王国 (Grid Kingdom) - Alpha v0.0.1"

class GameEngine:
    """
    游戏引擎类，封装了Pygame的初始化和主循环。
    """
    def __init__(self):
        pygame.init() # 初始化所有Pygame模块
        pygame.font.init() # 确保字体模块已初始化 (有时pygame.init()不够)
        logger.info("Pygame initialized.")

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(WINDOW_TITLE)
        logger.info(f"Display mode set to {SCREEN_WIDTH}x{SCREEN_HEIGHT}.")

        self.clock = pygame.time.Clock()
        self.running = False

        self.state_manager = GameStateManager()
        self._register_initial_states() # 注册初始状态

        logger.info("GameEngine initialized.")

    def _register_initial_states(self) -> None:
        """注册游戏启动时需要的状态。"""
        # 注册我们的占位符状态
        self.state_manager.register_state(
            "start_menu",
            lambda manager: PlaceholderState(manager, color=(50, 50, 150), text="Start Screen (Press SPACE to play)")
        )
        self.state_manager.register_state(
            "game_main",
            lambda manager: PlaceholderState(manager, color=(50, 150, 50), text="Game Main State (Press SPACE for menu)")
        )
        # 游戏启动时进入开始菜单
        self.state_manager.change_state("start_menu", initial_message="Welcome to Grid Kingdom!")


    def _handle_events(self) -> None:
        """处理Pygame事件队列。"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                logger.info("QUIT event received, stopping game.")
            
            # 将事件传递给当前活动状态处理
            self.state_manager.handle_event(event)

            # 示例：全局按键处理 (例如截图、调试开关等)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: # ESC键退出
                    self.running = False
                    logger.info("ESCAPE key pressed, stopping game.")


    def _update(self, dt: float) -> None:
        """更新游戏逻辑。dt是增量时间。"""
        self.state_manager.update(dt)
        # 未来可以在这里更新全局的游戏逻辑（如果独立于状态）

    def _render(self) -> None:
        """渲染游戏画面。"""
        # self.screen.fill((0, 0, 0)) # 通常由当前状态负责填充背景

        self.state_manager.render(self.screen)

        pygame.display.flip() # 更新整个屏幕显示

    def run(self) -> None:
        """启动游戏主循环。"""
        self.running = True
        logger.info("Starting game loop...")
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0 # 获取增量时间（秒）

            self._handle_events()
            self._update(dt)
            self._render()

        logger.info("Game loop finished.")
        self.quit()

    def quit(self) -> None:
        """清理并退出游戏。"""
        logger.info("Quitting Pygame...")
        pygame.quit()
        logger.info("Pygame quit successfully.")

