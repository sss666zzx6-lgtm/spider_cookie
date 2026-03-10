# from DrissionPage import WebPage, ChromiumOptions
# import time
#
#
# def open_renesas_website():
#     """使用DrissionPage打开瑞萨电子官网（英文站）"""
#     # 1. 配置浏览器选项（可选，比如禁用图片加载、无痕模式等）
#     co = ChromiumOptions()
#     # 可选：启用无痕模式（避免缓存影响）
#     # co.add_argument('--incognito')
#     # 可选：禁用图片加载，加快页面加载速度
#     # co.add_argument('--blink-settings=imagesEnabled=false')
#
#     try:
#         # 2. 创建WebPage对象（自动调用本地Chrome/Edge浏览器）
#         page = WebPage(chromium_options=co)
#
#         # 3. 打开目标网址（会自动等待页面基本加载完成）
#         url = 'https://www.renesas.com/en/user/sso-login/?destination=/en/products/cl8060%3Ftab%3Ddocumentation%26_gl%3D1*1lqy5xu*_gcl_au*MTk4Njc2NTQ3NS4xNzY4NDYzOTE0LjE3NzE1NjY3MDcuMTc3MTkyNjY2Mi4xNzcxOTI2NjY4*_ga*NjI4NjIzMjAwLjE3Njg0NjM5MTQ.*_ga_D1706WVDQV*czE3NzIwOTgzNjkkbzgkZzAkdDE3NzIwOTgzNzQkajU1JGwwJGgw'
#         print(f'正在打开网址：{url}')
#         page.get(url)
#
#         # 4. 等待页面完全加载（可选，根据页面复杂度调整等待时间）
#         # 方式1：固定等待3秒（简单粗暴）
#         time.sleep(3)
#         # 方式2：等待某个元素加载完成（更优雅，推荐）
#         # page.wait.ele_displayed('//header', timeout=10)  # 等待头部导航栏显示
#
#         print('✅ 网址已成功打开！')
#
#         # 5. 可选：停留10秒后关闭浏览器（按需调整/删除）
#         print('页面将在10秒后关闭...')
#         time.sleep(10)
#
#         # 6. 关闭页面和浏览器
#         page.close()
#
#     except Exception as e:
#         print(f'❌ 打开网址失败：{str(e)}')
#     finally:
#         # 确保浏览器进程完全退出
#         try:
#             page.quit()
#         except:
#             pass
#
#
# if __name__ == '__main__':
#     open_renesas_website()

from DrissionPage import WebPage, ChromiumOptions
import time
urls = [f"https://auk.co.kr/eng/s2/product.asp?idx={i}" for i in range(1,4)]


def open_renesas_website():
    """使用DrissionPage自动下载便携版Chromium，无界面打开瑞萨登录页"""
    # 1. 配置浏览器选项（无界面运行，移除无效的portable参数）
    co = ChromiumOptions()
    # 核心：无界面模式（新版API用set_argument）
    # co.set_argument('--headless=new')
    # 可选：禁用图片/音频，加快加载
    co.set_argument('--blink-settings=imagesEnabled=false')
    co.set_argument('--mute-audio')
    # 移除 co.set_browser_path(portable=True) → 新版无需此配置，自动下载便携版

    try:
        # 2. 创建WebPage对象（自动检测浏览器，无本地浏览器则下载便携版）
        print('📥 检测本地浏览器...无Chrome/Edge时将自动下载便携版Chromium（首次运行需等待）...')
        # 新版WebPage会自动处理便携版下载，无需手动配置
        page = WebPage(chromium_options=co)

        # 3. 打开目标网址（支持JS渲染，适配登录页）
        url = 'https://www.renesas.com/en/user/sso-login/?destination=/en/products/cl8060%3Ftab%3Ddocumentation%26_gl%3D1*1lqy5xu*_gcl_au*MTk4Njc2NTQ3NS4xNzY4NDYzOTE0LjE3NzE1NjY3MDcuMTc3MTkyNjY2Mi4xNzcxOTI2NjY4*_ga*NjI4NjIzMjAwLjE3Njg0NjM5MTQ.*_ga_D1706WVDQV*czE3NzIwOTgzNjkkbzgkZzAkdDE3NzIwOTgzNzQkajU1JGwwJGgw'
        print(f'正在打开网址：{url}')
        page.get(url)

        # 4. 等待页面加载（等待登录表单元素，更精准）
        try:
            # 等待登录相关元素加载（可根据实际页面调整XPath）
            page.wait.ele_displayed('//input[@type="text" or @type="email"]', timeout=15)
            print('✅ 页面加载完成（登录表单已渲染）！')
        except Exception as e:
            print(f'⚠️ 页面加载超时（可能是元素XPath需调整），但网址已打开：{str(e)}')

        # 5. 停留后关闭浏览器
        print('页面将在10秒后关闭...')
        time.sleep(10)
        input()
        page.close()

    except Exception as e:
        print(f'❌ 打开网址失败：{str(e)}')
    finally:
        # 确保Chromium进程完全退出
        try:
            page.quit()
        except:
            pass

if __name__ == '__main__':
    open_renesas_website()