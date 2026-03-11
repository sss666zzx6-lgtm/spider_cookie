from curl_cffi import requests
import os
import time
import schedule
from datetime import datetime, timedelta
from util.logger import get_logger

logger = get_logger("refresh_cookie_task")

# 全局Session对象（保持会话）
global_session = None
# 初始Cookie字符串
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'renesas_cookie.txt'), 'r', encoding='utf-8') as f:
    cookie_str = f.read()
logger.info(f"cookie_str: {cookie_str}")
INITIAL_COOKIE = cookie_str

# 初始化Session（只执行一次，保持会话）
def init_session():
    """初始化全局Session对象，设置Cookie和UA"""
    global global_session
    if global_session is None:
        global_session = requests.Session()
        # 设置请求头
        headers = {
            "cookie": INITIAL_COOKIE,
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36"
        }
        global_session.headers.update(headers)
        logger.info("全局Session初始化完成")
    return global_session


def verify_cookie(session):
    """验证Cookie有效性"""
    pdf_url = "https://www.renesas.com/en/document/dst/cl8060-datasheet"
    time.sleep(1)

    try:
        response = session.get(
            pdf_url,
            stream=True,  # 保持stream=True避免自动下载正文
            timeout=15,
            impersonate="chrome110"
        )

        response.raise_for_status()
        logger.info(f"请求成功，状态码：{response.status_code}")

        content_type = response.headers.get("Content-Type", "").lower()
        if "application/pdf" in content_type:
            logger.info("响应类型为PDF，Cookie有效！")
            return True
        else:
            logger.error(f"响应不是PDF，Content-Type：{content_type}")
            logger.error(f"响应内容预览：{response.text[:200]}")
            return False

    except requests.exceptions.HTTPError as e:
        logger.error(f"HTTP请求失败：{e}")
        return False
    except Exception as e:
        logger.error(f"请求异常：{str(e)}")
        return False


def task():
    """定时任务核心逻辑：验证Cookie"""
    logger.info("=" * 50)
    logger.info("开始执行6小时一次的Cookie验证任务")

    # 记录任务开始时间
    start_time = datetime.now()
    logger.info(f"任务开始时间：{start_time.strftime('%Y-%m-%d %H:%M:%S')}")

    # 获取全局Session
    session = init_session()

    # 第一步：访问myrenesas页面保持会话
    product_url = "https://www.renesas.com/en/myrenesas"
    try:
        response = session.get(product_url, impersonate="chrome110", timeout=15)
        logger.info(f"访问myrenesas状态码：{response.status_code}")
    except Exception as e:
        logger.error(f"访问myrenesas失败：{str(e)}")

    # 第二步：验证Cookie有效性
    is_valid = verify_cookie(session)

    # 记录任务结束时间和下次执行时间
    end_time = datetime.now()
    next_run_time = end_time + timedelta(hours=6)
    logger.info(f"任务结束时间：{end_time.strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info(f"下次执行时间：{next_run_time.strftime('%Y-%m-%d %H:%M:%S')}")

    logger.info("本次定时任务执行完成")
    logger.info("=" * 50)


if __name__ == "__main__":
    # 1. 初始化Session
    init_session()

    # 2. 立即执行一次任务（首次启动）
    logger.info("启动定时任务，首次执行Cookie验证...")
    task()

    # 3. 清理原有定时任务（避免重复）
    schedule.clear()

    # 4. 配置精准的定时任务：每6小时执行一次
    schedule.every(6).hours.do(task)
    logger.info(f"定时任务已配置：每6小时执行一次Cookie验证")

    # 5. 打印下次执行时间（便于调试）
    next_run = schedule.next_run()
    logger.info(f"下次任务执行时间：{next_run.strftime('%Y-%m-%d %H:%M:%S')}")

    # 6. 循环执行定时任务（缩短检查间隔，提高精准度）
    while True:
        schedule.run_pending()
        # 缩短检查间隔到1分钟，减少时间误差
        time.sleep(60)


