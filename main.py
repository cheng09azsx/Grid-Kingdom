"""
方格王国 (Grid Kingdom) - 主程序入口
该模块是游戏的入口点，负责初始化日志系统和启动游戏引擎。
"""
import os
import sys
import logging
import argparse
from src.utils.logger import setup_logger
from src.core.engine import GameEngine

def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description="方格王国 - 策略性方格世界建造游戏")
    parser.add_argument("--debug", action="store_true", help="启用调试模式")
    parser.add_argument("--no-log-file", action="store_true", help="禁用日志文件")
    return parser.parse_args()

def main():
    """游戏主函数入口"""
    # 解析命令行参数
    args = parse_args()
    
    # 设置日志级别
    log_level = logging.DEBUG if args.debug else logging.INFO
    
    # 设置日志系统
    logger = setup_logger(log_level=log_level, log_to_file=not args.no_log_file)
    logger.info("方格王国游戏启动中...")
    
    try:
        # 创建并启动游戏引擎
        engine = GameEngine()
        return engine.run()
    except KeyboardInterrupt:
        logger.info("用户中断游戏")
        return 0
    except Exception as e:
        logger.error(f"游戏运行出错: {e}", exc_info=True)
        return 1

if __name__ == "__main__":
    sys.exit(main())
