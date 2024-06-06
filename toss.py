import requests, os

def check(word, name, amount):
    if not os.path.isfile('토스_확인된거래.txt'):
        f = open('토스_확인된거래.txt', 'w')
        f.close()
        
    base = {"result": None, "id": None, "name": None, "amount": None, "msg": None}

    if 1 < len(name) < 5: # 2~4글자 이름, 두번째 문자 * 표시
        s = list(name)
        s[1] = "*"
        name = ''.join(s)
    elif len(name) > 6: #7글자 이상 이름, 6번째까지만 표시
        name = name[:6]

    url = "https://api-public.toss.im/api-public/v3/cashtag/transfer-feed/received/list?inputWord=" + word
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"}
    response = requests.get(url, headers=headers).json()

    if not response['resultType'] == "SUCCESS": # api 호출실패 (ip차단)
        print("ip차단")
        msg = response["error"]["errorCode"] + " " + response["error"]["reason"]
        base["result"] = "ip차단"
        base["msg"] = msg
        return base

    data = response["success"]["data"]
    for transaction in data:
        transfer_id = transaction["cashtagTransferId"]
        transfer_name = transaction["senderDisplayName"]
        transfer_amount = transaction["amount"]

        if name == transfer_name: # 1. 이름이 동일한가?
            with open("토스_확인된거래.txt") as f: # 입금자명을 정해준다면 이미 처리된 거래인지 확인하지 않아도 된다.
                checked = f.read()

            if not (str(transfer_id) + "\n") in checked and amount == transfer_amount: # 2. 이전에 처리되지 않은 기록인가? / 3. 금액이 동일한가?
                with open("토스_확인된거래.txt", "a") as f:
                    f.write(str(transfer_id) + "\n")
                base["result"] = True
                base["id"] = transfer_id
                base["name"] = transfer_name
                base["amount"] = transfer_amount
                return base

    base["result"] = False # 입금내역에 존재하지 않음
    base["msg"] = "입금 미확인"
    return base