import requests
import json
import base64
import datetime
import uuid


def get_token():
    url_token = "https://api.mvola.mg/token"
    consumer_key = "C_7hMJk8We7d_poyjXE0kiaGfn8a"
    consumer_secret = "clAJUi7qfbcM7flrLi5F0pC8JVQa"
    byte = "{}:{}".format(consumer_key, consumer_secret).encode('ascii')
    header = {"Authorization": "Basic {}".format(base64.b64encode(byte).decode("ascii"))}
    data = {}
    data["grant_type"] = "client_credentials"
    data['scope'] = "EXT_INT_MVOLA_SCOPE"
    result = requests.post(url=url_token, headers=header, data=data)
    data_token = result.json()
    access_token = data_token['access_token']
    return access_token


def get_pay_token_mvola (numero, tarif):
    url = "https://api.mvola.mg/mvola/mm/transactions/type/merchantpay/1.0.0/"
    header = {}
    header['Authorization'] = "Bearer "+get_token()
    header["Version"] = "1.0"
    header["X-CorrelationID"] = str(uuid.uuid4())
    header["X-CorrelationID"] = "ab04a625-c502-48a0-a879-e8624db33a7c"
    header["UserLanguage"] = "MG"
    header["UserAccountIdentifier"] = "msisdn;0340946627"
    header["X-Callback-URL"] = "https://sehatra.com/"
    header['partnerName'] = "Sehatra.com"
    header['Content-Type'] = "application/json"
    header['Cache-Control'] = "no-cache"
    ref= str(uuid.uuid4())
    post_data = {}
    post_data['currency'] = "Ar"
    post_data['amount'] = "{}".format(tarif)
    post_data["requestingOrganisationTransactionReference"] = ref
    date = str(datetime.datetime.now().isoformat())
    post_data['requestDate'] = date.replace(date[-3:], "Z")
    post_data['descriptionText'] = "billet sehatra"
    post_data['originalTransactionReference'] = ref
    post_data['debitParty'] = [{
      "key": "msisdn",
      "value": "{}".format(numero)
    }]
    post_data['creditParty'] = [{
      "key": "msisdn",
      "value": "0340946627"
    }]
    post_data['metadata'] = [
      {
        "key": "partnerName",
        "value": "SEHATRA.COM",
      }
    ]

    result = requests.post(url=url, headers=header, data=json.dumps(post_data))
    return result.json()["serverCorrelationId"]


def get_mvola_result(token):
    url = "https://api.mvola.mg/mvola/mm/transactions/type/merchantpay/1.0.0/"
    header = {}
    header['Authorization'] = "Bearer "+get_token()
    header["Version"] = "1.0"
    header["X-CorrelationID"] = str(uuid.uuid4())
    header["X-CorrelationID"] = "ab04a625-c502-48a0-a879-e8624db33a7c"
    header["UserLanguage"] = "MG"
    header["UserAccountIdentifier"] = "msisdn;0340946627"
    header["X-Callback-URL"] = "http://sehatra.com/"
    header['partnerName'] = "Sehatra.com"
    header['Content-Type'] = "application/json"
    header['Cache-Control'] = "no-cache"

    result = requests.get(url=url+"/status/{}".format(token), headers=header)

    return result.json()["status"]

