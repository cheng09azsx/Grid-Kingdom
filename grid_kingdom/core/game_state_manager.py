# grid_kingdom/core/game_state_manager.py
"""
游戏状态管理器
负责管理不同的游戏状态（场景）及其切换。
"""
from typing import Optional, Dict, Type
from grid_kingdom.utils.logger import logger

class BaseState:
    """
    游戏状态的基类。
    所有具体状态（如开始菜单、游戏主场景）都应继承此类。
    """
    def __init__(self, manager: 'GameStateManager'):
        self.manager = manager
        logger.info(f"State '{self.__class__.__name__}' initialized.")

    def handle_event(self, event) -> None:
        """处理输入事件。"""
        pass

    def update(self, dt: float) -> None:
        """更新游戏逻辑，dt是自上一帧以来的时间（秒）。"""
        pass

    def render(self, surface) -> None:
        """将当前状态渲染到屏幕上。"""
        pass

    def on_enter(self, **kwargs) -> None:
        """当进入此状态时调用。kwargs可以传递参数。"""
        logger.info(f"Entering state '{self.__class__.__name__}' with args: {kwargs}")

    def on_exit(self) -> None:
        """当退出此状态时调用。"""
        logger.info(f"Exiting state '{self.__class__.__name__}'.")


class GameStateManager:
    """
    管理游戏状态的切换。
    """
    def __init__(self):
        self.states: Dict[str, BaseState] = {}
        self.active_state: Optional[BaseState] = None
        self.active_state_name: Optional[str] = None
        logger.info("GameStateManager initialized.")

    def register_state(self, name: str, state_class: Type[BaseState]) -> None:
        """
        注册一个状态类。
        在实际切换到该状态前，不会实例化。
        """
        if name in self.states:
            logger.warning(f"State '{name}' already registered. Overwriting.")
        # 这里我们存储的是状态类，而不是实例，实现懒加载
        self.states[name] = state_class # type: ignore
        logger.info(f"State class '{state_class.__name__}' registered as '{name}'.")

    def change_state(self, name: str, **kwargs) -> None:
        """
        切换到指定名称的状态。
        kwargs 将传递给新状态的 on_enter 方法。
        """
        if self.active_state:
            self.active_state.on_exit()

        if name not in self.states:
            logger.error(f"Attempted to change to unregistered state '{name}'.")
            # 可以在这里做一个容错，比如切换到一个默认的错误状态
            return

        state_class_or_instance = self.states[name]
        if isinstance(state_class_or_instance, type) and issubclass(state_class_or_instance, BaseState):
            # 如果存储的是类，则实例化它
            new_state_instance = state_class_or_instance(self)
            # 可以选择是否替换掉字典中的类为实例，或者每次都重新实例化
            # 为了简单起见，并且如果状态需要重置，每次重新实例化更好
            self.active_state = new_state_instance
        elif isinstance(state_class_or_instance, BaseState):
            # 如果之前已经实例化并存储了实例 (当前设计是不这样做的)
            self.active_state = state_class_or_instance # type: ignore
        else:
            logger.error(f"Cannot activate state '{name}'. It's not a valid state class or instance.")
            return


        self.active_state_name = name
        logger.info(f"Changed active state to '{name}'.")
        if self.active_state:
            self.active_state.on_enter(**kwargs)

    def get_active_state(self) -> Optional[BaseState]:
        return self.active_state

    def handle_event(self, event) -> None:
        if self.active_state:
            self.active_state.handle_event(event)

    def update(self, dt: float) -> None:
        if self.active_state:
            self.active_state.update(dt)

    def render(self, surface) -> None:
        if self.active_state:
            self.active_state.render(surface)
        else:
            # 如果没有活动状态，可以渲染一个默认屏幕或错误信息
            surface.fill((50, 50, 50)) # Dark grey
            font = None
            try:
                import pygame
                pygame.font.init() #确保字体模块已初始化
                font = pygame.font.SysFont("arial", 24)
                text_surface = font.render("No active state.", True, (255, 255, 255))
                text_rect = text_surface.get_rect(center=(surface.get_width() // 2, surface.get_height() // 2))
                surface.blit(text_surface, text_rect)
            except Exception as e:
                logger.error(f"Error rendering no active state message: {e}")


# --- 示例状态 (后续会移到各自的文件中) ---
class PlaceholderState(BaseState):
    """一个占位符状态，用于演示。"""
    def __init__(self, manager: GameStateManager, color: tuple = (100, 100, 200), text: str = "Placeholder State"):
        super().__init__(manager)
        self.color = color
        self.text = text
        self.font = None # Pygame 字体对象

    def on_enter(self, **kwargs) -> None:
        super().on_enter(**kwargs)
        # 可以在这里加载状态特定的资源
        # 确保pygame.font在使用前已初始化
        import pygame # 局部导入pygame
        if not pygame.font.get_init():
            pygame.font.init()
        try:
            self.font = pygame.font.SysFont("arial", 48) # 使用系统字体
        except Exception as e:
            logger.error(f"Failed to load font in PlaceholderState: {e}")
            # 可以设置一个备用方案，或者让其保持为None，并在render中处理

        # 接收来自 change_state 的参数
        if 'message' in kwargs:
            self.text = kwargs['message']
            logger.info(f"PlaceholderState received message: {self.text}")


    def handle_event(self, event) -> None:
        super().handle_event(event)
        import pygame # 局部导入pygame
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                logger.info(f"Space pressed in {self.__class__.__name__}. Triggering state change.")
                # 示例：切换到另一个状态或自身（传递不同参数）
                if self.text == "Start Screen (Press SPACE to play)":
                    self.manager.change_state("game_main", difficulty="normal")
                elif self.text == "Game Main State (Press SPACE for menu)":
                     self.manager.change_state("start_menu", message="Welcome Back to Start Screen!")
                else:
                    self.manager.change_state("start_menu", message="Returned to Start Screen!")


    def render(self, surface) -> None:
        super().render(surface)
        surface.fill(self.color)
        if self.font:
            text_surface = self.font.render(self.text, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(surface.get_width() // 2, surface.get_height() // 2))
            surface.blit(text_surface, text_rect)
        else:
            # 如果字体加载失败，可以显示一个错误或默认文本
            # (当前GameStateManager的render中有类似处理)
            pass
