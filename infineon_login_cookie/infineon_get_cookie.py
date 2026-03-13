import time
import schedule
from datetime import datetime, timedelta
from playwright.sync_api import sync_playwright
import requests
from util.logger import get_logger
from util.create_cookie_api import create_cookie

logger = get_logger("infineon_cookie")

# 全局 Cookie 字符串
global_cookie_str = None
# 重试计数器
retry_count = 0
MAX_RETRY = 5  # 最多重试 5 次


def login_infineon():
    """登录英飞凌获取 Cookie"""
    logger.info("========== 开始登录英飞凌获取 Cookie ==========")

    with sync_playwright() as p:
        # 启动浏览器
        browser = p.firefox.launch(
            headless=True,
        )
        # 设置浏览器语言为英文（适配外国网站）
        context = browser.new_context()
        page = context.new_page()

        page.goto("https://www.infineon.com/")  # 英飞凌首页

        # 处理 Cookie 弹窗 - 点击 Accept
        try:
            accept_btn = page.wait_for_selector('#onetrust-accept-btn-handler', state='visible', timeout=5000)
            accept_btn.click()
            logger.info("✅ 已点击 Accept 接受 Cookie")
            page.wait_for_timeout(1000)  # 等待弹窗消失
        except Exception as e:
            logger.info(f"⚠️ 未找到 Cookie 弹窗，跳过：{e}")

        # 等待"Log in to myInfineon"登录按钮加载，然后点击
        login_button_selector = 'text=Log in to myInfineon'
        page.wait_for_selector(login_button_selector, state='visible', timeout=20000)
        page.click(login_button_selector)
        logger.info("✅ 已进入英飞凌首页并点击登录按钮")

        # 填写账号密码
        page.wait_for_selector('#identifierInput', state='visible', timeout=20000)
        page.fill('#identifierInput', 'sss666.zzx6@gmail.com')
        page.click('#signOnButton')

        page.wait_for_selector('#password', state='visible')
        page.fill('#password', 'dmf123456xX@')
        page.click('#signOnButton')
        logger.info("✅ 已输入密码并点击登录按钮")

        logger.info('\n========== 获取 Cookie ==========')

        # 获取所有 Cookie
        cookies = page.context.cookies()
        logger.info(f'Cookie 数量：{len(cookies)}')

        # 转换为字符串格式（用于 requests）
        cookie_str = '; '.join([f"{c['name']}={c['value']}" for c in cookies])

        logger.info(f'\nCookie 字符串:\n{cookie_str}')

        # 保存 Cookie 后停留 3 秒
        logger.info('\n登录完成，停留 3 秒后退出...')
        time.sleep(3)

        browser.close()

    logger.info("========== Cookie 获取完成 ==========")
    return cookie_str


def verify_cookie(cookie_str):
    """验证 Cookie 有效性"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Cookie': cookie_str,
    }

    pdf_url = "https://www.infineon.com/assets/row/public/documents/10/64/infineon-automotive-application-guide-2021-applicationbrochure-en.pdf"

    try:
        response_pdf = requests.get(pdf_url, stream=True, headers=headers)
        response_pdf.raise_for_status()
        logger.info(f"请求成功，状态码：{response_pdf.status_code}")

        content_type = response_pdf.headers.get("Content-Type", "").lower()
        if "application/pdf" in content_type:
            logger.info("响应类型为 PDF，Cookie 有效！")
            return True
        else:
            logger.error(f"响应不是 PDF，Content-Type：{content_type}")
            logger.error(f"响应内容预览：{response_pdf.text[:200]}")
            return False

    except requests.exceptions.HTTPError as e:
        logger.error(f"HTTP 请求失败：{e}")
        return False
    except Exception as e:
        logger.error(f"请求异常：{str(e)}")
        return False


def add_api_cookie(cookie_str):
    """调用 API 添加 Cookie"""
    logger.info("========== 调用 API 添加 Cookie ==========")
    create_cookie("www.infineon.com", cookie_str)
    logger.info("✅ Cookie 已添加到 API")


def task():
    """定时任务核心逻辑：验证 Cookie"""
    global global_cookie_str, retry_count

    logger.info("=" * 50)
    logger.info("开始执行 3 小时一次的 Cookie 验证任务")
    logger.info(f"任务执行时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info(f"当前重试次数：{retry_count}/{MAX_RETRY}")

    # 检查是否超过最大重试次数
    if retry_count >= MAX_RETRY:
        logger.error(f"已达到最大重试次数 ({MAX_RETRY})，停止自动登录，请人工介入检查！")
        logger.info("本次定时任务执行完成")
        logger.info("=" * 50)
        return

    # 验证当前 Cookie 有效性
    if global_cookie_str:
        is_valid = verify_cookie(global_cookie_str)
    else:
        logger.warning("当前没有 Cookie，需要重新登录")
        is_valid = False

    # 如果 Cookie 无效，重新登录获取新 Cookie
    if not is_valid:
        logger.warning("Cookie 验证失败，开始重新登录...")
        new_cookie = login_infineon()

        # 验证新 Cookie 有效性
        if verify_cookie(new_cookie):
            logger.info("新 Cookie 验证通过，更新全局 Cookie 并添加到 API")
            global_cookie_str = new_cookie
            add_api_cookie(new_cookie)
            # 重置重试计数器
            retry_count = 0
            logger.info("Cookie 验证成功，重试计数器已重置为 0")
        else:
            logger.error("新 Cookie 验证失败，无法添加到 API")
            retry_count += 1
            logger.warning(f"重试次数 +1，当前重试次数：{retry_count}/{MAX_RETRY}")
    else:
        logger.info("Cookie 验证通过，继续使用当前 Cookie")
        # 验证成功后重置计数器
        retry_count = 0

    # 计算下次执行时间
    next_run_time = datetime.now() + timedelta(hours=3)
    logger.info(f"下次执行时间：{next_run_time.strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("本次定时任务执行完成")
    logger.info("=" * 50)


if __name__ == "__main__":
    # 1. 首次执行：登录获取 Cookie
    logger.info("========== 首次启动，开始登录获取 Cookie ==========")
    cookie = login_infineon()

    # 2. 验证 Cookie 有效性
    logger.info("========== 验证 Cookie 有效性 ==========")
    verify_result = verify_cookie(cookie)

    if verify_result:
        # 3. 验证通过，添加到 API
        logger.info("========== Cookie 验证通过，添加到 API ==========")
        global_cookie_str = cookie
        add_api_cookie(cookie)
        logger.info("========== 首次执行完成 ==========")
    else:
        logger.error("首次获取的 Cookie 验证失败，无法添加到 API")
        retry_count += 1
        logger.warning(f"重试次数 +1，当前重试次数：{retry_count}/{MAX_RETRY}")
        # Cookie 无效，不添加到全局变量

    # 4. 配置定时任务：每 3 小时执行一次
    schedule.clear()
    schedule.every(3).hours.do(task)
    logger.info("定时任务已配置：每 3 小时执行一次 Cookie 验证")

    # 5. 打印下次执行时间
    next_run = schedule.next_run()
    logger.info(f"下次任务执行时间：{next_run.strftime('%Y-%m-%d %H:%M:%S')}")

    # 6. 循环执行定时任务
    while True:
        schedule.run_pending()
        time.sleep(60)  # 每分钟检查一次
