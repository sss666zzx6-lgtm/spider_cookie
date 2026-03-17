import os
from dotenv import load_dotenv
from typing import Optional

load_dotenv()


def strtobool(val: str) -> bool:
    """将字符串转换为布尔值，兼容原 strtobool 行为"""
    val = val.lower()
    if val in ('y', 'yes', 't', 'true', 'on', '1'):
        return True
    elif val in ('n', 'no', 'f', 'false', 'off', '0'):
        return False
    else:
        raise ValueError(f"invalid truth value {val}")


class Settings:
    # 应用配置
    DEBUG: bool = False

    # 日志配置
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO").lower()
    LOG_DIR: Optional[str] = os.getenv("LOG_DIR", "logs")

    # 英飞凌账户和密码
    INFINEON_USER: Optional[str] = os.getenv("INFINEON_USER")
    INFINEON_PWD: Optional[str] = os.getenv("INFINEON_PWD")

    # DARWIN
    DARWIN_AK: Optional[str] = os.getenv("DARWIN_AK")
    DARWIN_SK: Optional[str] = os.getenv("DARWIN_SK")
    SYS_DARWIN_AK: Optional[str] = os.getenv("SYS_DARWIN_AK")
    SYS_DARWIN_SK: Optional[str] = os.getenv("SYS_DARWIN_SK")



settings = Settings()
