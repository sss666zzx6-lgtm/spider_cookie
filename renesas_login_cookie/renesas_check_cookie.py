import os
import time
import requests
from curl_cffi import requests

headers = {
    "cookie": """_ga=GA1.1.252753382.1765965542; nmstat=a954251b-a5be-60cd-bfc3-298b27c52932; ELOQUA=GUID=1D50B4A8E71F48A4B833419F9D77DC91; notice_preferences=2:; notice_gdpr_prefs=0,1,2:; cmapi_gtm_bl=; cmapi_cookie_privacy=permit 1,2,3; proximity_400d32b72c8ba6f4d4a8984df2612eb0=eyJ6aXAiOiJERUYiLCJwMnMiOiJQeEtIbzBwNEN1ZEd1OEpHUk5ubFN3IiwicDJjIjoxMDAwLCJ2ZXIiOiIxIiwiZW5jIjoiQTI1NkdDTSIsImFsZyI6IlBCRVMyLUhTNTEyK0EyNTZLVyJ9.8uI9wAYdTP69k_BayWxzxSGnF-NvZukPN83-jrXMPVgOurHnvjJf2Q.-WV_zJ2BLaGK-awQ.JjqAjdiGaCIvc-BrqWpvmGuGJ_VMXvXMev88DVqzqCs1R-7czqkkoNMw_sQx6i71sNYvXeieEk0MEtP1Esod0I9u0N8_Jm8_mjk9RWl8bli_sAzdpcn7KqBcj1STQESrg4f41yz0wZe2cOYQeNZW90fu1q6caQbY7A-ZkeD0wu4o6Q.fDSe7YHypVc-oty9kfGnJA; kapa_ab_group=ai_enabled; IDT-Language=en; MkHcLang=en; MkHcCurrencyId=USD; notice_behavior=none; _ALGOLIA=anonymous-aaa80dd9-47af-4cca-8df2-7dc6cef3b2c4; referrer_path=/products/cl8060; cf_clearance=_twoA8zP_YwmSu015QqSFQLl017vWiY7kxWTdGknYUU-1772098535-1.2.1.1-fpS.9zim4AEbn6xasCXdmPitN4diHn_oqtfS1kJeM88JsGm_KY74lQPkRNSNaWdGq7uGhuoemfuF1vB0_eBpHwVAZoCygfZm4_oyMSMHCD2Af2H1lZS7y2Ozk1cueNv5Xt2jHFbuQYdM1gaqq05QO2cGKTWwEHucwMg_S8ZafIbgxhsHkdIieH1cNo7FBVgLOt_kJAEnhtONAwiTc0BGVIE84ruVBP1mzo.maHFOSdnYEt_XYb_5I6xkeYsiRaVe; __cf_bm=fLi6ZQuxzvHRGKwZgur76YpJ3kFjhoB_ZZK2fbzki.Y-1772098535.4100564-1.0.1.1-RkYt3HTW4fAblUUTeqwi9Ip41lwXWKFa6.KspGCG8tUS7Qojt0HRTACbiGodlDFqLniN0C4zoaBwJYyQnPd_w9JSfdPj1xRecoRFwSxEGA_F9BslIfIP3F8qSjdEtdwG; myr=102xlkLUi7USzShmfvm6RTgAw; sid=102xlkLUi7USzShmfvm6RTgAw; xids=102bQdD4W2cTSK0UPJi0SyVAw; JSESSIONID=6C6D756B4741FF9CA6244362E4D4A489; idx=eyJ6aXAiOiJERUYiLCJ2ZXIiOiIxIiwiYWxpYXMiOiJlbmNyeXB0aW9ua2V5Iiwib2lkIjoiMDBvMWNneDRvNHlBYXBZMmgzNTciLCJlbmMiOiJBMjU2R0NNIiwiYWxnIjoiZGlyIiwieHNpZCI6ImlkeE9GeGdvSUxDUmZLMWozcWJjckJnX3cifQ..SuP-BMjyIYKt-uSW.Rkma2Bx4UQ1IE37q4mamhHLu-BsD6e4Fbpotw1A_aSE4oKY-qkxTeTIcxaXrU_6pCsCZ_d35QX1sahQTaXjhPGDkUenStZtKtI658AJQsQB85QLyU1Yw2DQyvoZAMeFC7M5qGXgRa2q5js4y1NLpkqs_48f_JiHbeC6VpfY-lIz3T9d-IGcFykz7V-CG6ygZfH6KiI7H00G3UVHOWXyA739mjg8JHhhCfE6YASGa2EIKhADdi7zJ67mbAcCErW8lnknaCb_cIXYAjMaV_2JJQvaqmnb1hnlryBZxF7x0ItULWdhCMGb0xSY3PihJ6jaOv_UKvgahPj0CRXu30GD4W4kJqjnIeYXYRUpIlN7SMroHVnv_wmREZxb7FV3pbDsTlg9XtbVNMspwznoJHllZ_JSdS2-2pdqEzU9xo3_9YX6FSzeaSZvIpVf1JoEGbdQLdm_ZYtgjysvyMUOhjcxDzI2ks3gEwS33ljDV8Uxrnkr_gI2kAiRu4glL3lI3l33mwUQ0IHSHzg-Xb4pMZJyFWG9mIKtmVoCQcqy1HaojJdjsWQ2ZYVBflMqME0e-UmrhT62pWzhyoKnQFCzY5EQmueSYqSoethVOH0auI6Y2WbkcwAUUTm99CGRqGmEtYBRvkjchXN-8A23jbCrwdoFl5AKblYMVFfDbMfrEi4mzQODfiR01BZrtCvRGSNgrZCQqeVhv0ubHVmyorjuHp64nySZQhk33A1x7pif-B475f-EcHeeblohR8R-Qc0zlZgyY6JR0vkwRnLZi6XDpCg-dXYghjLBHAjP4NwXqSlOx7q31O6ACm89R9BGHyQTbhlwXcM3WIoTAkJpVW9FWcGLzrwfA6x14NdK-D8TqX4bBhONA7OuHtezhB-BThMSLLMtOJiYABvCWeSjtJ2xJzFBOxt37r3RGUjZIJaDk2fsgGg.a870M8iz42gPISAJhdCb2A; DT=DI1YNSifo2FS_amdXGagi59Lg; proximity_b7b50f02d73fdbb68d58d277864c3613=eyJ6aXAiOiJERUYiLCJwMnMiOiJqR3F1OFBpUkh6STNrRHRpc2ExNDdnIiwicDJjIjoxMDAwLCJ2ZXIiOiIxIiwiZW5jIjoiQTI1NkdDTSIsImFsZyI6IlBCRVMyLUhTNTEyK0EyNTZLVyJ9.NBYxCCDi_lWNTpsU1P-tuooNmArbQLKpmCN0lPMfDDfKOZ-v9Mhn1A.MaXQaS6bpIalpYbD.Tn-cE8evS607pwMpNOEOxWUsluqDF_ziiCuMnrOqV7V_ysFwk7EXFjFhgtA0pEpd6NzONGHEuY21IRy3GueBiX0jHLKsS1_EYllxZVVXWLZYxJv0roySt1judxIAI7ph0XVLb4mmuK0JTqcXlt5YjujJyf84hX7vPjI1S5hq8wSk_w.cW4y2TIPaci5tK_i1mafmg; SSESS8d786bdf64747b7f1b2e52f729beec12=l7eb36ksh3tfk9l0squs0um3ph; ren_usr_pr=0; uid=6942801; _gcl_au=1.1.299705081.1765965542.1089777303.1771997877.1771998993; accessedDocumentsFetched=1; _ga_D1706WVDQV=GS2.1.s1772096739$o70$g1$t1772098557$j57$l0$h0""",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36"
}
cookies = {
    "kapa_ab_group": "control",
    "nmstat": "16dce3a3-2c23-15d2-1e61-a1736d3b5475",
    "ELOQUA": "GUID=D5880C96D8114262829A97FB0D0A1FD9",
    "ren_usr_pr": "0",
    "notice_preferences": "2:",
    "notice_gdpr_prefs": "0,1,2:",
    "cmapi_gtm_bl": "",
    "cmapi_cookie_privacy": "permit 1,2,3",
    "_ga": "GA1.1.252753382.1765965542",
    "IDT-Language": "zh",
    "MkHcLang": "zh-CN",
    "MkHcCurrencyId": "USD",
    "notice_behavior": "expressed,eu",
    "_ALGOLIA": "anonymous-3755666a-0b13-482f-bee3-4cef80c7daa9",
    "Hm_lvt_b99db6af50ce7be250cabdfa36f447da": "1768273379,1768464776,1768541212,1770721347",
    "HMACCOUNT": "045E38B63DFCF0FA",
    "_clck": "6prpxc%5E2%5Eg3h%5E0%5E2206",
    "ELQCOUNTRY": "CN",
    "_ga_5JDBBP5TWD": "GS2.1.s1770782282$o1$g0$t1770782282$j60$l0$h0",
    "currentpath": "/zh/support/document-search",
    "TAsessionID": "26ebf285-c4f6-4d81-a85c-652c04bcc592|EXISTING",
    "_gcl_au": "1.1.299705081.1765965542.427803347.1770788128.1770788127",
    "myr": "102-jzEmU6KS1Su-yw8-ovthw",
    "sid": "102-jzEmU6KS1Su-yw8-ovthw",
    "xids": "1021VJyYq3NQ0iwz8Qh700dPw",
    "JSESSIONID": "9F504AC50571D676D2CAE9D93EC72EDF",
    "idx": "eyJ6aXAiOiJERUYiLCJ2ZXIiOiIxIiwiYWxpYXMiOiJlbmNyeXB0aW9ua2V5Iiwib2lkIjoiMDBvMWNneDRvNHlBYXBZMmgzNTciLCJlbmMiOiJBMjU2R0NNIiwiYWxnIjoiZGlyIiwieHNpZCI6ImlkeG4wcUgxcXFCVHFHdlNuMXB1anI4Y3cifQ..3hGujvolnYGimcd0.YjtQD3Ql3EDFZVAhufXurC3l9s4UtIQIqffvU1MF8E3QvEmQJPgi4Y09xAMuFPOZN09-3GPrpjmiek9DnrM9C9ixWgU_PQSJeRnIfKbhQmKYe1hZF9VXjCWn5PLvt7M_vv2njSiXzE-xxIQCXaMmAKArJiIgkMHvSLA7uvZc8r4dC3cLLfZiNDnw4_5BjYVU0DCsjIofUsaZU2B4mUjk-Pf1H6Z3dNWgZmDlIAL4pjcbWTS3UGHii4xLPjYeL1qDce_sLIi6uOzYhmrYG7BSx95ZdYvRV6UHYBnHKwqLMNpM1-NUA9NqbYHZcxv9VU7hbufkbRB59-rBh31eyfOqVpKCC_zlAdiW3CvEZM_0jGsqWXz1zSEj7fDi8Ya3SpqwEPV2AtBWcIYf-UgNEiO0yB6xq64qFeN89YoKZXv1EbzsQ-PvMRubues_GgYOz8cyRGk5eyMIzRx_MN-wai2FNRhW0Cmj40MZ4tI8XNglNQR8bWtX7wdvqeKJVRJoUZceiQM6Rx5Mzageyl4CnYaRth6Q0gNXkgtBhsdPNdje3vXTo5sY1uRaRl7SLtpNMD7CQR5mFQF8Zw0g9bDv4o-eTgZopAVlxE2RFF0YyO1hxLQN7x4GmXpGXl2f50GuwZFxtuoToVpV-XMxgVSkNG__cxX40aLd9giHoxfrfz2Y0K0xUiXDFisMIeysSfxesRct_SupjV1ORvsWHVU4HiSCxJUwkWXP2cxlu-ZlgGIPjWuG33ClNTMKJKdjIpjn-NeSZNSw9OlxOWLvZb6anWQH4QQzuU2ZWvt5xkztbz-EYGddHpp6KiiPvMzfXr3tVcBj_nL2Is_ajBT0dIDGmWisoxQPa6A98y3A2Krm1DP8UWWz86M3qQ7AQLzJWpd_2_HFP2KZoU-gV6_7PkiGmw595slwFwJLYGqVr1uzpDHkwvbbnA.pW91hHCtXClXXixCRdc-Lg",
    "DT": "DI1pIJ833EcQO22y7M2l60c4Q",
    "proximity_400d32b72c8ba6f4d4a8984df2612eb0": "eyJ6aXAiOiJERUYiLCJwMnMiOiJObk9OdzU4Q0lHR29WbGQ1WUV0ZmxRIiwicDJjIjoxMDAwLCJ2ZXIiOiIxIiwiZW5jIjoiQTI1NkdDTSIsImFsZyI6IlBCRVMyLUhTNTEyK0EyNTZLVyJ9._i0U8IRV39xF0cgP1W53TVNo1BemYQPPAJ1zIBWOrM9QRZxgX6OLxw.78ruqytMMty4uZmU.p33nIq_0TjicUwicbqhtJrusaE_WsxPlOEzThV4XFUuME-Ff29tffU9X3mDD4uF2tMnKjx71J4TaRDn7mPw0-j5pDJeeFOzFxzKaq2o7dx55bYHeFG77LvbzY81OY1dRQCF0RX52D3k-3yay8hECiRThorx6SJTpDdR69XaP57WURw.kfL6gIWiP-JqkqV7LU4nMQ",
    "SSESSf924456a8134245645d3d9c6c79ad01a": "snqbcae2onqpdqqbp5sg7nko27",
    "uid": "6930727",
    "ldoc": "25547336-en",
    "referrer_path": "/products/rbc220a75f3jws",
    "Hm_lpvt_b99db6af50ce7be250cabdfa36f447da": "1770788622",
    "_uetsid": "fcb290d0066f11f1924a456922007945",
    "_uetvid": "5b154240db2f11f09bdabd14e06f1c08",
    "_clsk": "da0mjv%5E1770788623386%5E18%5E1%5Ez.clarity.ms%2Fcollect",
    "_ga_D1706WVDQV": "GS2.1.s1770787935$o63$g1$t1770788639$j60$l0$h0",
    "__cf_bm": "YBEGf5qYeSnOtT3akfRLitUzR6lX_XDt6G3KWoHzHAk-1770788880-1.0.1.1-PlmohbnmHlhwd_cPq6dTf3wG5P2V7ARA09yTIK4WXbSJSMN73uT77s.cGzQkPPTlHL6sD.nTpqJ1GApMrZC..VoDMpa8E_u3LDcLXQ9zJzY"
}
url = "https://www.renesas.cn/zh/products/rbc220a75f3jws"
params = {
    "queryID": "c90f114073f188f73662c89b3bac89c8",
    "tab": "documentation"
}

session = requests.Session()

# for key, value in cookies.items():
#     session.cookies.set(key, value)


response = session.get(url, headers=headers, params=params)
print(f"响应文本：{response.text}")
print("\n===== 服务器返回的Cookie =====")
print(response.cookies)
print(session.cookies)


print(f"\n响应状态码：{response.status_code}")
# https://www.renesas.cn/zh/document/dst/rbn300n75a5jws-datasheet
# pdf_url = "https://www.renesas.cn/zh/document/dst/rbc220a75f3jws-datasheet"
# pdf_url = "https://www.renesas.cn/zh/document/dst/rju1c16jws-datasheet"
pdf_url = "https://www.renesas.com/en/document/dst/cl8060-datasheet"
# cl8060
save_path = "cl8060_datasheet.pdf"
time.sleep(1)
try:
    response = requests.get(
        pdf_url,
        headers=headers,
        # cookies=cookies,
        stream=True,
        impersonate="chrome110"
    )
    response.raise_for_status()
    print(response)

    with open(save_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=32 * 1024):
            if chunk:
                f.write(chunk)

    if os.path.getsize(save_path) > 0:
        print(f"PDF下载成功，保存路径：{os.path.abspath(save_path)}")
    else:
        print("下载失败：文件为空")

except Exception as e:
    print(f"下载失败：{str(e)}")

