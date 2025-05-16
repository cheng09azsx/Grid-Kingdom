# /grid_kingdom/systems/resource_system.py
"""
资源系统 (ResourceSystem)
负责管理游戏中的所有资源类型及其数量。
"""
from typing import Dict, Union,Optional
from enum import Enum, auto

from grid_kingdom.utils.logger import logger

class ResourceType(Enum):
    """枚举类，定义所有可用的资源类型。"""
    WOOD = auto()
    STONE = auto()
    FOOD = auto()
    GOLD = auto()
    MANA = auto()
    # ... 之后可以添加更多，如 IRON, COAL, KNOWLEDGE_POINTS 等

    def __str__(self):
        return self.name.capitalize()


class ResourceSystem:
    """
    管理玩家的资源。
    """
    def __init__(self, initial_resources: Optional[Dict[ResourceType, int]] = None):
        """
        初始化资源系统。

        Args:
            initial_resources (Optional[Dict[ResourceType, int]]): 初始资源数量。
                                                                    如果为None，则所有资源从0开始。
        """
        self._resources: Dict[ResourceType, int] = {}
        self._resource_caps: Dict[ResourceType, Optional[int]] = {} # 资源上限，None表示无上限

        # 初始化所有已知的资源类型，数量为0，上限为None
        for res_type in ResourceType:
            self._resources[res_type] = 0
            self._resource_caps[res_type] = None # 默认为无上限

        if initial_resources:
            for res_type, amount in initial_resources.items():
                if isinstance(res_type, ResourceType) and isinstance(amount, int):
                    self._resources[res_type] = max(0, amount) # 确保初始资源不为负
                else:
                    logger.warning(f"Invalid initial resource entry: {res_type}, {amount}. Skipping.")
        
        logger.info(f"ResourceSystem initialized. Current resources: {self.get_all_resources_str()}")

    def get_resource_amount(self, resource_type: ResourceType) -> int:
        """获取指定资源的数量。"""
        if not isinstance(resource_type, ResourceType):
            logger.error(f"Invalid resource type requested: {resource_type}")
            return 0
        return self._resources.get(resource_type, 0)

    def get_resource_cap(self, resource_type: ResourceType) -> Optional[int]:
        """获取指定资源的上限。"""
        if not isinstance(resource_type, ResourceType):
            logger.error(f"Invalid resource type for cap request: {resource_type}")
            return None
        return self._resource_caps.get(resource_type)

    def set_resource_cap(self, resource_type: ResourceType, cap: Optional[int]) -> bool:
        """设置指定资源的上限。cap为None表示无上限。"""
        if not isinstance(resource_type, ResourceType):
            logger.error(f"Invalid resource type for setting cap: {resource_type}")
            return False
        if cap is not None and cap < 0:
            logger.warning(f"Cannot set negative cap for {resource_type}. Cap remains {self._resource_caps.get(resource_type)}")
            return False
        
        self._resource_caps[resource_type] = cap
        logger.info(f"Resource cap for {resource_type} set to {cap}.")
        # 如果当前资源量超过新上限，需要处理（例如，截断或允许暂时超过）
        # 目前简单截断
        if cap is not None and self._resources[resource_type] > cap:
            self._resources[resource_type] = cap
            logger.info(f"Resource {resource_type} truncated to new cap {cap}.")
        return True


    def add_resource(self, resource_type: ResourceType, amount: int) -> bool:
        """
        增加指定资源的数量。

        Args:
            resource_type (ResourceType): 要增加的资源类型。
            amount (int): 要增加的数量 (必须为正数)。

        Returns:
            bool: 是否成功增加 (例如，如果数量为负则失败)。
        """
        if not isinstance(resource_type, ResourceType):
            logger.error(f"Invalid resource type for addition: {resource_type}")
            return False
        if amount <= 0:
            logger.warning(f"Attempted to add non-positive amount ({amount}) of {resource_type}. No change.")
            return False

        current_amount = self._resources.get(resource_type, 0)
        cap = self._resource_caps.get(resource_type)

        new_amount = current_amount + amount
        if cap is not None and new_amount > cap:
            self._resources[resource_type] = cap
            logger.info(f"Added {cap - current_amount} of {resource_type} (reached cap {cap}). {new_amount - cap} was excess.")
        else:
            self._resources[resource_type] = new_amount
            logger.info(f"Added {amount} of {resource_type}. New total: {self._resources[resource_type]}.")
        return True

    def spend_resource(self, resource_type: ResourceType, amount: int) -> bool:
        """
        消耗指定资源的数量。

        Args:
            resource_type (ResourceType): 要消耗的资源类型。
            amount (int): 要消耗的数量 (必须为正数)。

        Returns:
            bool: 如果资源足够并成功消耗则返回True，否则返回False。
        """
        if not isinstance(resource_type, ResourceType):
            logger.error(f"Invalid resource type for spending: {resource_type}")
            return False
        if amount <= 0:
            logger.warning(f"Attempted to spend non-positive amount ({amount}) of {resource_type}. No change.")
            return False # 或者 True，取决于是否认为这是一个“成功”的无操作

        current_amount = self._resources.get(resource_type, 0)
        if current_amount >= amount:
            self._resources[resource_type] = current_amount - amount
            logger.info(f"Spent {amount} of {resource_type}. Remaining: {self._resources[resource_type]}.")
            return True
        else:
            logger.warning(f"Failed to spend {amount} of {resource_type}. Only {current_amount} available.")
            return False

    def has_enough_resources(self, costs: Dict[ResourceType, int]) -> bool:
        """
        检查是否拥有足够的资源来支付一组指定的成本。

        Args:
            costs (Dict[ResourceType, int]): 一个包含资源类型和所需数量的字典。

        Returns:
            bool: 如果所有资源都足够则返回True，否则返回False。
        """
        for resource_type, required_amount in costs.items():
            if not isinstance(resource_type, ResourceType):
                logger.error(f"Invalid resource type in costs: {resource_type}")
                return False
            if self.get_resource_amount(resource_type) < required_amount:
                return False
        return True

    def spend_multiple_resources(self, costs: Dict[ResourceType, int]) -> bool:
        """
        一次性消耗多种资源。这是一个原子操作：要么全部成功消耗，要么全部不消耗。

        Args:
            costs (Dict[ResourceType, int]): 一个包含资源类型和所需数量的字典。

        Returns:
            bool: 如果所有资源都成功消耗则返回True，否则返回False。
        """
        if not self.has_enough_resources(costs):
            logger.warning(f"Not enough resources to cover costs: {costs}. Current: {self.get_all_resources_str()}")
            return False

        for resource_type, amount_to_spend in costs.items():
            # 我们已经检查过 has_enough_resources，所以这里直接减去
            # 但为了严谨，spend_resource内部还是会做检查
            if not self.spend_resource(resource_type, amount_to_spend):
                # 理论上不应该发生，因为上面检查过了
                # 如果发生了，说明逻辑有严重问题，可能需要回滚之前的消耗 (如果不是原子性的)
                # 对于这个简单版本，我们假设如果has_enough_resources通过，则单个spend_resource也会通过
                logger.critical(f"CRITICAL: spend_multiple_resources inconsistency! Failed to spend {resource_type} after check. Costs: {costs}")
                # 此处可以添加回滚逻辑，将已扣除的资源加回去
                return False 
        logger.info(f"Successfully spent multiple resources for costs: {costs}")
        return True

    def get_all_resources_str(self) -> str:
        """返回所有资源及其数量的字符串表示，用于日志或调试。"""
        return ", ".join(f"{res_type.name}: {amount}" for res_type, amount in self._resources.items())

    def __str__(self) -> str:
        return f"ResourceSystem({self.get_all_resources_str()})"

