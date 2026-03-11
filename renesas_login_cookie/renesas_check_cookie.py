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
    # 示例用法
    cookie = """referrer_path=/products/cl8060; xids=102rs8gkr4BSFeulQ7wLMVYtw; SSESS8d786bdf64747b7f1b2e52f729beec12=hbi7tegk0tdqf5bem24f2ebm8d; idx=eyJ6aXAiOiJERUYiLCJ2ZXIiOiIxIiwiYWxpYXMiOiJlbmNyeXB0aW9ua2V5Iiwib2lkIjoiMDBvMWNneDRvNHlBYXBZMmgzNTciLCJlbmMiOiJBMjU2R0NNIiwiYWxnIjoiZGlyIiwieHNpZCI6ImlkeDdsS19zWV9LU2FtVlJLcEd4TnQySUEifQ..b-a9tAEL8NJ0smt6.f-DXby8kekElu7nafcafXXDvjOcFvwL-NJ3z5iu1CMwwd7wbSNeIkvUgx2B1LSjpmf43whTv8uMwaqZq8rfFG_CfH_XZWm--8v8FG77Hn6pwkHd--HC66LRF_yFnk7hFaVKWkEjCV-2zqlPnT2a3pofYnbHqmabDhPmodN-WazCDKBf26PD8lype-dwSlXJwUd-DysXXr3ItpEp7YjJRpYtixZU5CSLdOEoToiS3gGxJnrm2xX1AKuNphoQQdUr40IezuZ2QU86AGzhm9FvW7TWkk1BYPPdULcqZXw3Ohh9o1hUASCVVDxS-WBIZKtINj9Z-gcgz5yPogsZBviFs_-GQdzX95s2Z-qPBXGWESjdxhLTWhLQs6lVV4kKG9PHfMlXwKE7nOz3Ht7q5OE12kdGK1QCWPCs4Amt9VXeUAlq3kGIdTKGeLTFahWicVyb6iHicakh-SGvv3EYj_0V2jRhDC_n9V7YYneB2vtWnjUgcA68JQPuKbQ8Rqj8V2is4-PiW4GX7XSWtpCvtCxFclcEyGTz3cxZ3ZDF0HQxEGaaLRRKyBxuXgJ4cGJVCsLpoiiUIPbfrTHrYMZBAXdE1hEPD0DZi1oK5Pr0tZIR6tj4gy4QHWMcEyfRubS3aeKv_EsQurNgKgfOgKf3ix85KbH9pphZmyxeEWMr9hf-n5WzXDMA7mu8dlah42QwPeJZKce2j2vXTToIFWsej7qt2ZoQaKql_XSRtS7Eu3UIt6rvXVQLan6TjmzPoDee5Cr7NpqvsBr0WJFkOtLSqd8t-yj-dgTSXmZ5axzm5OSeV2-m4huXatkG8SKm23I80X2LTD3aghfy5XIJux8dOHoH9r9F8sVVukvPskzipMcjQcJvxJvmrAK2NZ5BMZ_qSGhOoTDScTmWmC3l7XGn2l2NS5PZNa0BSFoJz_cC6tWAouFLe.B-fyqYDObPuNLsEHlHttHQ; JSESSIONID=25F85EC18E1BDAA798DBADD05929F227; myr=102dn5nIV7aSSS410DyiWmyDQ; _gcl_au=1.1.2137071434.1772535507.428395886.1773213625.1773213625; ren_usr_pr=0; idt_user_login_type=login; kapa_ab_group=ai_enabled; __cf_bm=4u.zB1LBGUla91ivdyYZ47uXQq9KzKYxZqPmVqR0V4o-1773213619.263809-1.0.1.1-4xvdjrUf17lFI3toxwaVa153OJ6T2WxxUMJD7h.0f41npZsycViqvKoBuLBRKCxuXxQL4kcytRxPboUUexZTuwcYk.nvcXnWvGoITttF1ehufWapIoWcCEFVKzPdDvJL; MkHcCurrencyId=USD; notice_behavior=none; DT=DI10W3RvZRgTP6cYVd2KwXgcg; IDT-Language=en; _ga_D1706WVDQV=GS2.1.s1773213529$o5$g1$t1773213635$j39$l0$h0; proximity_b7b50f02d73fdbb68d58d277864c3613=eyJ6aXAiOiJERUYiLCJwMnMiOiJQVmljb0FYcnhhdlZnbDlMbzBBaEJ3IiwicDJjIjoxMDAwLCJ2ZXIiOiIxIiwiZW5jIjoiQTI1NkdDTSIsImFsZyI6IlBCRVMyLUhTNTEyK0EyNTZLVyJ9.GIcXhN4bmViq9t0Kp6WofGA97d_YbeMSTanpTujcsK53Ke1hr1f0SA.3aWUqDhkBjSBXoMp.i9NTqmszM2Kr0LCS_7jyLPT6rMVNAfm1EyFRQGJuffd9-6dmia1XCURGVFaThpj0LIAjbyj7N3lSsEKkK_p9MdaEDYwfsXzjS6OgPg3Rnhobnu4LiY9lYzX7TBGxDc_jvQ_hn7jBPrqR18X1qYVIr-_MzwIfGs82g_YSY7VBm6_dpQ.1N5k7RTofb8f7zOlgjAeFg; _ALGOLIA=anonymous-6650e843-3b71-4ab6-96c9-5788ce9ab299; cf_chl_rc_ni=1; cf_clearance=WaXAn8BWaXmpStbJOxgy.xjv6eP_fgnMZNeuHAN8aH8-1773213619-1.2.1.1-AItUy3oEGc2.1jz3GA3vJGor7bo5.E1stetCK0atOmXUvApOHqodD_.D..d141LoGn_kwbEb_uQ8VD4l.i.acgkxXq402FzgJ0pqrcoty.bFji25lOZER__JPm6P5DWA9lqcFx0dsAy5rMe5WYZKLAvNegT0zErwTU0ouweghDq9kcNLWUBTydq9Z4byNwOodNqUSv5fXwkMst3PmZ6dmdn__XTEoheicGgGnVbxjORtikvad7NgRC5MshIXsVab; uid=6942801; sid=102dn5nIV7aSSS410DyiWmyDQ; ELOQUA=GUID=7C83A6B8AC734A69877ED6FFC79B8D00; MkHcLang=en; _ga=GA1.1.1401676060.1772535507; nmstat=272f2b61-d302-dee8-953c-17fbb3d27624"""
    pdf_url = "https://www.renesas.com/en/document/dst/cl8060-datasheet"
    save_path = "cl8060_datasheet.pdf"

    result = check_cookie(cookie, pdf_url, save_path)
    print(result)
