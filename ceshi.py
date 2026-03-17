# import time
# import os  # 新增：用于设置环境变量、校验路径
# from playwright.sync_api import sync_playwright
# import requests
# from utils.logger import get_logger
#
# logger = get_logger("infineon_cookie")
#
#
# def login_infineon():
#     # ========== 关键修改1：指定Playwright下载的Firefox路径 ==========
#     # 替换为你实际下载的Firefox版本号（比如firefox-1509）
#     FIREFOX_VERSION = "1509"
#     firefox_path = os.path.expanduser(f"~/.cache/ms-playwright/firefox-{FIREFOX_VERSION}/firefox/firefox")
#
#     # 校验Firefox路径是否存在，避免启动失败
#     if not os.path.exists(firefox_path):
#         error_msg = f"❌ Firefox路径不存在：{firefox_path}\n请执行以下命令确认版本号：ls ~/.cache/ms-playwright/"
#         logger.error(error_msg)
#         raise FileNotFoundError(error_msg)
#
#     with sync_playwright() as p:
#         # ========== 关键修改2：Firefox启动参数（解决无sudo/依赖问题） ==========
#         browser = p.firefox.launch(
#             # 改用新版无头模式（无桌面依赖，必须用new，不能用True）
#             headless="new",
#             # 核心参数：绕过Linux系统限制、无sudo适配
#             args=[
#                 '--no-sandbox',                # 非root用户必需
#                 '--disable-dev-shm-usage',     # 解决/dev/shm空间不足
#                 '--disable-gpu',               # 禁用GPU（无显卡环境）
#                 '--disable-software-rasterizer', # 兼容无渲染环境
#                 '--no-xshm',                   # 禁用X11共享内存（无桌面）
#                 '--remote-debugging-port=0',   # 避免端口冲突
#             ],
#             # 强制指定便携版Firefox，不用系统依赖缺失的浏览器
#             executable_path=firefox_path,
#             # 禁用Playwright默认的扩展参数，减少依赖报错
#             ignore_default_args=["--disable-extensions"],
#         )
#
#         # ========== 原有逻辑完全保留 ==========
#         # 设置浏览器语言为英文（适配外国网站）
#         context = browser.new_context(
#             locale="en-US"  # 补充：显式设置英文，适配海外网站
#         )
#         page = context.new_page()
#
#         page.goto("https://www.infineon.com/")  # 英飞凌首页
#
#         # 处理 Cookie 弹窗 - 点击 Accept
#         try:
#             accept_btn = page.wait_for_selector('#onetrust-accept-btn-handler', state='visible', timeout=5000)
#             accept_btn.click()
#             logger.info("✅ 已点击 Accept 接受 Cookie")
#             page.wait_for_timeout(1000)  # 等待弹窗消失
#         except Exception as e:
#             logger.warning(f"⚠️ 未找到 Cookie 弹窗，跳过：{e}")
#
#         # 2. 等待”Log in to myInfineon”登录按钮加载，然后点击
#         login_button_selector = 'text=Log in to myInfineon'
#         page.wait_for_selector(login_button_selector, state='visible', timeout=20000)
#         page.click(login_button_selector)
#         logger.info("✅ 已进入英飞凌首页并点击登录按钮")
#
#         # 等待账号输入框并输入
#         page.wait_for_selector('#identifierInput', state='visible', timeout=20000)
#         page.fill('#identifierInput', 'sss666.zzx6@gmail.com')
#         page.click('#signOnButton')
#
#         # 等待密码框并输入
#         page.wait_for_selector('#password', state='visible')
#         page.fill('#password', 'dmf123456xX@')
#         page.click('#signOnButton')
#         logger.info("✅ 已输入密码并点击登录按钮")
#
#         logger.info('\n========== 获取 Cookie ==========')
#
#         # 获取所有 Cookie
#         cookies = page.context.cookies()
#         logger.info(f'Cookie 数量：{len(cookies)}')
#
#         # 转换为字符串格式（用于 requests）
#         cookie_str = '; '.join([f"{c['name']}={c['value']}" for c in cookies])
#
#         logger.info(f'\nCookie 字符串:\n{cookie_str}')
#
#         # 保存到文件（可选开启）
#         # with open('infineon_cookie.txt', 'w', encoding='utf-8') as f:
#         #     f.write(cookie_str)
#         # logger.info(f'\n✅ Cookie 已保存到 infineon_cookie.txt')
#
#         # 保存 Cookie 后停留 3 秒
#         logger.info('\n登录完成，停留 3 秒后退出...')
#         time.sleep(3)
#
#         browser.close()
#
#     return cookie_str
#
# def verify_cookie(cookie_str):
#     headers = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
#         'Cookie': cookie_str,
#     }
#
#     pdf_url = "https://www.infineon.com/assets/row/public/documents/10/64/infineon-automotive-application-guide-2021-applicationbrochure-en.pdf"
#
#     try:
#         response_pdf = requests.get(pdf_url, stream=True, headers=headers, timeout=15)
#
#         response_pdf.raise_for_status()
#         logger.info(f"请求成功，状态码：{response_pdf.status_code}")
#
#         content_type = response_pdf.headers.get("Content-Type", "").lower()
#         if "application/pdf" in content_type:
#             logger.info("响应类型为PDF，Cookie有效！")
#             return True
#         else:
#             logger.error(f"响应不是PDF，Content-Type：{content_type}")
#             logger.error(f"响应内容预览：{response_pdf.text[:200]}")
#             return False
#
#     except requests.exceptions.HTTPError as e:
#         logger.error(f"HTTP请求失败：{e}")
#         return False
#     except Exception as e:
#         logger.error(f"请求异常：{str(e)}")
#         return False
#
# if __name__ == "__main__":
#     # ========== 关键修改3：启动前跳过Playwright依赖校验 ==========
#     os.environ["PLAYWRIGHT_SKIP_DEPENDENCY_VALIDATION"] = "1"
#
#     try:
#         cookie_str = login_infineon()
#         if cookie_str:
#             logger.info(f"最终获取的Cookie：{cookie_str}")
#             verify_result = verify_cookie(cookie_str)
#             logger.info(f"Cookie验证结果：{'有效' if verify_result else '无效'}")
#     except Exception as e:
#         logger.error(f"程序执行失败：{type(e).__name__} - {str(e)}")
#         raise  # 可选：抛出异常，方便定位问题