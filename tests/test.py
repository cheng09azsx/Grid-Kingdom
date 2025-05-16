import pygame
import os
pygame.init()
pygame.font.init()
# --- 假设这是你的常量定义 ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) # 假设这个测试脚本在项目根目录的tests文件夹
ASSETS_DIR = os.path.join(os.path.dirname(BASE_DIR), "assets") # 退回到项目根目录再进入assets
FONTS_DIR = os.path.join(ASSETS_DIR, "fonts")
# !! 修改为你实际的字体文件名 !!
# FONT_NAME = "SimHei.ttf" 
FONT_NAME = "BoutiqueBitmap9x9_1.6.ttf" # 例如 msyh.ttf
DEFAULT_FONT_PATH_TEST = os.path.join(FONTS_DIR, FONT_NAME)
print(f"Attempting to load font from: {DEFAULT_FONT_PATH_TEST}")
screen = pygame.display.set_mode((600, 200))
pygame.display.set_caption("Font Test")
font_to_test = None
error_message = "Font load failed or cannot render."
try:
    if os.path.exists(DEFAULT_FONT_PATH_TEST):
        font_to_test = pygame.font.Font(DEFAULT_FONT_PATH_TEST, 30)
        if font_to_test:
            error_message = None # 清除错误信息，表示字体对象创建成功
        else: # font.Font 返回 None 的情况（理论上应该抛异常）
            error_message = f"pygame.font.Font returned None for {FONT_NAME}"
    else:
        error_message = f"Font file not found: {DEFAULT_FONT_PATH_TEST}"
except Exception as e:
    error_message = f"Error loading font {FONT_NAME}: {e}"
    print(error_message)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((50, 50, 50))
    if font_to_test and not error_message:
        try:
            text_surf_eng = font_to_test.render("Hello World", True, (255, 255, 255))
            text_surf_zh = font_to_test.render("你好世界 方格王国", True, (255, 255, 0))
            screen.blit(text_surf_eng, (20, 20))
            screen.blit(text_surf_zh, (20, 70))
        except Exception as render_e:
            print(f"Error rendering text: {render_e}")
            fail_surf = pygame.font.SysFont("arial", 20).render(f"Render error: {render_e}", True, (255,0,0))
            screen.blit(fail_surf, (20, 120))
    elif error_message:
        # 尝试用系统字体显示错误信息
        try:
            sys_font = pygame.font.SysFont("arial", 20) # 或者其他你确定存在的系统字体
            err_surf = sys_font.render(error_message, True, (255, 0, 0))
            screen.blit(err_surf, (20, 20))
        except Exception as e_sysfont:
             print(f"Could not even render error with SysFont: {e_sysfont}")
    pygame.display.flip()
pygame.quit()