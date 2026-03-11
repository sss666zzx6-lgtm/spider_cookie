from DrissionPage import WebPage, ChromiumOptions
import time

LOGIN_EMAIL = "3521445647@qq.com"
LOGIN_PASSWORD = "123456xX@"


def get_renesas_cookie():
    """打开瑞萨登录页 → 填写账号密码 → 点击登录按钮"""
    co = ChromiumOptions()
    # 调试时注释掉headless，显示浏览器窗口
    # co.set_argument('--headless=new')
    # co.set_argument('--blink-settings=imagesEnabled=false')
    # co.set_argument('--mute-audio')

    page = None
    try:
        page = WebPage(chromium_options=co)
        page.set.window.max()  # 最大化浏览器窗口
        login_url = 'https://www.renesas.com/en/user/sso-login/?destination=/en/products/cl8060%3Ftab%3Ddocumentation%26_gl%3D1*1lqy5xu*_gcl_au*MTk4Njc2NTQ3NS4xNzY4NDYzOTE0LjE3NzE1NjY3MDcuMTc3MTkyNjY2Mi4xNzcxOTI2NjY4*_ga*NjI4NjIzMjAwLjE3Njg0NjM5MTQ.*_ga_D1706WVDQV*czE3NzIwOTgzNjkkbzgkZzAkdDE3NzIwOTgzNzQkajU1JGwwJGgw'
        page.get(login_url)

        # 等待页面加载
        time.sleep(10)
        # 1. 填写邮箱
        print('🔄 正在查找用户名输入框...')

        # 主逻辑：等待并查找元素（带多种备选定位方式）
        email_ele = None
        # 尝试 1: CSS ID 定位（# 表示 ID）
        try:
            email_ele = page.ele('#edit-username', timeout=10)
            print('✅ 通过 ID 找到用户名输入框')
        except:
            # 尝试 2: name 属性
            try:
                email_ele = page.ele('@name=username', timeout=5)
                print('✅ 通过 name 找到用户名输入框')
            except:
                # 尝试 3: data-drupal-selector 属性（最稳定）
                try:
                    email_ele = page.ele('@data-drupal-selector=edit-username', timeout=5)
                    print('✅ 通过 data-drupal-selector 找到用户名输入框')
                except:
                    print('❌ 所有定位方式都失败了')

        if email_ele:
            email_ele.clear()
            email_ele.input(LOGIN_EMAIL)
            print(f'✅ 已填写邮箱：{LOGIN_EMAIL}')
        else:
            print('❌ 未找到用户名输入框，请手动检查页面结构')
            # 打印当前页面所有输入框用于调试
            inputs = page.eles('tag:input')
            print(f'调试信息：当前页面找到 {len(inputs)} 个输入框')
            for i, inp in enumerate(inputs[:5]):  # 只显示前 5 个
                print(f'  [{i}] {inp.attrs}')

        # 2. 填写密码
        try:
            password_ele = page.ele('#edit-password', timeout=10)
            password_ele.clear()
            password_ele.input(LOGIN_PASSWORD)
            print(f'✅ 已填写密码')
        except Exception as e:
            print(f'❌ 未找到密码输入框：{e}')
            return

        # 3. 定位并点击登录按钮（核心新增逻辑）
        try:
            # 方式1：用id定位（最推荐，id唯一且稳定）
            login_btn = page.ele('#edit-submit', timeout=10)
            # 方式2：备选（用value文本定位，适配按钮文本）
            # login_btn = page.wait.ele_enabled('value:Log In', timeout=10)
            # 方式3：备选（用data-drupal-selector定位）
            # login_btn = page.wait.ele_enabled('data-drupal-selector:edit-submit', timeout=10)

            # 点击登录按钮
            login_btn.click()
            print('✅ 已点击登录按钮，等待登录结果...')

            # 等待登录跳转（等待 5 秒）
            time.sleep(5)

            # ================================
            # 获取并保存 Cookie（核心新增）
            # ================================
            print('\n========== 获取 Cookie ==========')

            # 获取所有 Cookie（DrissionPage 返回 CookiesList 对象，是列表格式）
            cookies_list = page.cookies()

            # 转换为字典格式
            cookies_dict = {}
            for cookie in cookies_list:
                cookies_dict[cookie['name']] = cookie['value']

            print(f'Cookie 字典格式：{cookies_dict}')

            # 转换为字符串格式（用于 requests）
            cookie_str = '; '.join([f"{k}={v}" for k, v in cookies_dict.items()])
            print(f'\nCookie 字符串格式:\n{cookie_str}')

            # 保存到文件
            with open('renesas_cookie.txt', 'w', encoding='utf-8') as f:
                f.write(cookie_str)
            print(f'\n✅ Cookie 已保存到 renesas_cookie.txt')
            print('================================\n')

            # 返回 Cookie 字符串（方便后续使用）
            return cookie_str

        except Exception as e:
            print(f'⚠️ 获取 Cookie 失败：{str(e)}')

        # 停留页面查看结果
        print('\n登录操作完成，页面将停留30秒...')
        time.sleep(30)

    except Exception as e:
        print(f'❌ 整体流程失败：{str(e)}')
    finally:
        try:
            page.close()
            page.quit()
        except:
            pass

if __name__ == '__main__':
    get_renesas_cookie()
    with open('renesas_cookie.txt', 'r', encoding='utf-8') as f:
        cookie_str = f.read()
        print(cookie_str)