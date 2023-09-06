import requests
import json


def get_token():
    url_token ="https://api.orange.com/oauth/v3/token"
    header_test = {"Authorization": "Basic VUxWZ25HZE9SNGdNS2MwbFZIV0VyNUxNTlNsRU81cVo6WkdhWHRYTE5NMjJhaWRXdQ=="}
    header = {"Authorization": "Basic dnVHSkdIV0FoUzZaV2dPWEp0alN0RmJ5YXFzeHo3OFo6MUdsbDdyR05BcnJHWDljNQ=="}
    data = {}
    data["grant_type"] = "client_credentials"
    result = requests.post(url=url_token, headers=header, data=data)
    data_token = result.json()
    access_token = data_token['access_token']
    return access_token


def get_pay_token (billet):
    # merchant_key_test = "50ff86f7"
    merchant_key = "9eba21fa"
    url = "https://api.orange.com/orange-money-webpay/mg/v1/webpayment"
    # url_test = "https://api.orange.com/orange-money-webpay/dev/v1/webpayment"
    header = {"Authorization": "Bearer "+ get_token(), "Content-Type": "application/json"}
    post_data = {}
    post_data['merchant_key'] = merchant_key
    post_data['currency'] = "MGA"
    post_data['order_id'] = "Billet-{}".format(billet.slug)
    post_data['amount'] = billet.video.tarif_ariary
    url_sehatra = "https://sehatra.com"
    post_data['return_url'] = "{}/paiement/orange-money/return/{}/".format(url_sehatra, billet.slug)
    post_data['cancel_url'] = "{}/paiement/orange-money/cancel/{}/".format(url_sehatra, billet.slug)
    post_data['notif_url'] = "{}/paiement/orange-money/notif/{}/".format(url_sehatra, billet.slug)
    post_data['lang'] = "fr"
    post_data['reference'] = "SEHATRA.COM"
    result = requests.post(url=url, headers=header, data=json.dumps(post_data))
    return result


def get_transaction_status (paiement):
    url = "https://api.orange.com/orange-money-webpay/mg/v1/transactionstatus"
    header = {"Authorization": "Bearer "+ get_token(), "Content-Type": "application/json"}
    post_data = {}
    post_data['order_id'] = "Billet-{}".format(paiement.billet.slug)
    post_data['pay_token'] = paiement.token
    post_data['amount'] = 100
    result = requests.post(url=url, headers=header, data=json.dumps(post_data))
    return result


