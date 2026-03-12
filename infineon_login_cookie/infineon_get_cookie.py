import time
from playwright.sync_api import sync_playwright
import requests
from util.logger import get_logger

logger = get_logger("infineon_cookie")


def login_foreign_website():
    with sync_playwright() as p:
        # 1. 启动浏览器（设置代理、语言，模拟海外环境）
        browser = p.chromium.launch(
            headless=False,
            # headless=True,
        )
        # 设置浏览器语言为英文（适配外国网站）
        context = browser.new_context()
        page = context.new_page()

        page.goto("https://www.infineon.com/")  # 英飞凌首页

        # 处理 Cookie 弹窗 - 点击 Accept
        try:
            accept_btn = page.wait_for_selector('#onetrust-accept-btn-handler', state='visible', timeout=5000)
            accept_btn.click()
            print("✅ 已点击 Accept 接受 Cookie")
            page.wait_for_timeout(1000)  # 等待弹窗消失
        except Exception as e:
            print(f"⚠️ 未找到 Cookie 弹窗，跳过：{e}")

        # 2. 等待”Log in to myInfineon”登录按钮加载，然后点击
        # 定位按钮：用你截图里的文本“Log in to myInfineon”
        login_button_selector = 'text=Log in to myInfineon'
        page.wait_for_selector(login_button_selector, state='visible', timeout=20000)
        page.click(login_button_selector)
        print("✅ 已进入英飞凌首页并点击登录按钮")

        # 2. 访问外国网站登录页（如英飞凌官网）
        # page.wait_for_url("https://sso.infineon.com/as/authorization.oauth2?scope=email+openid+profile+address+ifxScope&response_type=code&redirect_uri=https%3A%2F%2Fwww.infineon.com%2Fauth%2Fcallback&state=eK9r5AkFORF9bY_AHRSJ8X0M7N-XcIUeTiHGu7iFKHs%3AoriginURL%3D%2F%26action%3Dlg_lg%26ui_locales%3Den&code_challenge_method=S256&nonce=aEkCLW3s2zJJ4tJVXNrCoM7TvVc8nrtAF0L0wv7cJfE&client_id=ifxWebUser&code_challenge=8j6l8_gHqkAx2_h3KrzEqHwx8xFCRoTJ9_YNOMhwvJQ&ui_locales=EN")
        page.wait_for_selector('#identifierInput', state='visible', timeout=20000)
        page.fill('#identifierInput', 'sss666.zzx6@gmail.com')
        page.click('#signOnButton')

        page.wait_for_selector('#password', state='visible')
        # 输入密码（替换为你的真实密码）
        page.fill('#password', 'dmf123456xX@')
        # 点击登录按钮（和Next按钮是同一个ID，因为页面复用了组件）
        page.click('#signOnButton')
        print("✅ 已输入密码并点击登录按钮")

        print('\n========== 获取 Cookie ==========')

        # 获取所有 Cookie
        cookies = page.context.cookies()
        print(f'Cookie 数量：{len(cookies)}')

        # 转换为字符串格式（用于 requests）
        cookie_str = '; '.join([f"{c['name']}={c['value']}" for c in cookies])

        print(f'\nCookie 字符串:\n{cookie_str}')

        # 保存到文件
        # with open('infineon_cookie.txt', 'w', encoding='utf-8') as f:
        #     f.write(cookie_str)
        # print(f'\n✅ Cookie 已保存到 infineon_cookie.txt')
        # print('================================\n')

        # 保存 Cookie 后停留 3 秒
        print('\n登录完成，停留 3 秒后退出...')
        time.sleep(3)

        browser.close()

    return cookie_str

def verify_cookie(cookie_str):
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
            logger.info("响应类型为PDF，Cookie有效！")
            return True
        else:
            logger.error(f"响应不是PDF，Content-Type：{content_type}")
            logger.error(f"响应内容预览：{response_pdf.text[:200]}")
            return False

    except requests.exceptions.HTTPError as e:
        logger.error(f"HTTP请求失败：{e}")
        return False
    except Exception as e:
        logger.error(f"请求异常：{str(e)}")
        return False

if __name__ == "__main__":
    cookie_str = login_foreign_website()
    if cookie_str:
        print(cookie_str)
        verify_result = verify_cookie(cookie_str)



