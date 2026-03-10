from curl_cffi import requests
import os
import time
import schedule
from datetime import datetime, timedelta
from util.logger import get_logger

logger = get_logger("refresh_cookie_task")

# 全局Session对象（保持会话）
global_session = None
# 初始Cookie字符串
INITIAL_COOKIE = """_ga=GA1.1.252753382.1765965542; nmstat=a954251b-a5be-60cd-bfc3-298b27c52932; ELOQUA=GUID=1D50B4A8E71F48A4B833419F9D77DC91; notice_preferences=2:; notice_gdpr_prefs=0,1,2:; cmapi_gtm_bl=; cmapi_cookie_privacy=permit 1,2,3; proximity_400d32b72c8ba6f4d4a8984df2612eb0=eyJ6aXAiOiJERUYiLCJwMnMiOiJQeEtIbzBwNEN1ZEd1OEpHUk5ubFN3IiwicDJjIjoxMDAwLCJ2ZXIiOiIxIiwiZW5jIjoiQTI1NkdDTSIsImFsZyI6IlBCRVMyLUhTNTEyK0EyNTZLVyJ9.8uI9wAYdTP69k_BayWxzxSGnF-NvZukPN83-jrXMPVgOurHnvjJf2Q.-WV_zJ2BLaGK-awQ.JjqAjdiGaCIvc-BrqWpvmGuGJ_VMXvXMev88DVqzqCs1R-7czqkkoNMw_sQx6i71sNYvXeieEk0MEtP1Esod0I9u0N8_Jm8_mjk9RWl8bli_sAzdpcn7KqBcj1STQESrg4f41yz0wZe2cOYQeNZW90fu1q6caQbY7A-ZkeD0wu4o6Q.fDSe7YHypVc-oty9kfGnJA; kapa_ab_group=ai_enabled; IDT-Language=en; MkHcLang=en; MkHcCurrencyId=USD; notice_behavior=none; _ALGOLIA=anonymous-aaa80dd9-47af-4cca-8df2-7dc6cef3b2c4; referrer_path=/products/cl8060; cf_clearance=_twoA8zP_YwmSu015QqSFQLl017vWiY7kxWTdGknYUU-1772098535-1.2.1.1-fpS.9zim4AEbn6xasCXdmPitN4diHn_oqtfS1kJeM88JsGm_KY74lQPkRNSNaWdGq7uGhuoemfuF1vB0_eBpHwVAZoCygfZm4_oyMSMHCD2Af2H1lZS7y2Ozk1cueNv5Xt2jHFbuQYdM1gaqq05QO2cGKTWwEHucwMg_S8ZafIbgxhsHkdIieH1cNo7FBVgLOt_kJAEnhtONAwiTc0BGVIE84ruVBP1mzo.maHFOSdnYEt_XYb_5I6xkeYsiRaVe; __cf_bm=fLi6ZQuxzvHRGKwZgur76YpJ3kFjhoB_ZZK2fbzki.Y-1772098535.4100564-1.0.1.1-RkYt3HTW4fAblUUTeqwi9Ip41lwXWKFa6.KspGCG8tUS7Qojt0HRTACbiGodlDFqLniN0C4zoaBwJYyQnPd_w9JSfdPj1xRecoRFwSxEGA_F9BslIfIP3F8qSjdEtdwG; myr=102xlkLUi7USzShmfvm6RTgAw; sid=102xlkLUi7USzShmfvm6RTgAw; xids=102bQdD4W2cTSK0UPJi0SyVAw; JSESSIONID=6C6D756B4741FF9CA6244362E4D4A489; idx=eyJ6aXAiOiJERUYiLCJ2ZXIiOiIxIiwiYWxpYXMiOiJlbmNyeXB0aW9ua2V5Iiwib2lkIjoiMDBvMWNneDRvNHlBYXBZMmgzNTciLCJlbmMiOiJBMjU2R0NNIiwiYWxnIjoiZGlyIiwieHNpZCI6ImlkeE9GeGdvSUxDUmZLMWozcWJjckJnX3cifQ..SuP-BMjyIYKt-uSW.Rkma2Bx4UQ1IE37q4mamhHLu-BsD6e4Fbpotw1A_aSE4oKY-qkxTeTIcxaXrU_6pCsCZ_d35QX1sahQTaXjhPGDkUenStZtKtI658AJQsQB85QLyU1Yw2DQyvoZAMeFC7M5qGXgRa2q5js4y1NLpkqs_48f_JiHbeC6VpfY-lIz3T9d-IGcFykz7V-CG6ygZfH6KiI7H00G3UVHOWXyA739mjg8JHhhCfE6YASGa2EIKhADdi7zJ67mbAcCErW8lnknaCb_cIXYAjMaV_2JJQvaqmnb1hnlryBZxF7x0ItULWdhCMGb0xSY3PihJ6jaOv_UKvgahPj0CRXu30GD4W4kJqjnIeYXYRUpIlN7SMroHVnv_wmREZxb7FV3pbDsTlg9XtbVNMspwznoJHllZ_JSdS2-2pdqEzU9xo3_9YX6FSzeaSZvIpVf1JoEGbdQLdm_ZYtgjysvyMUOhjcxDzI2ks3gEwS33ljDV8Uxrnkr_gI2kAiRu4glL3lI3l33mwUQ0IHSHzg-Xb4pMZJyFWG9mIKtmVoCQcqy1HaojJdjsWQ2ZYVBflMqME0e-UmrhT62pWzhyoKnQFCzY5EQmueSYqSoethVOH0auI6Y2WbkcwAUUTm99CGRqGmEtYBRvkjchXN-8A23jbCrwdoFl5AKblYMVFfDbMfrEi4mzQODfiR01BZrtCvRGSNgrZCQqeVhv0ubHVmyorjuHp64nySZQhk33A1x7pif-B475f-EcHeeblohR8R-Qc0zlZgyY6JR0vkwRnLZi6XDpCg-dXYghjLBHAjP4NwXqSlOx7q31O6ACm89R9BGHyQTbhlwXcM3WIoTAkJpVW9FWcGLzrwfA6x14NdK-D8TqX4bBhONA7OuHtezhB-BThMSLLMtOJiYABvCWeSjtJ2xJzFBOxt37r3RGUjZIJaDk2fsgGg.a870M8iz42gPISAJhdCb2A; DT=DI1YNSifo2FS_amdXGagi59Lg; proximity_b7b50f02d73fdbb68d58d277864c3613=eyJ6aXAiOiJERUYiLCJwMnMiOiJqR3F1OFBpUkh6STNrRHRpc2ExNDdnIiwicDJjIjoxMDAwLCJ2ZXIiOiIxIiwiZW5jIjoiQTI1NkdDTSIsImFsZyI6IlBCRVMyLUhTNTEyK0EyNTZLVyJ9.NBYxCCDi_lWNTpsU1P-tuooNmArbQLKpmCN0lPMfDDfKOZ-v9Mhn1A.MaXQaS6bpIalpYbD.Tn-cE8evS607pwMpNOEOxWUsluqDF_ziiCuMnrOqV7V_ysFwk7EXFjFhgtA0pEpd6NzONGHEuY21IRy3GueBiX0jHLKsS1_EYllxZVVXWLZYxJv0roySt1judxIAI7ph0XVLb4mmuK0JTqcXlt5YjujJyf84hX7vPjI1S5hq8wSk_w.cW4y2TIPaci5tK_i1mafmg; SSESS8d786bdf64747b7f1b2e52f729beec12=l7eb36ksh3tfk9l0squs0um3ph; ren_usr_pr=0; uid=6942801; _gcl_au=1.1.299705081.1765965542.1089777303.1771997877.1771998993; accessedDocumentsFetched=1; _ga_D1706WVDQV=GS2.1.s1772096739$o70$g1$t1772098557$j57$l0$h0"""


# 初始化Session（只执行一次，保持会话）
def init_session():
    """初始化全局Session对象，设置Cookie和UA"""
    global global_session
    if global_session is None:
        global_session = requests.Session()
        # 设置请求头
        headers = {
            "cookie": INITIAL_COOKIE,
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36"
        }
        global_session.headers.update(headers)
        logger.info("全局Session初始化完成")
    return global_session


def verify_cookie(session):
    """验证Cookie有效性"""
    pdf_url = "https://www.renesas.com/en/document/dst/cl8060-datasheet"
    time.sleep(1)

    try:
        response = session.get(
            pdf_url,
            stream=True,  # 保持stream=True避免自动下载正文
            timeout=15,
            impersonate="chrome110"
        )

        response.raise_for_status()
        logger.info(f"请求成功，状态码：{response.status_code}")

        content_type = response.headers.get("Content-Type", "").lower()
        if "application/pdf" in content_type:
            logger.info("响应类型为PDF，Cookie有效！")
            return True
        else:
            logger.error(f"响应不是PDF，Content-Type：{content_type}")
            logger.error(f"响应内容预览：{response.text[:200]}")
            return False

    except requests.exceptions.HTTPError as e:
        logger.error(f"HTTP请求失败：{e}")
        return False
    except Exception as e:
        logger.error(f"请求异常：{str(e)}")
        return False


def task():
    """定时任务核心逻辑：验证Cookie"""
    logger.info("=" * 50)
    logger.info("开始执行6小时一次的Cookie验证任务")

    # 记录任务开始时间
    start_time = datetime.now()
    logger.info(f"任务开始时间：{start_time.strftime('%Y-%m-%d %H:%M:%S')}")

    # 获取全局Session
    session = init_session()

    # 第一步：访问myrenesas页面保持会话
    product_url = "https://www.renesas.com/en/myrenesas"
    try:
        response = session.get(product_url, impersonate="chrome110", timeout=15)
        logger.info(f"访问myrenesas状态码：{response.status_code}")
    except Exception as e:
        logger.error(f"访问myrenesas失败：{str(e)}")

    # 第二步：验证Cookie有效性
    is_valid = verify_cookie(session)

    # 记录任务结束时间和下次执行时间
    end_time = datetime.now()
    next_run_time = end_time + timedelta(hours=6)
    logger.info(f"任务结束时间：{end_time.strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info(f"下次执行时间：{next_run_time.strftime('%Y-%m-%d %H:%M:%S')}")

    logger.info("本次定时任务执行完成")
    logger.info("=" * 50)


if __name__ == "__main__":
    # 1. 初始化Session
    init_session()

    # 2. 立即执行一次任务（首次启动）
    logger.info("启动定时任务，首次执行Cookie验证...")
    task()

    # 3. 清理原有定时任务（避免重复）
    schedule.clear()

    # 4. 配置精准的定时任务：每6小时执行一次
    schedule.every(6).hours.do(task)
    logger.info(f"定时任务已配置：每6小时执行一次Cookie验证")

    # 5. 打印下次执行时间（便于调试）
    next_run = schedule.next_run()
    logger.info(f"下次任务执行时间：{next_run.strftime('%Y-%m-%d %H:%M:%S')}")

    # 6. 循环执行定时任务（缩短检查间隔，提高精准度）
    while True:
        schedule.run_pending()
        # 缩短检查间隔到1分钟，减少时间误差
        time.sleep(60)



#
# from curl_cffi import requests
# import time
# from datetime import datetime, timedelta
# from apscheduler.schedulers.background import BackgroundScheduler  # 核心：改用APScheduler
# from apscheduler.triggers.interval import IntervalTrigger
# from util.logger import get_logger
#
# logger = get_logger("refresh_cookie_task")
#
# # 全局Session对象（保持会话）
# global_session = None
# # 初始Cookie字符串
# INITIAL_COOKIE = """_ga=GA1.1.252753382.1765965542; nmstat=a954251b-a5be-60cd-bfc3-298b27c52932; ELOQUA=GUID=1D50B4A8E71F48A4B833419F9D77DC91; notice_preferences=2:; notice_gdpr_prefs=0,1,2:; cmapi_gtm_bl=; cmapi_cookie_privacy=permit 1,2,3; proximity_400d32b72c8ba6f4d4a8984df2612eb0=eyJ6aXAiOiJERUYiLCJwMnMiOiJQeEtIbzBwNEN1ZEd1OEpHUk5ubFN3IiwicDJjIjoxMDAwLCJ2ZXIiOiIxIiwiZW5jIjoiQTI1NkdDTSIsImFsZyI6IlBCRVMyLUhTNTEyK0EyNTZLVyJ9.8uI9wAYdTP69k_BayWxzxSGnF-NvZukPN83-jrXMPVgOurHnvjJf2Q.-WV_zJ2BLaGK-awQ.JjqAjdiGaCIvc-BrqWpvmGuGJ_VMXvXMev88DVqzqCs1R-7czqkkoNMw_sQx6i71sNYvXeieEk0MEtP1Esod0I9u0N8_Jm8_mjk9RWl8bli_sAzdpcn7KqBcj1STQESrg4f41yz0wZe2cOYQeNZW90fu1q6caQbY7A-ZkeD0wu4o6Q.fDSe7YHypVc-oty9kfGnJA; kapa_ab_group=ai_enabled; IDT-Language=en; MkHcLang=en; MkHcCurrencyId=USD; notice_behavior=none; _ALGOLIA=anonymous-aaa80dd9-47af-4cca-8df2-7dc6cef3b2c4; referrer_path=/products/cl8060; cf_clearance=_twoA8zP_YwmSu015QqSFQLl017vWiY7kxWTdGknYUU-1772098535-1.2.1.1-fpS.9zim4AEbn6xasCXdmPitN4diHn_oqtfS1kJeM88JsGm_KY74lQPkRNSNaWdGq7uGhuoemfuF1vB0_eBpHwVAZoCygfZm4_oyMSMHCD2Af2H1lZS7y2Ozk1cueNv5Xt2jHFbuQYdM1gaqq05QO2cGKTWwEHucwMg_S8ZafIbgxhsHkdIieH1cNo7FBVgLOt_kJAEnhtONAwiTc0BGVIE84ruVBP1mzo.maHFOSdnYEt_XYb_5I6xkeYsiRaVe; __cf_bm=fLi6ZQuxzvHRGKwZgur76YpJ3kFjhoB_ZZK2fbzki.Y-1772098535.4100564-1.0.1.1-RkYt3HTW4fAblUUTeqwi9Ip41lwXWKFa6.KspGCG8tUS7Qojt0HRTACbiGodlDFqLniN0C4zoaBwJYyQnPd_w9JSfdPj1xRecoRFwSxEGA_F9BslIfIP3F8qSjdEtdwG; myr=102xlkLUi7USzShmfvm6RTgAw; sid=102xlkLUi7USzShmfvm6RTgAw; xids=102bQdD4W2cTSK0UPJi0SyVAw; JSESSIONID=6C6D756B4741FF9CA6244362E4D4A489; idx=eyJ6aXAiOiJERUYiLCJ2ZXIiOiIxIiwiYWxpYXMiOiJlbmNyeXB0aW9ua2V5Iiwib2lkIjoiMDBvMWNneDRvNHlBYXBZMmgzNTciLCJlbmMiOiJBMjU2R0NNIiwiYWxnIjoiZGlyIiwieHNpZCI6ImlkeE9GeGdvSUxDUmZLMWozcWJjckJnX3cifQ..SuP-BMjyIYKt-uSW.Rkma2Bx4UQ1IE37q4mamhHLu-BsD6e4Fbpotw1A_aSE4oKY-qkxTeTIcxaXrU_6pCsCZ_d35QX1sahQTaXjhPGDkUenStZtKtI658AJQsQB85QLyU1Yw2DQyvoZAMeFC7M5qGXgRa2q5js4y1NLpkqs_48f_JiHbeC6VpfY-lIz3T9d-IGcFykz7V-CG6ygZfH6KiI7H00G3UVHOWXyA739mjg8JHhhCfE6YASGa2EIKhADdi7zJ67mbAcCErW8lnknaCb_cIXYAjMaV_2JJQvaqmnb1hnlryBZxF7x0ItULWdhCMGb0xSY3PihJ6jaOv_UKvgahPj0CRXu30GD4W4kJqjnIeYXYRUpIlN7SMroHVnv_wmREZxb7FV3pbDsTlg9XtbVNMspwznoJHllZ_JSdS2-2pdqEzU9xo3_9YX6FSzeaSZvIpVf1JoEGbdQLdm_ZYtgjysvyMUOhjcxDzI2ks3gEwS33ljDV8Uxrnkr_gI2kAiRu4glL3lI3l33mwUQ0IHSHzg-Xb4pMZJyFWG9mIKtmVoCQcqy1HaojJdjsWQ2ZYVBflMqME0e-UmrhT62pWzhyoKnQFCzY5EQmueSYqSoethVOH0auI6Y2WbkcwAUUTm99CGRqGmEtYBRvkjchXN-8A23jbCrwdoFl5AKblYMVFfDbMfrEi4mzQODfiR01BZrtCvRGSNgrZCQqeVhv0ubHVmyorjuHp64nySZQhk33A1x7pif-B475f-EcHeeblohR8R-Qc0zlZgyY6JR0vkwRnLZi6XDpCg-dXYghjLBHAjP4NwXqSlOx7q31O6ACm89R9BGHyQTbhlwXcM3WIoTAkJpVW9FWcGLzrwfA6x14NdK-D8TqX4bBhONA7OuHtezhB-BThMSLLMtOJiYABvCWeSjtJ2xJzFBOxt37r3RGUjZIJaDk2fsgGg.a870M8iz42gPISAJhdCb2A; DT=DI1YNSifo2FS_amdXGagi59Lg; proximity_b7b50f02d73fdbb68d58d277864c3613=eyJ6aXAiOiJERUYiLCJwMnMiOiJqR3F1OFBpUkh6STNrRHRpc2ExNDdnIiwicDJjIjoxMDAwLCJ2ZXIiOiIxIiwiZW5jIjoiQTI1NkdDTSIsImFsZyI6IlBCRVMyLUhTNTEyK0EyNTZLVyJ9.NBYxCCDi_lWNTpsU1P-tuooNmArbQLKpmCN0lPMfDDfKOZ-v9Mhn1A.MaXQaS6bpIalpYbD.Tn-cE8evS607pwMpNOEOxWUsluqDF_ziiCuMnrOqV7V_ysFwk7EXFjFhgtA0pEpd6NzONGHEuY21IRy3GueBiX0jHLKsS1_EYllxZVVXWLZYxJv0roySt1judxIAI7ph0XVLb4mmuK0JTqcXlt5YjujJyf84hX7vPjI1S5hq8wSk_w.cW4y2TIPaci5tK_i1mafmg; SSESS8d786bdf64747b7f1b2e52f729beec12=l7eb36ksh3tfk9l0squs0um3ph; ren_usr_pr=0; uid=6942801; _gcl_au=1.1.299705081.1765965542.1089777303.1771997877.1771998993; accessedDocumentsFetched=1; _ga_D1706WVDQV=GS2.1.s1772096739$o70$g1$t1772098557$j57$l0$h0"""
#
#
# # 初始化Session（只执行一次，保持会话）
# def init_session():
#     """初始化全局Session对象，设置Cookie和UA"""
#     global global_session
#     if global_session is None:
#         global_session = requests.Session()
#         # 设置请求头
#         headers = {
#             "cookie": INITIAL_COOKIE,
#             "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36"
#         }
#         global_session.headers.update(headers)
#         logger.info("全局Session初始化完成")
#     return global_session
#
#
# def verify_cookie(session):
#     """验证Cookie有效性"""
#     pdf_url = "https://www.renesas.com/en/document/dst/cl8060-datasheet"
#     time.sleep(1)
#
#     try:
#         response = session.get(
#             pdf_url,
#             stream=True,  # 保持stream=True避免自动下载正文
#             timeout=15,
#             impersonate="chrome110"
#         )
#
#         response.raise_for_status()
#         logger.info(f"请求成功，状态码：{response.status_code}")
#
#         content_type = response.headers.get("Content-Type", "").lower()
#         if "application/pdf" in content_type:
#             logger.info("响应类型为PDF，Cookie有效！")
#             return True
#         else:
#             logger.error(f"响应不是PDF，Content-Type：{content_type}")
#             logger.error(f"响应内容预览：{response.text[:200]}")
#             return False
#
#     except requests.exceptions.HTTPError as e:
#         logger.error(f"HTTP请求失败：{e}")
#         return False
#     except Exception as e:
#         logger.error(f"请求异常：{str(e)}")
#         return False
#
#
# def task():
#     """定时任务核心逻辑：验证Cookie"""
#     logger.info("=" * 50)
#     logger.info("开始执行6小时一次的Cookie验证任务")
#
#     # 记录任务开始时间
#     start_time = datetime.now()
#     logger.info(f"任务开始时间：{start_time.strftime('%Y-%m-%d %H:%M:%S')}")
#
#     # 获取全局Session
#     session = init_session()
#
#     # 第一步：访问myrenesas页面保持会话
#     product_url = "https://www.renesas.com/en/myrenesas"
#     try:
#         response = session.get(product_url, impersonate="chrome110", timeout=15)
#         logger.info(f"访问myrenesas状态码：{response.status_code}")
#     except Exception as e:
#         logger.error(f"访问myrenesas失败：{str(e)}")
#
#     # 第二步：验证Cookie有效性
#     verify_cookie(session)
#
#     # 记录任务结束时间和下次执行时间
#     end_time = datetime.now()
#     next_run_time = end_time + timedelta(hours=6)
#     logger.info(f"任务结束时间：{end_time.strftime('%Y-%m-%d %H:%M:%S')}")
#     logger.info(f"下次执行时间：{next_run_time.strftime('%Y-%m-%d %H:%M:%S')}")
#
#     logger.info("本次定时任务执行完成")
#     logger.info("=" * 50)
#
#
# if __name__ == "__main__":
#     # 1. 初始化Session
#     init_session()
#
#     # 2. 立即执行一次任务（首次启动）
#     logger.info("启动定时任务，首次执行Cookie验证...")
#     task()
#
#     # 3. 配置APScheduler（工业级定时任务）
#     # 核心：使用后台调度器，避免阻塞主线程
#     scheduler = BackgroundScheduler(timezone="Asia/Shanghai")  # 指定时区，避免时间偏移
#     # 添加间隔任务：每6小时执行一次，从首次任务完成后开始计算
#     scheduler.add_job(
#         task,
#         trigger=IntervalTrigger(hours=6),  # 严格的6小时间隔
#         id="cookie_verify_task",
#         replace_existing=True,  # 替换已存在的任务，避免重复
#         misfire_grace_time=300  # 允许5分钟的执行误差（避免轻微延迟导致任务跳过）
#     )
#
#     # 启动调度器
#     scheduler.start()
#     logger.info("APScheduler定时任务已启动，每6小时执行一次Cookie验证")
#
#     # 打印下次执行时间
#     next_job = scheduler.get_job("cookie_verify_task")
#     if next_job:
#         logger.info(f"下次任务执行时间：{next_job.next_run_time.strftime('%Y-%m-%d %H:%M:%S')}")
#
#     # 保持程序运行（捕获退出信号，优雅关闭）
#     try:
#         while True:
#             time.sleep(3600)  # 主线程休眠1小时，减少资源占用
#     except (KeyboardInterrupt, SystemExit):
#         # 收到终止信号时，关闭调度器
#         scheduler.shutdown()
#         logger.info("定时任务调度器已优雅关闭")