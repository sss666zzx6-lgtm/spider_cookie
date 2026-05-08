from curl_cffi import requests
import os
import time
import schedule
from datetime import datetime, timedelta
from src.utils.logger import get_logger

logger = get_logger("refresh_cookie_task")

# 全局 Session 对象（保持会话）
global_session = None


def reset_session():
    """重置全局 Session（Cookie 失效时调用）"""
    global global_session
    global_session = None
    logger.info("已重置全局 Session")


# 初始化 Session（只执行一次，保持会话）
def init_session():
    cookie_str = "_ALGOLIA=anonymous-b94a6d11-3b83-4b31-9800-f3c4324764d6; nmstat=272f2b61-d302-dee8-953c-17fbb3d27624; DT=DI1GWGErz9GRd2vZEkuhiDvKg; kapa_ab_group=ai_enabled; _ga_D1706WVDQV=GS2.1.s1773297649$o7$g1$t1773297700$j9$l0$h0; accessedDocumentsFetched=1; IDT-Language=en; ren_usr_pr=0; MkHcCurrencyId=USD; cf_clearance=sLyOMvsXV3Orni3fvIUyH0GMdTXHQYfsj0Milo121eU-1773297692-1.2.1.1-B3mGEdk3fG4hI5_9UxGa4ies5BxUA88gdvG8mSR7Bov_DrIQYxH2LC3jV8z4beWYHcH6k_ZAal9tIJRyt8rPI4JqjC9bYoxQEfYW7.pIRUCTlcK_.Hz42yf5eQfyLbO8rsKGBeljIkyZ8YbI97vIsgRZKzg7SXL.P3T3guCImmwTY5JNMPpUaOrLKveHgFVZePpn7nKSCU3TDgxH36.4taEgwMls4n8BNwZBIXXuggLxrEofAXTcV8n9WWpBX8Mw; xids=1029n-gZ9gFQmKBQryiTLsjiQ; idx=eyJ6aXAiOiJERUYiLCJ2ZXIiOiIxIiwiYWxpYXMiOiJlbmNyeXB0aW9ua2V5Iiwib2lkIjoiMDBvMWNneDRvNHlBYXBZMmgzNTciLCJlbmMiOiJBMjU2R0NNIiwiYWxnIjoiZGlyIiwieHNpZCI6ImlkeDZPQTZCLVNUUjRDVUlCbGZ3R2pCLXcifQ..rHKx3EMQ88woNH6H.w4H6dMD74j_hXwC2uCNzJsTwftRwPoZRYadROxQKwu9ZurEWD8ydxBzaGpaHiYZ_BwdeGTeFHRL2np-mCgniYWBlunRQaiHe5-HvlAl_0djmhvjIzSUafgin5a1sfQzapuZJlTC5T7UJB79OKc-pg2Tj52l-5TZM5OCj01DTvPYpoC_G0vXkOF5JKU-IyK5ygvuBqfQWWxIY8yG7S9MVjOUfWKEDD0wUb75RMlcqRAGd5L3zPgwolUM3kgilAAB4Imu0Ni-Z9QaTSxmPz5zMMtSnkYqOybABMjsNftTnf15XHO44IhIseSqloXBy9DtVl4OhxGTfYl6r_xnqix4FmCCkf751bh1IfFnW2LRdnbC-RnqDUmXhccXQdHcGMqKtomp98P3JyOoutE7aktrepguVECxU_qZE1dSnG3LC-Zu_Yia2ZTuOACIA5PttspsPhE7GoIphMWyo1WeR_63rdXa639U5bYTOROaYRUs_NtvPW27FtD9OEOHGspTMjuaNAnaH_azrZcenjdoNgOzBTfziNUJoiOknL5gugQGDuxsesE0YjEcr7aprX8ZCmmr3Xe4CTXsCOhXvep2YEERDm6DituqX7GO1-uhb3FLyNFdzLi91Y1M8WzEhyEmDl77zfcnXVsBVQQDEDDW640CZgcbMcvlQn_aIEMH9r_8MVeZwVX8THRk5u8OwQFuLUU9Fa9lswNbF3quWZIGpmyrLSoc-rkcFaodBYLgCHyYtgNG9baxUATu8gDy7hpbIe3QqllZPE2hvErXfL4IL2seW2hFixYsPyv5KDcCkFK85qhWr_YKxwoHWNwwcF0LY3BBWzT_e7NB5cDicYtjwuuxQg6zvRWlaGCoTStUd_B-BQB4-O_-cFlUUS3AlxKuikGvfCwa70MoW4Sw6BBSB-fGDN4q7lnfGhOE6zWgl7PfMKG6jwsI.z7hV1YWlAKSvTV6gaKKWjw; myr=102Bxjt8k2xQbSTDVHWugleBA; idt_user_login_type=login; uid=6942801; referrer_path=/products/cl8060; notice_behavior=none; _ga=GA1.1.1401676060.1772535507; ELOQUA=GUID=7C83A6B8AC734A69877ED6FFC79B8D00; _gcl_au=1.1.2137071434.1772535507.426341254.1773297694.1773297694; MkHcLang=en; sid=102Bxjt8k2xQbSTDVHWugleBA; JSESSIONID=312E85D56041FCA75D475719AD63142E; proximity_b7b50f02d73fdbb68d58d277864c3613=eyJ6aXAiOiJERUYiLCJwMnMiOiItcnVTTWFZWlJhRk0xRWxnZmwwdW5BIiwicDJjIjoxMDAwLCJ2ZXIiOiIxIiwiZW5jIjoiQTI1NkdDTSIsImFsZyI6IlBCRVMyLUhTNTEyK0EyNTZLVyJ9.FTCbrZw82x6TM-Jy6DxnIGEoaAr3utISd_jNoNebnwqWxtwC2lBlaA.SIi5ndnku8lvcq2I.Xa7KAd5wQ8H1rhFGKZnxCS4a1-NFalBZDez0cg340aJwPLDWwxOpBHaT-W58SZiuhD-fPJwpa253nTymwkfL5fmCntasZULkdFDJ3Y5m_zKJnbb5S4hpavYbki2TqCsI5WpD6jVt8ePa1Sj0Aro6ORb_LJpTwHBD66R-BViG3aGReQ.BypzzZMmvwlbslcYxk1jzg; __cf_bm=qclzfW0rS5yWXEkB0sMW.1189eDfAjV.HyH5uVgFGOU-1773297692.560536-1.0.1.1-26rbmX5XuiWayt5t1aBlfJK30fH95OwRnh17h7un9vwbyVLbFEen7aiGNgDkTx_Tzp1jAHu3rSD4qVpPT9Os349u7PkJKqsUCBZe0eYA0zEKu4ihwEa915iqs8.nXt0d; SSESS8d786bdf64747b7f1b2e52f729beec12=24k0boqc4f4ihl523khmiiu96a"
    INITIAL_COOKIE = cookie_str
    """初始化全局 Session 对象，设置 Cookie 和 UA"""
    global global_session
    if global_session is None:
        global_session = requests.Session()
        # 设置请求头
        headers = {
            "cookie": INITIAL_COOKIE,
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36"
        }
        global_session.headers.update(headers)
        logger.info("全局 Session 初始化完成")
    return global_session


def verify_cookie(session):
    """验证 Cookie 有效性"""
    pdf_url = "https://www.renesas.com/en/document/dst/cl8060-datasheet"
    time.sleep(1)

    try:
        response = session.get(
            pdf_url,
            stream=True,  # 保持 stream=True 避免自动下载正文
            timeout=15,
            impersonate="chrome110"
        )

        response.raise_for_status()
        logger.info(f"请求成功，状态码：{response.status_code}")

        content_type = response.headers.get("Content-Type", "").lower()
        if "application/pdf" in content_type:
            logger.info("响应类型为 PDF，Cookie 有效！")
            return True
        else:
            logger.error(f"响应不是 PDF，Content-Type：{content_type}")
            logger.error(f"响应内容预览：{response.text[:200]}")
            return False

    except requests.exceptions.HTTPError as e:
        logger.error(f"HTTP 请求失败：{e}")
        return False
    except Exception as e:
        logger.error(f"请求异常：{str(e)}")
        return False


def task():
    """定时任务核心逻辑：验证 Cookie"""
    logger.info("=" * 50)
    logger.info("开始执行 1 小时一次的 Cookie 验证任务")

    # 记录任务开始时间
    start_time = datetime.now()
    logger.info(f"任务开始时间：{start_time.strftime('%Y-%m-%d %H:%M:%S')}")

    # 获取全局 Session
    session = init_session()

    # 第一步：访问 myrenesas 页面保持会话
    product_url = "https://www.renesas.com/en/myrenesas"
    try:
        response = session.get(product_url, impersonate="chrome110", timeout=15)
        logger.info(f"访问 myrenesas 状态码：{response.status_code}")
    except Exception as e:
        logger.error(f"访问 myrenesas 失败：{str(e)}")

    # 第二步：验证 Cookie 有效性
    is_valid = verify_cookie(session)

    # 如果 Cookie 失效，重置 Session 并记录日志
    if not is_valid:
        logger.warning("Cookie 验证失败，已重置 Session，下次任务将重新初始化")
        reset_session()

    # 记录任务结束时间和下次执行时间
    end_time = datetime.now()
    next_run_time = end_time + timedelta(hours=6)
    logger.info(f"任务结束时间：{end_time.strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info(f"下次执行时间：{next_run_time.strftime('%Y-%m-%d %H:%M:%S')}")

    logger.info("本次定时任务执行完成")
    logger.info("=" * 50)


if __name__ == "__main__":
    # 1. 初始化 Session
    init_session()

    # 2. 立即执行一次任务（首次启动）
    logger.info("启动定时任务，首次执行 Cookie 验证...")
    task()

    # 3. 清理原有定时任务（避免重复）
    schedule.clear()

    # 4. 配置精准的定时任务：每 1 小时执行一次
    schedule.every(1).hours.do(task)
    logger.info(f"定时任务已配置：每 1 小时执行一次 Cookie 验证")

    # 5. 打印下次执行时间（便于调试）
    next_run = schedule.next_run()
    logger.info(f"下次任务执行时间：{next_run.strftime('%Y-%m-%d %H:%M:%S')}")

    # 6. 循环执行定时任务（缩短检查间隔，提高精准度）
    while True:
        schedule.run_pending()
        # 缩短检查间隔到 1 分钟，减少时间误差
        time.sleep(60)
#         nohup python -m src.renesas_login_cookie.refresh_cookie > refresh_cookie.log 2>&1 &
