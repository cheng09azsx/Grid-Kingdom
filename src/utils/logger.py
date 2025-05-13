"""
日志工具 - 提供游戏日志记录功能
该模块设置了日志系统，支持彩色控制台输出和文件记录，便于开发调试和问题追踪。
"""
import os
import sys
import logging
import colorlog
from datetime import datetime
from typing import Optional

def setup_logger(log_level: int = logging.INFO, log_to_file: bool = True) -> logging.Logger:
    """
    设置和配置日志系统
    
    Args:
        log_level: 日志级别，默认为INFO
        log_to_file: 是否将日志写入文件，默认为True
    
    Returns:
        logging.Logger: 配置好的日志记录器
    """
    # 确定日志文件的目录路径
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    log_dir = os.path.join(base_dir, "logs")
    
    # 创建日志目录
    os.makedirs(log_dir, exist_ok=True)
    
    # 配置根日志记录器
    logger = logging.getLogger("grid_kingdom")
    logger.setLevel(log_level)
    logger.propagate = False  # 防止日志向上传播
    
    # 避免重复添加处理器
    if logger.handlers:
        return logger
    
    # 创建彩色控制台处理器
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    
    # 配置彩色格式
    colors = {
        'DEBUG': 'cyan',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'red,bg_white',
    }
    
    console_formatter = colorlog.ColoredFormatter(
        '%(log_color)s[%(asctime)s][%(levelname)s][%(name)s]: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        log_colors=colors
    )
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    
    # 创建文件处理器
    if log_to_file:
        current_time = datetime.now().strftime('%Y%m%d_%H%M%S')
        log_filename = f"grid_kingdom_{current_time}.log"
        log_file_path = os.path.join(log_dir, log_filename)
        
        file_handler = logging.FileHandler(log_file_path, encoding='utf-8')
        file_handler.setLevel(log_level)
        
        file_formatter = logging.Formatter(
            '[%(asctime)s][%(levelname)s][%(name)s]: %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
    
    logger.info("日志系统初始化完成")
    
    # 记录一些系统信息，便于调试
    logger.info(f"Python 版本: {sys.version}")
    logger.info(f"运行平台: {sys.platform}")
    
    return logger
