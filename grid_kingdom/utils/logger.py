# grid_kingdom/utils/logger.py
"""
基础日志模块
提供一个配置好的logger实例，方便在项目各处使用。
"""
import logging
import sys
from logging.handlers import RotatingFileHandler # 用于日志文件轮转

# --- 配置常量 ---
LOG_LEVEL = logging.DEBUG  # 日志记录的最低级别 (DEBUG, INFO, WARNING, ERROR, CRITICAL)
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(name)s - [%(filename)s:%(lineno)d] - %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
LOG_FILE_PATH = "grid_kingdom.log"  # 日志文件路径
ENABLE_FILE_LOGGING = True  # 是否启用文件日志记录
ENABLE_CONSOLE_LOGGING = True # 是否启用控制台日志记录

# --- Logger实例 ---
# 获取根logger或者一个特定的logger，这里我们使用模块名作为logger名
# 如果在不同模块使用相同的logger_name，它们会共享配置
# 通常一个应用使用一个主logger，或者模块划分logger
logger = logging.getLogger("GridKingdom")
logger.setLevel(LOG_LEVEL) # 设置logger处理的最低级别

# --- 防止重复添加handler ---
# 如果logger.handlers为空，才添加新的handler
if not logger.handlers:
    # --- 控制台Handler ---
    if ENABLE_CONSOLE_LOGGING:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(LOG_LEVEL)
        console_formatter = logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT)
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)

    # --- 文件Handler (带轮转功能) ---
    if ENABLE_FILE_LOGGING:
        # RotatingFileHandler会在文件达到一定大小时自动创建新文件
        # maxBytes: 单个日志文件的最大大小 (这里设为5MB)
        # backupCount: 保留的旧日志文件数量
        file_handler = RotatingFileHandler(
            LOG_FILE_PATH,
            maxBytes=5 * 1024 * 1024, # 5 MB
            backupCount=3,
            encoding='utf-8'
        )
        file_handler.setLevel(LOG_LEVEL)
        file_formatter = logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT)
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

# --- 导出logger实例，方便其他模块使用 ---
# 使用方法: from grid_kingdom.utils.logger import logger
# logger.debug("This is a debug message.")
# logger.info("This is an info message.")
# logger.warning("This is a warning message.")
# logger.error("This is an error message.")
# logger.critical("This is a critical message.")

if __name__ == '__main__':
    # 测试日志功能
    logger.debug("日志模块测试：这是一条 DEBUG 信息。")
    logger.info("日志模块测试：这是一条 INFO 信息。")
    logger.warning("日志模块测试：这是一条 WARNING 信息。")
    logger.error("日志模块测试：这是一条 ERROR 信息。")
    logger.critical("日志模块测试：这是一条 CRITICAL 信息。")

    try:
        x = 1 / 0
    except ZeroDivisionError:
        logger.exception("日志模块测试：捕获到一个异常！") # logger.exception会自动记录堆栈信息
