# -*- coding: utf-8 -*-
from config import account_id, secret_key
from yookassa import Configuration,  Payment
import json
import asyncio

Configuration.account_id = account_id
Configuration.secret_key = secret_key
async def payment_create(sum, description):
    payment = Payment.create({
        "amount": {
            "value": sum,
        "currency": "RUB"
    },
        "payment_method_data": {
        "type": "bank_card"
    },
    "confirmation": {
        "type": "redirect",
        "return_url": "Ссылка, куда перенаправить после совершения платежа"
    },
    "capture": True,
    "description": description
    })
    payment_data = json.loads(payment.json())
    payment_id = payment_data['id']
    payment_url = (payment_data['confirmation'])['confirmation_url']
    return (payment_id,payment_url)
    #return json.loads(payment.json())


async def check_payment(payment_id):
	payment = json.loads((Payment.find_one(payment_id)).json())
	while payment['status'] == 'pending':
		payment = json.loads((Payment.find_one(payment_id)).json())
		await asyncio.sleep(5)

	if payment['status']=='succeeded':
		print("SUCCSESS RETURN")
		print(payment)
		return True
	else:
		print("BAD RETURN")
		print(payment)
		return False