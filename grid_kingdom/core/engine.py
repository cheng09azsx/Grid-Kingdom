# grid_kingdom/core/engine.py
"""
游戏引擎核心
负责初始化Pygame，管理游戏主循环，处理全局事件，以及驱动状态管理器。
"""
import pygame
from grid_kingdom.utils.logger import logger
from grid_kingdom.core.game_state_manager import GameStateManager, PlaceholderState, GameMainState 
from grid_kingdom.utils import constants as C

# --- 游戏常量 (后续可以移到config或constants模块) ---
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60
WINDOW_TITLE = "方格王国 (Grid Kingdom) - Alpha v0.0.1"

class GameEngine:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        logger.info("Pygame initialized.")

        self.screen = pygame.display.set_mode((C.SCREEN_WIDTH, C.SCREEN_HEIGHT))
        pygame.display.set_caption(C.WINDOW_TITLE) # 使用常量中的中文标题
        logger.info(f"Display mode set to {C.SCREEN_WIDTH}x{C.SCREEN_HEIGHT}.")

        self.clock = pygame.time.Clock()
        self.running = False

        self.state_manager = GameStateManager()
        # 将自身引用传递给 state_manager，以便状态可以访问 engine 的属性 (如 screen)
        # 这是一种简单的依赖注入形式，更好的方式可能是在 change_state 时传递必要参数
        # 或者让状态直接从全局配置/引擎实例中获取所需信息
        setattr(self.state_manager, 'engine_ref', self) 

        self._register_initial_states()

        logger.info("GameEngine initialized.")

    def _register_initial_states(self) -> None:
        logger.debug("Registering initial states...")
        
        def create_start_menu_state(manager_instance):
            return PlaceholderState(manager_instance, color=(50, 50, 150), text="Start Screen (Press SPACE to play)")

        # 我们不再需要第二个 PlaceholderState，而是使用 GameMainState
        # def create_game_main_state_placeholder(manager_instance):
        #     return PlaceholderState(manager_instance, color=(50, 150, 50), text="Game Main State (Press SPACE for menu)")

        self.state_manager.register_state(
            "start_menu",
            create_start_menu_state
        )
        # 注册我们新的主游戏状态
        self.state_manager.register_state(
            "game_main",
            GameMainState #直接传递类，让GameStateManager在切换时实例化
        )
        
        logger.debug("Initial states registered. Attempting to change to 'start_menu'.")
        self.state_manager.change_state("start_menu", initial_message="Welcome to Grid Kingdom!")
        if not self.state_manager.get_active_state():
            logger.critical("CRITICAL: GameStateManager has no active state after initial change_state call!")
        else:
            logger.info(f"Initial active state set to: {self.state_manager.active_state_name}")

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
