# /grid_kingdom/systems/turn_system.py
"""
回合系统 (TurnSystem)
负责管理游戏的回合数以及回合结束时的结算逻辑。
"""
from typing import Callable, List
from grid_kingdom.utils.logger import logger
from grid_kingdom.systems.resource_system import ResourceSystem, ResourceType # 需要资源系统进行全局消耗

class TurnSystem:
    """
    管理游戏的回合。
    """
    def __init__(self, resource_system: ResourceSystem, initial_turn: int = 1):
        """
        初始化回合系统。

        Args:
            resource_system (ResourceSystem): 游戏资源系统的实例，用于全局消耗。
            initial_turn (int): 初始回合数。
        """
        self.current_turn: int = max(1, initial_turn)
        self.resource_system = resource_system # 持有资源系统的引用

        # 回调列表，用于在回合结束时执行特定动作（如建筑生产、事件触发等）
        # 每个回调函数应该不接受参数或接受 TurnSystem 实例作为参数
        self._on_turn_end_callbacks: List[Callable] = []
        self._on_new_turn_start_callbacks: List[Callable] = [] # 新增：回合开始时的回调

        logger.info(f"TurnSystem initialized. Current turn: {self.current_turn}.")

    def register_on_turn_end_callback(self, callback: Callable) -> None:
        """注册一个在回合结束时调用的回调函数。"""
        if callback not in self._on_turn_end_callbacks:
            self._on_turn_end_callbacks.append(callback)
            logger.debug(f"Callback {callback.__name__ if hasattr(callback, '__name__') else str(callback)} registered for turn end.")

    def unregister_on_turn_end_callback(self, callback: Callable) -> None:
        """取消注册回合结束回调。"""
        if callback in self._on_turn_end_callbacks:
            self._on_turn_end_callbacks.remove(callback)
            logger.debug(f"Callback {callback.__name__ if hasattr(callback, '__name__') else str(callback)} unregistered from turn end.")

    def register_on_new_turn_start_callback(self, callback: Callable) -> None:
        """注册一个在新回合开始时调用的回调函数。"""
        if callback not in self._on_new_turn_start_callbacks:
            self._on_new_turn_start_callbacks.append(callback)
            logger.debug(f"Callback {callback.__name__ if hasattr(callback, '__name__') else str(callback)} registered for new turn start.")
            
    def unregister_on_new_turn_start_callback(self, callback: Callable) -> None:
        """取消注册新回合开始回调。"""
        if callback in self._on_new_turn_start_callbacks:
            self._on_new_turn_start_callbacks.remove(callback)
            logger.debug(f"Callback {callback.__name__ if hasattr(callback, '__name__') else str(callback)} unregistered from new turn start.")


    def _execute_callbacks(self, callback_list: List[Callable]) -> None:
        """执行指定列表中的所有回调函数。"""
        for callback in callback_list:
            try:
                # 考虑回调函数可能需要 TurnSystem 或 ResourceSystem 实例
                # 或者干脆不传参数，让回调函数自己从全局或其所属对象获取所需数据
                callback() 
            except Exception as e:
                logger.error(f"Error executing callback {callback.__name__ if hasattr(callback, '__name__') else str(callback)}: {e}", exc_info=True)

    def _process_global_turn_effects(self) -> None:
        """处理全局的回合效果，例如全局资源消耗。"""
        logger.info(f"Processing global effects for end of turn {self.current_turn}.")
        
        # 示例：每回合固定消耗1单位的食物 (如果食物资源存在)
        cost_per_turn = {ResourceType.FOOD: 1} 
        # 你也可以让这个消耗值是动态的，比如基于王国人口等
        
        if self.resource_system.spend_multiple_resources(cost_per_turn):
            logger.info(f"Global upkeep paid for turn {self.current_turn}: {cost_per_turn}")
        else:
            logger.warning(f"Failed to pay global upkeep for turn {self.current_turn}. Cost: {cost_per_turn}. Resources might be critically low.")
            # 这里可以触发一些负面事件或状态，比如饥饿、士气下降等

    def advance_turn(self) -> None:
        """
        推进到下一回合。
        这将触发回合结束回调、全局回合效果，然后增加回合数并触发新回合开始回调。
        """
        logger.info(f"--- Advancing from Turn {self.current_turn} ---")

        # 1. 执行回合结束时的回调 (例如建筑生产、维护费支付 - 这些逻辑现在在GameMainState._process_next_turn_logic)
        #    我们应该将 GameMainState._process_next_turn_logic 注册到这里
        logger.debug("Executing on_turn_end_callbacks...")
        self._execute_callbacks(self._on_turn_end_callbacks)

        # 2. 处理全局回合效果 (例如，全局资源消耗)
        self._process_global_turn_effects()

        # 3. 增加回合数
        self.current_turn += 1
        logger.info(f"--- New Turn Started: {self.current_turn} ---")

        # 4. 执行新回合开始时的回调 (例如，刷新手牌、触发新事件)
        logger.debug("Executing on_new_turn_start_callbacks...")
        self._execute_callbacks(self._on_new_turn_start_callbacks)
        
        logger.info(f"Advanced to turn {self.current_turn}. Current resources: {self.resource_system.get_all_resources_str()}")

