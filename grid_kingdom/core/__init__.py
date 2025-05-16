# file/grid_kingdom/core/__init__.py
from .engine import GameEngine
from .game_state_manager import GameStateManager, BaseState

# 可以选择性地控制哪些名称通过 from grid_kingdom.core import * 被导入
# __all__ = ["GameEngine", "GameStateManager", "BaseState"]