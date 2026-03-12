from playwright.sync_api import sync_playwright
import os

# 手动指定完整 Chromium 的路径（下载成功的目录）
chromium_path = os.path.expanduser("~/.cache/ms-playwright/chromium-1208/chrome-linux64/chrome")

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=True,
        args=['--no-sandbox', '--disable-gpu', '--disable-dev-shm-usage'],
        executable_path=chromium_path  # 强制用完整 Chromium
    )
    print('✅ 浏览器启动成功！')
    browser.close()