# /main.py
"""
游戏主入口点。
"""
from grid_kingdom.core.engine import GameEngine
from grid_kingdom.utils.logger import logger # 确保日志在最早被初始化和使用

def main():
    """主函数，创建并运行游戏引擎。"""
    logger.info("Application starting...")
    try:
        engine = GameEngine()
        engine.run()
    except Exception as e:
        logger.critical("An unhandled exception occurred in the_game engine!", exc_info=True)
        # exc_info=True 会记录完整的堆栈跟踪
        # 在生产环境中，可能需要更优雅的错误报告方式
    finally:
        logger.info("Application shutting down.")

if __name__ == "__main__":
    main()
