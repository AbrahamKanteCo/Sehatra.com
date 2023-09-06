from urllib.parse import urlencode
from urllib.request import Request, urlopen
from urllib.error import  HTTPError


def get_user_data_from_cognito(code= "code", refresh_token= "refresh_token"):
    url= "https://inscription.tolotra-malagasy.com/oauth2/token"

    header = {"Content-Type": 'application/x-www-form-urlencoded'}

    data= {}
    data["grant_type"] = "authorization_code"
    data['client_id'] = "60olko77t7033h8oi58dckcj4t"
    data["client_secret"] = "1vm1kojat6101le213hs2s6qpps3s243aba7qehiupn06k7meneo"
    data["code"] = code
    data["redirect_uri"]= "https://tolotra-malagasy.com"

    post_fields = data
    request = Request(url, urlencode(post_fields).encode())
    try:
        result = urlopen(request).read().decode()
        print (result)
    except HTTPError as e:
        raise


    try:
        if result.json()['error'] == "invalid_grant":

            data= {}
            data["grant_type"] = "refresh_token"
            data['client_id'] = "60olko77t7033h8oi58dckcj4t"
            data["client_secret"] = "1vm1kojat6101le213hs2s6qpps3s243aba7qehiupn06k7meneo"
            data["refresh_token"] = refresh_token

            post_fields = data
            request = Request(url, urlencode(post_fields).encode())
            result = urlopen(request).read().decode()
    except:
        pass
    print("2")
    print (result.json())
    access_token = result.json()['access_token']
    url= "https://inscription.tolotra-malagasy.com/oauth2/userInfo"
    header= {"Authorization": "Bearer " + access_token}
    result2 = requests.get(url= url, headers= header)
    return result2

code ="9dbbe9c5-66af-443e-8229-e2ff6997cfd9"
refresh_token= "eyJjdHkiOiJKV1QiLCJlbmMiOiJBMjU2R0NNIiwiYWxnIjoiUlNBLU9BRVAifQ.Hekg_dV02SWyFwn1kCd96j1j8wh1GI1bwOenuw2Tx8VrUMg9I3CgcOX70M7cBrvp-brqir5hPejyIF5qQez383ZGOzp5nAIo610_AC2K9wo2Hjte9sVBuu3MckWm5nhtfVvBPCxu8tuxoZBbuT8m5KuN29WoDvqotm9wERZ5Am8VdZM1AGUgqjY594FLC01RUBsIN5NjNrkWgSNK_wCq17SbFSsY4EdOau6wiVKzB7S1p4Nb7HdbFQwYboMHsPoLYz1X-PbxKx8zbTd92zXCLSAC2-Thna1fnBmwdNMPFtEFzqHmQ4l3BhbM0K5S7NV4dXkFTCQpCo5J8mKtIZLjtg.cDY-idFW67kphVJK.ovkEysco6tyVz49bJ0Q1DlQmlAdLP8-S2jLHv_jZS5Q1fBNl2xtHIbICKo4GjP9ZB00mgd4Mip59XlOO_xDggWJg7CEVW_JKfEgIUNYZp8Hn5CZs7WhegVypz4ew2jaR3pIpJwKiJiKT5QUQ80zlwnzFR6fDIEnTyLik1Z5tO-GM1BcC_doJ-SkCA_skRo9oEnCZs1ckSqbVHwVwHB0en-wtPKCNYb2toQkSJFYokQg3n_rjrUCDrk6e1_Z1v3diRlxqpDp-3t4p7hXcEl3qSEmKViAtMtwcXeWNOxxiATVN5gDvsqAhy1IvXzaPe1Pkp4zJLsbA02hLaUioS8TSogsFMuAPm2OIRhjHlbMR-f626FWItPkMDnjmdzkD-N8GP-fvkrhmUKZjIURpuV4cd77dbZK-LoL-4RgtsmLlhGOrQC34OsSJJwojxP5PT0gUwu3wy8bFmsbDu8PuU61brmGzLpA7MNHMwq40Hw4kfgYa1mpq615_F6PG-ykY2fdrwLj3q2Qs3kSHrNhtZJbj-nfH_kjWFL3DXK6nDPvBJumTl53MlSj_auzgZQVHiyImKsTCH3DeM78pmEi-eCfpvUHex9jXWuSsaSpvoyUbCOpIzME1VmmwhYn-DYuu_dwZIMiUoSO5Ewjps3uAdVSugpEIrX-kuffAXjbnHzx0kbjGXXVLdpXzeJbN_eURXlcuK05iYc0XvK9A_TgewpkfksuCXajrTxMsK7Vt0judlL9d0pxXhy1x_s8wRI-aAh7kQcc5nyylsqPoFq_xoDo7gvXjrs-zaIbotla9onQ20LhyScov1NCSIFsU_oeKPqs8ARSGhJLjhiM9jrIyEPMEcU7lX5jd-8_wax5CbNMZOAlkYZrPXAd60nbDhUo2fIHUdf0D42kyDnhI5AImZ4uXHoEVNL-aK_y3B4PuLcvTVqMTNGxaq7FGq3cIqCkXpQZo-CbsXco1wTRLH9Ppd4H9GkREOMDLUXvLo5wsud4YhemzpnsS9Qu7yrtKDHJFs2744R_st1bmb76QIdLC6OPFKgzbJ2GI_0ASJ-Owfk64DuoLGkpf_1DYJjdeU1fOzPx20izjrQzY5ZVK8EX2EmQHYLEoI2-dbdk7orW5-HO0z5iM9EsEQ-cyw6hdGzBgpKjIQ4Z7ScwlQoa-DrfFPGrTI6PcKWArpdFDVFpp_6iwu9RqUudlFxXawH1c8AaGnhb0NEjUaWWwgEhZBe5HT1LiC9IkDbrNsN-k8JPaTYqFU7u8hkNnJWwiMZfXWP0fxfuXnLEhiR4rJMteH52hYTEb_p0BZbsPWQ.qwmOSZitVUltmBXMSYkR8Q"
result = get_user_data_from_cognito(code=code)
print (result.json())
