 # src/systems/resource_system.py
"""
资源系统 - 管理游戏中的各类资源
该模块负责处理资源的存储、更新、获取和消耗，是游戏经济系统的基础。
"""
import os
import json
import logging
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from enum import Enum, auto

from src.utils.constants import ASSETS_DIR, RESOURCE_TYPES


class ResourceType(Enum):
    """资源类型枚举"""
    WOOD = auto()       # 木材
    STONE = auto()      # 石料
    FOOD = auto()       # 食物
    GOLD = auto()       # 金币
    ENERGY = auto()     # 能源
    WOOD_PLANK = auto() # 木板 (加工品)


@dataclass
class ResourceInfo:
    """资源信息数据类，存储资源的基本属性"""
    
    name: str                     # 资源名称
    description: str              # 资源描述
    resource_type: ResourceType   # 资源类型
    icon_path: str = ""           # 资源图标路径
    is_basic: bool = True         # 是否基础资源
    max_storage: int = 1000       # 默认最大存储量
    color_code: str = "#FFFFFF"   # 资源颜色代码
    
    def __post_init__(self):
        """初始化后处理，设置默认图标路径"""
        if not self.icon_path:
            # 如果未提供图标路径，使用默认路径
            resource_name = self.resource_type.name.lower()
            self.icon_path = f"assets/images/resources/{resource_name}.png"


class ResourceManager:
    """资源管理器类，负责管理游戏中的所有资源"""
    
    def __init__(self) -> None:
        """初始化资源管理器"""
        self.logger = logging.getLogger("grid_kingdom.resource")
        self.logger.info("初始化资源管理器")
        
        # 资源信息字典，存储所有资源类型的基本信息
        self.resource_info: Dict[ResourceType, ResourceInfo] = {}
        
        # 当前拥有的资源数量
        self.resources: Dict[ResourceType, int] = {}
        
        # 资源存储上限
        self.storage_limits: Dict[ResourceType, int] = {}
        
        # 加载资源定义
        self._load_resource_definitions()
        
        # 初始化默认资源
        self._initialize_default_resources()
        
        self.logger.info(f"资源管理器初始化完成，已加载{len(self.resource_info)}种资源")
    
    def _load_resource_definitions(self) -> None:
        """
        从数据文件加载资源定义
        如果文件不存在或加载失败，则使用内置默认定义
        """
        resource_file = os.path.join(ASSETS_DIR, "data", "resources.json")
        
        try:
            if os.path.exists(resource_file):
                with open(resource_file, "r", encoding="utf-8") as f:
                    resource_data = json.load(f)
                
                for resource_id, data in resource_data.items():
                    try:
                        resource_type = ResourceType[resource_id]
                        self.resource_info[resource_type] = ResourceInfo(
                            name=data.get("name", resource_id),
                            description=data.get("description", ""),
                            resource_type=resource_type,
                            icon_path=data.get("icon_path", ""),
                            is_basic=data.get("is_basic", True),
                            max_storage=data.get("max_storage", 1000),
                            color_code=data.get("color_code", "#FFFFFF")
                        )
                    except (KeyError, ValueError) as e:
                        self.logger.warning(f"跳过无效资源定义: {resource_id}, 错误: {e}")
                
                self.logger.info(f"从文件加载了{len(self.resource_info)}种资源定义")
            else:
                self.logger.warning(f"资源定义文件不存在: {resource_file}，将使用默认定义")
                self._create_default_definitions()
        except Exception as e:
            self.logger.error(f"加载资源定义失败: {e}", exc_info=True)
            self._create_default_definitions()
    
    def _create_default_definitions(self) -> None:
        """创建默认资源定义"""
        # 基础资源定义
        default_resources = {
            ResourceType.WOOD: ResourceInfo(
                name="木材",
                description="就是那种你连搭个狗窝都不够用的破烂木头",
                resource_type=ResourceType.WOOD,
                color_code="#8B4513"
            ),
            ResourceType.STONE: ResourceInfo(
                name="石料",
                description="比你的脑子还要硬的材料，惊讶吧？",
                resource_type=ResourceType.STONE,
                color_code="#808080"
            ),
            ResourceType.FOOD: ResourceInfo(
                name="食物",
                description="你连这个都要系统告诉你是什么？难怪你总是饿肚子",
                resource_type=ResourceType.FOOD,
                color_code="#FFD700"
            ),
            ResourceType.GOLD: ResourceInfo(
                name="金币",
                description="反正你也攒不够的东西",
                resource_type=ResourceType.GOLD,
                color_code="#DAA520"
            ),
            ResourceType.ENERGY: ResourceInfo(
                name="能源",
                description="跟你完全相反，它真的很有用",
                resource_type=ResourceType.ENERGY,
                is_basic=False,
                color_code="#00FFFF"
            ),
            ResourceType.WOOD_PLANK: ResourceInfo(
                name="木板",
                description="经过加工的木材，就像你——只是经过了也还是废物",
                resource_type=ResourceType.WOOD_PLANK,
                is_basic=False,
                color_code="#DEB887"
            )
        }
        
        self.resource_info = default_resources
        self.logger.info("已创建默认资源定义")
    
    def _initialize_default_resources(self) -> None:
        """初始化默认资源数量和存储上限"""
        # 为所有资源类型设置初始数量和存储上限
        for resource_type, info in self.resource_info.items():
            # 基础资源有初始值，非基础资源初始为0
            initial_amount = 50 if info.is_basic else 0
            
            # 特殊资源的初始值调整
            if resource_type == ResourceType.FOOD:
                initial_amount = 100
            elif resource_type == ResourceType.GOLD:
                initial_amount = 20
            
            self.resources[resource_type] = initial_amount
            self.storage_limits[resource_type] = info.max_storage
    
    def get_resource_amount(self, resource_type: ResourceType) -> int:
        """
        获取指定资源的当前数量
        
        Args:
            resource_type: 资源类型
        
        Returns:
            int: 资源数量
        """
        return self.resources.get(resource_type, 0)
    
    def get_resource_storage_limit(self, resource_type: ResourceType) -> int:
        """
        获取指定资源的存储上限
        
        Args:
            resource_type: 资源类型
        
        Returns:
            int: 资源存储上限
        """
        return self.storage_limits.get(resource_type, 0)
    
    def get_all_resources(self) -> Dict[ResourceType, int]:
        """
        获取所有资源的当前数量
        
        Returns:
            Dict[ResourceType, int]: 资源类型和数量的字典
        """
        return self.resources.copy()
    
    def get_resource_info(self, resource_type: ResourceType) -> Optional[ResourceInfo]:
        """
        获取指定资源的信息
        
        Args:
            resource_type: 资源类型
        
        Returns:
            Optional[ResourceInfo]: 资源信息，如果不存在则返回None
        """
        return self.resource_info.get(resource_type)
    
    def add_resource(self, resource_type: ResourceType, amount: int) -> Tuple[int, int]:
        """
        增加指定资源的数量，不超过存储上限
        
        Args:
            resource_type: 资源类型
            amount: 要增加的数量
        
        Returns:
            Tuple[int, int]: (实际增加的数量, 当前资源数量)
        """
        if amount <= 0:
            return (0, self.resources.get(resource_type, 0))
        
        # 如果资源类型不存在，先初始化为0
        if resource_type not in self.resources:
            self.resources[resource_type] = 0
        
        # 计算可以增加的最大数量（考虑存储上限）
        storage_limit = self.get_resource_storage_limit(resource_type)
        max_add = storage_limit - self.resources[resource_type]
        actual_add = min(amount, max_add)
        
        # 增加资源
        if actual_add > 0:
            self.resources[resource_type] += actual_add
            self.logger.debug(f"增加资源: {resource_type.name} +{actual_add} (总计: {self.resources[resource_type]})")
        
        return (actual_add, self.resources[resource_type])
    
    def consume_resource(self, resource_type: ResourceType, amount: int) -> bool:
        """
        消耗指定资源的数量
        
        Args:
            resource_type: 资源类型
            amount: 要消耗的数量
        
        Returns:
            bool: 是否成功消耗（资源足够）
        """
        if amount <= 0:
            return True
        
        current = self.resources.get(resource_type, 0)
        
        # 检查资源是否足够
        if current < amount:
            self.logger.debug(f"资源不足: {resource_type.name} 需要{amount}，当前{current}")
            return False
        
        # 消耗资源
        self.resources[resource_type] -= amount
        self.logger.debug(f"消耗资源: {resource_type.name} -{amount} (剩余: {self.resources[resource_type]})")
        return True
    
    def can_consume(self, resource_type: ResourceType, amount: int) -> bool:
        """
        检查是否可以消耗指定数量的资源
        
        Args:
            resource_type: 资源类型
            amount: 要消耗的数量
        
        Returns:
            bool: 是否可以消耗
        """
        return self.resources.get(resource_type, 0) >= amount
    
    def increase_storage_limit(self, resource_type: ResourceType, amount: int) -> None:
        """
        增加指定资源的存储上限
        
        Args:
            resource_type: 资源类型
            amount: 要增加的存储上限
        """
        if resource_type not in self.storage_limits:
            self.storage_limits[resource_type] = 0
        
        self.storage_limits[resource_type] += amount
        self.logger.debug(f"增加存储上限: {resource_type.name} +{amount} (总计: {self.storage_limits[resource_type]})")
    
    def multi_consume(self, resources: Dict[ResourceType, int]) -> bool:
        """
        消耗多种资源
        
        Args:
            resources: 资源类型和数量的字典
        
        Returns:
            bool: 是否全部成功消耗
        """
        # 先检查所有资源是否足够
        for resource_type, amount in resources.items():
            if not self.can_consume(resource_type, amount):
                return False
        
        # 消耗所有资源
        for resource_type, amount in resources.items():
            self.consume_resource(resource_type, amount)
        
        return True
    
    def to_dict(self) -> Dict[str, Any]:
        """
        将资源状态转换为字典，用于保存
        
        Returns:
            Dict[str, Any]: 资源状态字典
        """
        return {
            "resources": {r_type.name: amount for r_type, amount in self.resources.items()},
            "storage_limits": {r_type.name: limit for r_type, limit in self.storage_limits.items()}
        }
    
    def from_dict(self, data: Dict[str, Any]) -> None:
        """
        从字典加载资源状态
        
        Args:
            data: 资源状态字典
        """
        # 加载资源数量
        if "resources" in data:
            for r_name, amount in data["resources"].items():
                try:
                    r_type = ResourceType[r_name]
                    self.resources[r_type] = amount
                except KeyError:
                    self.logger.warning(f"未知资源类型: {r_name}")
        
        # 加载存储上限
        if "storage_limits" in data:
            for r_name, limit in data["storage_limits"].items():
                try:
                    r_type = ResourceType[r_name]
                    self.storage_limits[r_type] = limit
                except KeyError:
                    self.logger.warning(f"未知资源类型: {r_name}")
    
    def reset(self) -> None:
        """重置资源状态为初始值"""
        self._initialize_default_resources()
        self.logger.info("资源状态已重置为初始值")

