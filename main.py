import datetime
import json
from time import sleep

from playwright.sync_api import sync_playwright

from xhs import DataFetchError, XhsClient, help


def sign(uri, data=None, a1="", web_session=""):
    for _ in range(10):
        try:
            with sync_playwright() as playwright:
                stealth_js_path = "/usr/local/xhs/stealth.min.js"
                chromium = playwright.chromium

                # 如果一直失败可尝试设置成 False 让其打开浏览器，适当添加 sleep 可查看浏览器状态
                browser = chromium.launch(headless=True)

                browser_context = browser.new_context()
                browser_context.add_init_script(path=stealth_js_path)
                context_page = browser_context.new_page()
                context_page.goto("https://www.xiaohongshu.com")
                browser_context.add_cookies([
                    {'name': 'a1', 'value': a1, 'domain': ".xiaohongshu.com", 'path': "/"}]
                )
                context_page.reload()
                # 这个地方设置完浏览器 cookie 之后，如果这儿不 sleep 一下签名获取就失败了，如果经常失败请设置长一点试试
                sleep(1)
                encrypt_params = context_page.evaluate("([url, data]) => window._webmsxyw(url, data)", [uri, data])
                return {
                    "x-s": encrypt_params["X-s"],
                    "x-t": str(encrypt_params["X-t"])
                }
        except Exception:
            # 这儿有时会出现 window._webmsxyw is not a function 或未知跳转错误，因此加一个失败重试趴
            pass
    raise Exception("重试了这么多次还是无法签名成功，寄寄寄")


if __name__ == '__main__':
    cookie = "a1=1905ee705a2h29iztvt1zj8cqlb2xkwx27k5g25qh40000338681;abRequestId=933cacf7-2922-5bcd-9dcb-8e5f8bacfa92;access-token-creator.xiaohongshu.com=customer.creator.AT-68c517384815744329520880s6xgpbl8jham0cbt;customer-sso-sid=68c5173848157443251648902d3b8825d957ab4d;customerClientId=178234479713173;galaxy_creator_session_id=U1UMjBkYPcuxzF26Ei4uqw1hIFC2Uf2JUiX4;galaxy.creator.beaker.session.id=1719411403889048209870;gid=yj82i8dyi8JWyj82ddW82WJ20JxJj3u9h9yuTAxVYSA1D248JCTECk888qqYKYy8J2iDddj8;sec_poison_id=4e6416e0-905f-46b8-a961-29ded64137f1;unread={%22ub%22:%22667aa265000000001c0249bc%22%2C%22ue%22:%22667e5986000000001c025368%22%2C%22uc%22:26};web_session=040069b5859d2f467151abf34b344b8569ff48;webBuild=4.23.1;webId=ca2450c18f92fe671c654be042212575;websectiga=cf46039d1971c7b9a650d87269f31ac8fe3bf71d61ebf9d9a0a87efb414b816c;x-user-id-creator.xiaohongshu.com=64f1de670000000005002107;xsecappid=xhs-pc-web;acw_tc=05fd7cae71f199e10dd5bc8d563934c24d262a5e42d4de209b519bdc0877fa89;"

    xhs_client = XhsClient(cookie, sign=sign)
    print(datetime.datetime.now())

    for _ in range(5):
        # 即便上面做了重试，还是有可能会遇到签名失败的情况，重试即可
        try:
            title = "从深呼吸开始"
            desc = "每天九点，深呼吸自愈一分钟 \n"
            images = [
                "/usr/local/xhs/generate-img/img/IMG_0560 (2).jpg",
                "/usr/local/xhs/generate-img/ending.jpg"
            ]
            topics=[
                {"id": "601b5f29000000000101f7fb","name": "正念练习","type": "topic"},
                {"id": "5e2e909d0000000001003238","name": "身心灵疗愈","type": "topic"},
                {"id": "5cfdaa72000000000d01940f","name": "能量疗愈","type": "topic"},
                {"id": "6049dded0000000001003d68","name": "今日宇宙指引","type": "topic"},
                {"name": "相信自己","type": "topic","id": "5c47264b000000000f03c841"},
                {"id": "5c7119c4000000000d01b242","name": "自我成长","type": "topic"},
                {"name": "女生必看","type": "topic","id": "5bfa9db460c92d00011a0b8b"},
                {"id": "62156c5b000000000100a10d","name": "正念打卡","type": "topic"},
                {"id": "53199e4cb4c4d6649d8b6131","name": "正能量","type": "topic"},
                {"id": "5455d746d6e4a908670092cf","name": "传递正能量","type": "topic"},
                {"id": "5f6bede0000000000100ba5d","name": "拒绝焦虑","type": "topic"},
                {"id": "60d02cea000000000101e96a","name": "拒绝内耗","type": "topic"},
                {"type": "topic","id": "5c320e7f00000000090316ef","name": "正念"},
                {"id": "5e8b565400000000010018d0","name": "一切都会越来越好","type": "topic"},
                {"id": "6374a654000000000100394b","name": "浪漫生活的记录者","type": "topic"}
            ]
            for topic in topics:
                desc = desc + f"#{topic['name']}[话题]#"
            note = xhs_client.create_image_note(title, desc, images, topics=topics, is_private=False, post_time="2023-07-25 23:59:59")
            print(note)
            break
        except DataFetchError as e:
            print(e)
            print("失败重试一下下")
