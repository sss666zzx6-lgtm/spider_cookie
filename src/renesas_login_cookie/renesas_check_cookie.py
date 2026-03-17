import os
import time
from typing import Optional

from curl_cffi import requests


def check_cookie(
    cookie: str,
    pdf_url: str,
    save_path: str,
    user_agent: str = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36",
    impersonate: str = "chrome110",
    chunk_size: int = 32 * 1024,
    verbose: bool = True
) -> bool:
    """
    使用提供的 cookie 下载 Renesas PDF 文档。

    Args:
        cookie: Cookie 字符串
        pdf_url: PDF 文档 URL
        save_path: 保存路径
        user_agent: User-Agent 字符串
        impersonate: curl_cffi 的 impersonate 参数
        chunk_size: 下载分块大小
        verbose: 是否打印日志

    Returns:
        bool: 下载成功返回 True，失败返回 False
    """
    headers = {
        "cookie": cookie,
        "user-agent": user_agent
    }

    time.sleep(1)
    try:
        response = requests.get(
            pdf_url,
            headers=headers,
            stream=True,
            impersonate=impersonate
        )
        response.raise_for_status()

        if verbose:
            print(response)
            print(response.headers.get("Content-Type", ""))

        with open(save_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=chunk_size):
                if chunk:
                    f.write(chunk)

        if os.path.getsize(save_path) > 0:
            if verbose:
                print(f"PDF 下载成功，保存路径：{os.path.abspath(save_path)}")
            return True
        else:
            if verbose:
                print("下载失败：文件为空")
            return False

    except Exception as e:
        if verbose:
            print(f"下载失败：{str(e)}")
        return False


if __name__ == '__main__':
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'renesas_cookie.txt'), 'r',
              encoding='utf-8') as f:
        cookie_str = f.read()
    pdf_url = "https://www.renesas.com/en/document/dst/cl8060-datasheet"
    save_path = "cl8060_datasheet.pdf"

    result = check_cookie(cookie_str, pdf_url, save_path)
    print(result)
