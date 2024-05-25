import bcrypt
import pybase64
import time
import requests
import datetime


def get_timestamp():
    return int(time.time() * 1000)


def create_signature(client_id: str, client_secret: str, timestamp: int) -> str:
    # 밑줄로 연결하여 password 생성
    password = client_id + "_" + str(timestamp)

    # bcrypt 해싱
    hashed = bcrypt.hashpw(password.encode('utf-8'), client_secret.encode('utf-8'))

    # base64 인코딩
    return pybase64.standard_b64encode(hashed).decode('utf-8')


def get_token(client_id: str, client_secret: str) -> tuple[bool, str]:
    timestamp = get_timestamp()

    res = requests.post(
        "https://api.commerce.naver.com/external/v1/oauth2/token",
        data={
            "client_id": client_id,
            "timestamp": timestamp,
            "grant_type": "client_credentials",
            "client_secret_sign": create_signature(client_id, client_secret, timestamp),
            "type": "SELF"
        }
    )

    if res.status_code != 200:
        return False, "네이버 커머스API OAuth2 인증 토큰 발급에 실패하였습니다"

    return True, res.json()["access_token"]


def get_order_ids(token: str, order_id: str) -> tuple[bool, str, list[str]]:
    if not order_id.isnumeric():
        return False, "주문번호가 숫자가 아닙니다", []

    res = requests.get(
        f"https://api.commerce.naver.com/external/v1/pay-order/seller/orders/{order_id}/product-order-ids",
        headers={
            "authorization": f"Bearer {token}"
        }
    )

    if res.status_code != 200:
        return False, res.json()["message"], []

    return True, res.json()["traceId"], res.json()["data"]


def get_order_details(token: str, order_ids: list[str]) -> tuple[bool, str, list[dict]]:
    if not all(order_id.isnumeric() for order_id in order_ids):
        return False, "주문 ID가 숫자가 아닙니다", []

    res = requests.post(
        "https://api.commerce.naver.com/external/v1/pay-order/seller/product-orders/query",
        headers={
            "authorization": f"Bearer {token}",
            "content-type": "application/json"
        },
        json={
            "productOrderIds": order_ids
        }
    )

    if res.status_code != 200:
        return False, res.json()["message"], []

    return True, res.json()["traceId"], res.json()["data"]


def deliver_order(token: str, order_id: str):
    if not order_id.isnumeric():
        return False, "주문 ID가 숫자가 아닙니다"

    res = requests.post(
        "https://api.commerce.naver.com/external/v1/pay-order/seller/product-orders/dispatch",
        headers={
            "authorization": f"Bearer {token}",
            "content-type": "application/json"
        },
        json={
            "dispatchProductOrders": [
                {
                    "productOrderId": order_id,
                    "deliveryMethod": "DIRECT_DELIVERY",
                    "dispatchDate": datetime.datetime.now().astimezone().isoformat()
                }
            ]
        }
    )

    print(res.json())
    if res.status_code != 200:
        return False, res.json()["message"]

    if len(res.json()["data"]["successProductOrderIds"]) == 1:
        return True, res.json()["traceId"]

    return False, res.json()["data"]["failProductOrderInfos"][0].message