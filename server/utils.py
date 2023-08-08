import datetime
import uuid
from typing import Any, Dict, List, Optional

import razorpay
from django.conf import settings

CLIENT = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))


def create_razorpay_order(
    amount: int,
    currency: str = "INR",
    receipt: Optional[str] = None,
    notes: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    if receipt is None:
        receipt = str(uuid.uuid4())[:8]

    data = {
        "amount": amount,
        "currency": currency,
        "receipt": receipt,
        "notes": notes,
    }
    response = CLIENT.order.create(data=data)
    response["key"] = settings.RAZORPAY_KEY_ID
    response["order_id"] = response["id"]
    return response


def get_transactions() -> List[Dict[str, Any]]:
    now = datetime.datetime.now()
    last_week = now - datetime.timedelta(days=7)

    page_size = 100
    default = {
        "from": int(last_week.timestamp()),
        "to": int(now.timestamp()),
        "count": page_size,
    }

    transactions = []
    skip = 0
    while True:
        query = dict(**default, skip=skip)
        transactions_ = CLIENT.payment.all(query)
        if transactions_["count"] == 0:
            break
        else:
            transactions.extend(transactions_["items"])
        skip += page_size

    return transactions


def verify_razorpay_payment(payment_info: Dict[str, str]) -> bool:
    try:
        return CLIENT.utility.verify_payment_signature(payment_info)
    except razorpay.errors.SignatureVerificationError as e:
        print(e)
        return False


def verify_razorpay_webhook_payload(body: str, signature: str) -> bool:
    secret = settings.RAZORPAY_WEBHOOK_SECRET
    try:
        return CLIENT.utility.verify_webhook_signature(body, signature, secret)
    except razorpay.errors.SignatureVerificationError as e:
        print(e)
        return False


def mask_string(s: str) -> str:
    n = len(s)
    if n >= 8:
        return s[:2] + "x" * (n - 4) + s[-2:]
    elif n >= 6:
        return s[:1] + "x" * (n - 2) + s[-1:]
    else:
        return s[:1] + "x" * (n - 1)
