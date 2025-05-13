# src\utils\constants.py
"""
常量定义 - 游戏中使用的全局常量
该模块定义了游戏中使用的各种常量，包括窗口设置、颜色、网格参数等。
"""
import os
import sys
from typing import Tuple, Dict, Any

# 根目录和资源目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

# 窗口设置
WINDOW_WIDTH: int = 1280
WINDOW_HEIGHT: int = 720
FPS: int = 60
GAME_TITLE: str = "方格王国 (Grid Kingdom)"

# 字体设置
FONT_FILE = "wqy-microhei.ttc" # 内置字体文件名

if sys.platform == 'win32':
    FONT_NAME: str = "Microsoft YaHei"  # Windows默认使用微软雅黑
elif sys.platform == 'darwin':
    FONT_NAME: str = "PingFang SC"      # macOS默认使用苹方
else:
    FONT_NAME: str = "WenQuanYi Micro Hei"  # Linux默认使用文泉驿微米黑

# 颜色定义 (R, G, B)
COLOR_BLACK: Tuple[int, int, int] = (0, 0, 0)
COLOR_WHITE: Tuple[int, int, int] = (255, 255, 255)
COLOR_GRAY: Tuple[int, int, int] = (128, 128, 128)
COLOR_LIGHT_GRAY: Tuple[int, int, int] = (200, 200, 200)
COLOR_RED: Tuple[int, int, int] = (255, 0, 0)
COLOR_GREEN: Tuple[int, int, int] = (0, 255, 0)
COLOR_BLUE: Tuple[int, int, int] = (0, 0, 255)
COLOR_YELLOW: Tuple[int, int, int] = (255, 255, 0)
COLOR_CYAN: Tuple[int, int, int] = (0, 255, 255)
COLOR_MAGENTA: Tuple[int, int, int] = (255, 0, 255)
COLOR_ORANGE: Tuple[int, int, int] = (255, 165, 0)
COLOR_PURPLE: Tuple[int, int, int] = (128, 0, 128)
COLOR_BROWN: Tuple[int, int, int] = (165, 42, 42)

# 网格设置
GRID_ROWS: int = 10
GRID_COLS: int = 15
GRID_CELL_SIZE: int = 50
GRID_MARGIN: int = 5
GRID_LINE_COLOR: Tuple[int, int, int] = COLOR_GRAY
GRID_BG_COLOR: Tuple[int, int, int] = (20, 20, 20)

# 网格状态颜色
GRID_HIGHLIGHT_COLOR: Tuple[int, int, int] = (0, 255, 0)  # 高亮选中颜色
GRID_VALID_COLOR: Tuple[int, int, int] = (0, 200, 0)      # 有效放置颜色
GRID_INVALID_COLOR: Tuple[int, int, int] = (200, 0, 0)    # 无效放置颜色

# 资源类型
RESOURCE_WOOD: str = "wood"
RESOURCE_STONE: str = "stone"
RESOURCE_FOOD: str = "food"
RESOURCE_GOLD: str = "gold"

# 建筑类型
BUILDING_LUMBERMILL: str = "lumbermill"
BUILDING_QUARRY: str = "quarry"
BUILDING_FARM: str = "farm"
BUILDING_HOUSE: str = "house"

# 游戏状态
STATE_MENU: str = "menu"
STATE_GAME: str = "game"
STATE_PAUSE: str = "pause"

# 资源相关常量
RESOURCE_PANEL_HEIGHT: int = 80
RESOURCE_ICON_SIZE: int = 32
RESOURCE_TEXT_COLOR: Tuple[int, int, int] = COLOR_WHITE
RESOURCE_PANEL_BG_COLOR: Tuple[int, int, int] = (40, 40, 40)
RESOURCE_PANEL_BORDER_COLOR: Tuple[int, int, int] = COLOR_GRAY
RESOURCE_STORAGE_WARNING_THRESHOLD: float = 0.8  # 资源达到存储上限80%时显示警告

# 资源类型字符串映射（用于配置加载）
RESOURCE_TYPES: Dict[str, str] = {
    "WOOD": "木材",
    "STONE": "石料",
    "FOOD": "食物",
    "GOLD": "金币",
    "ENERGY": "能源",
    "WOOD_PLANK": "木板"
}
