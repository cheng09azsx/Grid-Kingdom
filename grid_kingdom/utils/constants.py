# file/grid_kingdom/utils/constants.py
"""
游戏全局常量定义
"""
import os

# --- 基础路径 ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # 项目根目录 Grid-Kingdom/
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
FONTS_DIR = os.path.join(ASSETS_DIR, "fonts")

# --- 字体文件 ---
# 请确保在 assets/fonts/ 目录下有这个字体文件
DEFAULT_FONT_PATH = os.path.join(FONTS_DIR, "BoutiqueBitmap9x9_1.6.ttf")
FALLBACK_FONT_NAME = "arial" # 系统备用字体 (可能无中文)

# --- 屏幕与游戏设置 ---
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60
WINDOW_TITLE = "方格王国 - 开发版" # 中文标题

# --- 颜色 ---
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_LIGHT_GREY = (220, 220, 220)
COLOR_GREY = (150, 150, 150)
COLOR_DARK_GREY = (80, 80, 80)
COLOR_VERY_DARK_GREY = (30, 30, 30)
COLOR_RED = (255, 0, 0)
COLOR_GREEN = (0, 255, 0)
COLOR_BLUE = (0, 0, 255)
COLOR_YELLOW = (255, 255, 0)

# --- UI 文本 ---
TEXT_WOOD = "木材"
TEXT_STONE = "石头"
TEXT_FOOD = "食物"
TEXT_GOLD = "金币"
TEXT_MANA = "法力"
TEXT_TURN = "回合"
TEXT_END_TURN_BUTTON = "结束回合"
TEXT_BUILD_MODE = "建筑模式"
TEXT_SELECTED = "选中"
TEXT_PLACEMENT_VALID = "可放置"
TEXT_HOVER_TILE = "悬停地块"
TEXT_MOUSE_POS = "鼠标位置"