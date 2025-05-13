# utils/logger.py
"""
日志工具，配置日志系统
"""
import logging
import os
from datetime import datetime

def setup_logger():
    """
    设置日志系统
    
    Returns:
        logging.Logger: 配置好的日志器
    """
    # 创建logs目录(如果不存在)
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    # 获取当前日期时间作为日志文件名的一部分
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = f"logs/grid_kingdom_{current_time}.log"
    
    # 配置根日志器
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    
    # 创建文件处理器
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)
    
    # 创建控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    # 创建格式化器
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # 添加处理器到日志器
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger
