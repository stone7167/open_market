import json, threading
from websocket import WebSocketApp


def register(auth_token: str, name: str, amount: int, on_success):
    def on_message(ws, message):
        try:
            message = json.loads(message)

            if message["type"] == "nop":
                return
            elif message["type"] == "push":
                push = message["push"]

                notification_name = ""
                notification_amount = 0

                print("[푸시불렛] {} | {}: {}".format(push["package_name"], push["title"], push["body"].replace("\n", " ")))

                if push["package_name"] == "com.IBK.SmartPush.app":
                    sp = push["body"].split(" ")
                    notification_name = sp[2]
                    notification_amount = int(sp[1].replace("원", "").replace(",",""))
                    print(f"BankAPI[SUCCESS]: com.IBK.SmartPush.app")
                elif push["package_name"] == "com.nh.mobilenoti":
                    notification_name = message[5]
                    notification_amount = message[1].replace("입금", "").replace("원", "").replace(",","")
                    notification_amount = int(notification_amount)
                    print(f"BankAPI[SUCCESS]: com.nh.mobilenoti")
                elif push["package_name"] == "com.wooribank.smart.npib":
                    sp = push["body"].split(" ")
                    notification_name = sp[1]
                    notification_amount = int(sp[5].replace("원", "").replace(",",""))
                    print(f"BankAPI[SUCCESS]: com.wooribank.smart.npib")
                elif push["package_name"] == "com.kakaobank.channel":
                    if "입금 " in push["title"]:
                        notification_name = push["body"].split(" ")[0]
                        notification_amount = int(push["title"].replace("입금 ", "").replace(",", "").replace("원", ""))

                        print(f"[푸시불렛] 카카오뱅크 입금 | {notification_name}: {notification_amount}원")
                elif push["package_name"] == "viva.republica.toss":
                    if "원 입금" in push["title"]:
                        notification_name = push["body"].split(" ")[0]
                        notification_amount = int(push["title"].replace(",", "").replace("원 입금", ""))

                        print(f"[푸시불렛] 토스뱅크 입금 | {notification_name}: {notification_amount}원")
                else:
                    return False

                if name == notification_name and amount == notification_amount:
                    print(f"[푸시불렛] 성공 | {notification_name}: {notification_amount}원")
                    on_success()

                    ws.close()
        except Exception as e:
            print(f"[푸시불렛] 오류")
            print(e)

    ws = WebSocketApp("wss://stream.pushbullet.com/websocket/" + auth_token, on_message=on_message)

    wst = threading.Thread(target=ws.run_forever)
    wst.start()

    print(f"[푸시불렛] 입금 신청 | {name}: {amount}원")
    return True