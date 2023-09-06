from urllib.parse import urlencode
from urllib.request import Request, urlopen
from urllib.error import  HTTPError
import requests

url = "https://api.moobipay.com/token/auth"

data = {}
data['client_id'] = "phkTrJitFoBfPhxvTfslPFmyKfQHXAQt"
data["client_secret"] = "NambGtiFKAxuERhS"
data["authorization_code"] = "cGhrVHJKaXRGb0JmUGh4dlRmc2xQRm15S2ZRSFhBUXQ6TmFtYkd0aUZLQXh1RVJoUw=="

res = requests.post(url, json=data)
print (res.json())
access_token = res.json()['access_token']
# access_token = "3239383bbfc700b0c628b7452a462cc68f1e0e43e55e6dfe7d96ccddc12201cf"
# url_paiement = "https://api.moobipay.com/v1/payment-init"
# header = {"Authorization": "Bearer " + access_token}
# data= {}
#
# data['currency'] = "MGA"
# data['service'] = "om"
# data['order_id'] = "12042021"
# data['order_label'] = "Test Paiement"
# data['amount'] = "10000"
# data['return_url'] = "http://localhost:8000"
# data['notif_url'] = "http://localhost:8000"
# data['cancel_url'] = "http://localhost:8000"
#
# res = requests.post(url_paiement, json=data, headers= header)
# print (res.json())
#
# pay_url = res.json()['pay_url']
#
#
#
#
#


