import os
import logging
from datetime import datetime
from pathlib import Path
from typing import Optional
from logging.handlers import RotatingFileHandler


class LoggerManager:
    """统一日志管理器"""

    def __init__(self):
        self.loggers = {}

    def get_logger(self, name: Optional[str] = None) -> logging.Logger:
        """
        获取日志记录器
        :param name: 日志记录器名称
        :return: logging.Logger实例
        """
        if name is None:
            name = "app"

        if name in self.loggers:
            return self.loggers[name]

        # 创建日志记录器（固定日志级别为INFO，替代settings.LOG_LEVEL）
        logger = logging.getLogger(name)
        logger.setLevel(logging.INFO)  # 固定级别：INFO

        # 避免重复添加处理器
        if not logger.handlers:
            # 创建格式化器
            formatter = logging.Formatter(
                fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )

            # 控制台处理器（固定级别为INFO）
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)  # 固定级别
            console_handler.setFormatter(formatter)
            logger.addHandler(console_handler)

            # 文件处理器（固定日志目录为项目根目录的logs文件夹）
            log_dir = "./logs"  # 固定日志目录，替代settings.LOG_DIR
            if log_dir:
                if not os.path.exists(log_dir):
                    os.makedirs(log_dir, exist_ok=True)

                log_file = os.path.join(log_dir, f"{name}.log")
                file_handler = RotatingFileHandler(
                    log_file,
                    maxBytes=10 * 1024 * 1024,  # 10MB
                    backupCount=20,
                    encoding='utf-8'
                )
                file_handler.setLevel(logging.INFO)  # 固定级别
                file_handler.setFormatter(formatter)
                logger.addHandler(file_handler)

        self.loggers[name] = logger
        return logger


# 全局日志管理器实例
logger_manager = LoggerManager()


def get_logger(name: Optional[str] = None) -> logging.Logger:
    """
    获取日志记录器的便捷函数
    :param name: 日志记录器名称
    :return: logging.Logger实例
    """
    return logger_manager.get_logger(name)