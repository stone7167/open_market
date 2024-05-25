import json, ssl, random, threading, string
from websocket import WebSocketApp
from flask import Flask, request

approved_deposits = []
app = Flask(__name__)

def get_random_string(size):
    chars = string.ascii_lowercase+string.ascii_uppercase+string.digits
    return ''.join(random.choice(chars) for _ in range(size))

@app.route("/register", methods=["POST"])
def register():
    req = request.get_json()
    push_pin = req["token"]
    name = req["name"]
    amount = req["amount"]

    id = get_random_string(20)

    def on_message(ws, message):
        try:
            message = json.loads(message)

            if message["type"] == "nop":
                return
            elif message["type"] == "push":
                push = message["push"]

                notification_name = ""
                notification_amount = 0

                print("[pushbullet] {} | {}: {}".format(push["application_name"], push["title"], push["body"].replace("\n", " ")))

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

                        print(f"[pushbullet] 카카오뱅크 입금 | {notification_name}: {notification_amount}원")
                elif push["package_name"] == "viva.republica.toss":
                    if "원 입금" in push["title"]:
                        notification_name = push["body"].split(" ")[0]
                        notification_amount = int(push["title"].replace(",", "").replace("원 입금", ""))

                        print(f"[pushbullet] 토스뱅크 입금 | {notification_name}: {notification_amount}원")
                else:
                    return False

                if name == notification_name and amount == notification_amount:
                    print(f"[pushbullet] {id} | {notification_name}: {notification_amount}")
                    approved_deposits.append(id)

                    ws.close()
        except Exception as e:
            print(f"[pushbullet] 오류 | {e}")

    print(f"[pushbullet] 시작 | {push_pin} | {id}")

    ws = WebSocketApp("wss://stream.pushbullet.com/websocket/" + push_pin, on_message=on_message)

    wst = threading.Thread(target=ws.run_forever)
    wst.start()

    return { "id": id }

@app.route("/get", methods=["POST"])
def get():
    req = request.get_json()
    if req["id"] in approved_deposits:
        approved_deposits.remove(req["id"])
        return { "result": True }
    else:
        return { "result": False }

app.run(port=4040)