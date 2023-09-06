import requests


def validate_token(token):
    access_token = "f3644d524e292a191fb0c8d64df6696cf5481d9daf7b6e7afc802882e187831a"
    url_paiement = "https://api.moobipay.com/v1/paiment-status"
    header = {"Authorization": "Bearer " + access_token}
    data= {}

    data['pay_token'] = token

    res = requests.post(url_paiement, json=data, headers= header)
    print (res.json())
    if res.json()['status'] == "success":
        return True
    else:
        return False


if __name__ == "__main__":
    print (validate_token("7ee70b4b9a4e10f39bfef4646ee904d937818458"))