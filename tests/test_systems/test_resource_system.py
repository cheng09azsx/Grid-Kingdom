# tests/test_systems/test_resource_system.py
"""
资源系统测试 - 测试资源管理器的基础功能
"""
import sys
import os

# 获取当前文件的绝对路径，并向上回溯到项目根目录
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.insert(0, project_root)

import unittest
from src.systems.resource_system import ResourceManager, ResourceType, ResourceInfo

class TestResourceSystem(unittest.TestCase):
    """测试资源系统的基本功能"""
    
    def setUp(self):
        """测试前设置"""
        self.resource_manager = ResourceManager()
    
    def test_resource_initialization(self):
        """测试资源系统初始化"""
        # 检查基础资源是否已初始化
        self.assertGreater(self.resource_manager.get_resource_amount(ResourceType.WOOD), 0)
        self.assertGreater(self.resource_manager.get_resource_amount(ResourceType.STONE), 0)
        self.assertGreater(self.resource_manager.get_resource_amount(ResourceType.FOOD), 0)
        self.assertGreater(self.resource_manager.get_resource_amount(ResourceType.GOLD), 0)
        
        # 检查非基础资源是否初始化为0
        self.assertEqual(self.resource_manager.get_resource_amount(ResourceType.ENERGY), 0)
        self.assertEqual(self.resource_manager.get_resource_amount(ResourceType.WOOD_PLANK), 0)
        
        # 检查存储上限是否设置
        for resource_type in ResourceType:
            self.assertGreater(self.resource_manager.get_resource_storage_limit(resource_type), 0)
    
    def test_resource_info(self):
        """测试资源信息获取"""
        # 检查每种资源类型是否有对应的资源信息
        for resource_type in ResourceType:
            resource_info = self.resource_manager.get_resource_info(resource_type)
            self.assertIsNotNone(resource_info)
            self.assertIsInstance(resource_info, ResourceInfo)
            self.assertEqual(resource_info.resource_type, resource_type)
            self.assertIsNotNone(resource_info.name)
            self.assertIsNotNone(resource_info.description)
    
    def test_add_resource(self):
        """测试增加资源"""
        # 记录初始资源数量
        initial_wood = self.resource_manager.get_resource_amount(ResourceType.WOOD)
        
        # 增加资源
        added_amount = 50
        actual_added, new_amount = self.resource_manager.add_resource(ResourceType.WOOD, added_amount)
        
        # 验证结果
        self.assertEqual(actual_added, added_amount)
        self.assertEqual(new_amount, initial_wood + added_amount)
        self.assertEqual(self.resource_manager.get_resource_amount(ResourceType.WOOD), initial_wood + added_amount)
    
    def test_add_resource_exceeding_limit(self):
        """测试增加超过存储上限的资源"""
        # 设置接近上限的资源数量
        wood_limit = self.resource_manager.get_resource_storage_limit(ResourceType.WOOD)
        self.resource_manager.resources[ResourceType.WOOD] = wood_limit - 10
        
        # 尝试增加超过上限的资源
        actual_added, new_amount = self.resource_manager.add_resource(ResourceType.WOOD, 50)
        
        # 验证结果
        self.assertEqual(actual_added, 10)  # 只应该增加10单位
        self.assertEqual(new_amount, wood_limit)  # 应该达到上限
    
    def test_consume_resource(self):
        """测试消耗资源"""
        # 确保有足够的资源
        self.resource_manager.resources[ResourceType.STONE] = 100
        
        # 消耗资源
        initial_stone = self.resource_manager.get_resource_amount(ResourceType.STONE)
        consume_amount = 30
        result = self.resource_manager.consume_resource(ResourceType.STONE, consume_amount)
        
        # 验证结果
        self.assertTrue(result)
        self.assertEqual(self.resource_manager.get_resource_amount(ResourceType.STONE), initial_stone - consume_amount)
    
    def test_consume_insufficient_resource(self):
        """测试消耗不足的资源"""
        # 设置资源数量
        self.resource_manager.resources[ResourceType.FOOD] = 10
        
        # 尝试消耗超过拥有量的资源
        result = self.resource_manager.consume_resource(ResourceType.FOOD, 20)
        
        # 验证结果
        self.assertFalse(result)
        self.assertEqual(self.resource_manager.get_resource_amount(ResourceType.FOOD), 10)  # 资源不应被消耗
    
    def test_can_consume(self):
        """测试是否可以消耗资源"""
        # 设置资源数量
        self.resource_manager.resources[ResourceType.GOLD] = 15
        
        # 测试足够和不足的情况
        self.assertTrue(self.resource_manager.can_consume(ResourceType.GOLD, 10))
        self.assertTrue(self.resource_manager.can_consume(ResourceType.GOLD, 15))
        self.assertFalse(self.resource_manager.can_consume(ResourceType.GOLD, 16))
    
    def test_multi_consume(self):
        """测试消耗多种资源"""
        # 设置资源数量
        self.resource_manager.resources[ResourceType.WOOD] = 50
        self.resource_manager.resources[ResourceType.STONE] = 30
        
        # 定义消耗
        consumption = {
            ResourceType.WOOD: 20,
            ResourceType.STONE: 10
        }
        
        # 消耗资源
        result = self.resource_manager.multi_consume(consumption)
        
        # 验证结果
        self.assertTrue(result)
        self.assertEqual(self.resource_manager.get_resource_amount(ResourceType.WOOD), 30)
        self.assertEqual(self.resource_manager.get_resource_amount(ResourceType.STONE), 20)
    
    def test_multi_consume_insufficient(self):
        """测试消耗不足的多种资源"""
        # 设置资源数量
        self.resource_manager.resources[ResourceType.WOOD] = 50
        self.resource_manager.resources[ResourceType.STONE] = 5
        
        # 定义消耗
        consumption = {
            ResourceType.WOOD: 20,
            ResourceType.STONE: 10
        }
        
        # 消耗资源
        result = self.resource_manager.multi_consume(consumption)
        
        # 验证结果
        self.assertFalse(result)
        # 资源不应被消耗
        self.assertEqual(self.resource_manager.get_resource_amount(ResourceType.WOOD), 50)
        self.assertEqual(self.resource_manager.get_resource_amount(ResourceType.STONE), 5)
    
    def test_increase_storage_limit(self):
        """测试增加存储上限"""
        # 记录初始存储上限
        initial_limit = self.resource_manager.get_resource_storage_limit(ResourceType.WOOD)
        
        # 增加存储上限
        increase_amount = 200
        self.resource_manager.increase_storage_limit(ResourceType.WOOD, increase_amount)
        
        # 验证结果
        self.assertEqual(self.resource_manager.get_resource_storage_limit(ResourceType.WOOD), initial_limit + increase_amount)
    
    def test_to_from_dict(self):
        """测试资源状态的序列化和反序列化"""
        # 设置一些资源数量和存储上限
        self.resource_manager.resources[ResourceType.WOOD] = 123
        self.resource_manager.resources[ResourceType.STONE] = 456
        self.resource_manager.storage_limits[ResourceType.WOOD] = 1500
        
        # 序列化
        state_dict = self.resource_manager.to_dict()
        
        # 创建新的资源管理器并反序列化
        new_manager = ResourceManager()
        new_manager.from_dict(state_dict)
        
        # 验证数据是否正确恢复
        self.assertEqual(new_manager.get_resource_amount(ResourceType.WOOD), 123)
        self.assertEqual(new_manager.get_resource_amount(ResourceType.STONE), 456)
        self.assertEqual(new_manager.get_resource_storage_limit(ResourceType.WOOD), 1500)
    
    def test_reset(self):
        """测试重置资源状态"""
        # 修改资源状态
        self.resource_manager.resources[ResourceType.WOOD] = 999
        self.resource_manager.storage_limits[ResourceType.WOOD] = 2000
        
        # 重置
        self.resource_manager.reset()
        
        # 验证是否恢复到初始状态
        self.assertNotEqual(self.resource_manager.get_resource_amount(ResourceType.WOOD), 999)
        self.assertNotEqual(self.resource_manager.get_resource_storage_limit(ResourceType.WOOD), 2000)

if __name__ == '__main__':
    unittest.main()
