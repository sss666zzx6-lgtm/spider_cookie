from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import requests
from util.create_cookie_api import create_cookie


def get_mouser_cookie_with_edge(url: str) -> tuple[list, webdriver.Edge]:

    edge_options = Options()
    # 注释掉下面一行可显示Edge窗口（必须显示，才能保持打开）
    # edge_options.add_argument("--headless=new")
    edge_options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
    edge_options.add_argument("--disable-popup-blocking")
    edge_options.add_argument("--ignore-certificate-errors")
    edge_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    edge_options.add_experimental_option('useAutomationExtension', False)
    edge_options.add_argument("--disable-blink-features=AutomationControlled")

    driver = None
    try:
        driver = webdriver.Edge(options=edge_options)
        driver.get(url)

        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.TAG_NAME, "title"))
        )
        time.sleep(2)

        cookies = driver.get_cookies()
        print("Edge获取到的Cookie列表：")
        for cookie in cookies:
            print(f"名称：{cookie['name']} | 值：{cookie['value']} | 域名：{cookie['domain']}")

        return cookies, driver

    except Exception as e:
        print(f"Edge获取Cookie失败：{str(e)}")
        if driver:
            input("\n程序出错，按回车键关闭浏览器...")
            driver.quit()
        return [], None


def format_cookie_for_headers(cookie_list: list) -> str:

    cookie_parts = []
    for cookie in cookie_list:
        name = cookie.get("name", "")
        value = cookie.get("value", "")
        if name and value:
            cookie_parts.append(f"{name}={value}")

    return "; ".join(cookie_parts)

if __name__ == "__main__":
    target_url = "https://www.mouser.com/ProductDetail/Kinetic-Technologies/KTU1128EGAD-TA?qs=P%2FxahI%252BVehmzxSyJ6TAHmQ%3D%3D"

    # 1. 获取Cookie和浏览器驱动对象
    cookie_list, driver = get_mouser_cookie_with_edge(target_url)
    cookie_str = format_cookie_for_headers(cookie_list)
    print(f"\n【拼接后的Cookie（可直接放入Headers）】\n{cookie_str}")

    # 2. 关键逻辑：只有按回车才关闭浏览器
    if driver:
        input("\n浏览器已保持打开，按回车键关闭浏览器并退出脚本...")
        driver.quit()
        print("浏览器已关闭，脚本退出")

    host = "www.mouser.com"
    create_cookie(host=host, cookie=cookie_str)



    # headers = {
    #     "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    #     "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    #     "cache-control": "no-cache",
    #     "pragma": "no-cache",
    #     "priority": "u=0, i",
    #     "sec-ch-device-memory": "8",
    #     "sec-ch-ua": "\"Not(A:Brand\";v=\"8\", \"Chromium\";v=\"144\", \"Microsoft Edge\";v=\"144\"",
    #     "sec-ch-ua-arch": "\"x86\"",
    #     "sec-ch-ua-full-version-list": "\"Not(A:Brand\";v=\"8.0.0.0\", \"Chromium\";v=\"144.0.7559.133\", \"Microsoft Edge\";v=\"144.0.3719.115\"",
    #     "sec-ch-ua-mobile": "?0",
    #     "sec-ch-ua-model": "\"\"",
    #     "sec-ch-ua-platform": "\"Windows\"",
    #     "sec-fetch-dest": "document",
    #     "sec-fetch-mode": "navigate",
    #     "sec-fetch-site": "none",
    #     "sec-fetch-user": "?1",
    #     "upgrade-insecure-requests": "1",
    #     "cookie": cookie_str,
    #     "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36 Edg/144.0.0.0"
    # }
    # url = "https://www.mouser.com/ProductDetail/Kinetic-Technologies/KTU1128EGAD-TA"
    # params = {
    #     "qs": "P/xahI%2BVehmzxSyJ6TAHmQ=="
    # }
    # response = requests.get(url, headers=headers, params=params)
    #
    # print(response.text)
    # print(response)