from datetime import datetime
import requests
import json

# read sensitives
f = open('sensitive.json')
sensitives = json.load(f)

TOKEN = sensitives['dnspod_token']

f.close()

###########
# ddns
###########

url = 'https://dnsapi.cn/Record.Ddns'

header = {
    'user-agent': 'ddns/1.0.0(tz039e@outlook.com)'
}

data = {
    "login_token": TOKEN,
    "domain": 'leoz.ml',
    "sub_domain": '*',
    "record_id": '811321586',
    "record_line_id": "0",
    "value": ''
}

data_2 = {
    "login_token": TOKEN,
    "domain": 'leoz.ml',
    "record_id": '811321226',
    "record_line_id": "0",
    "value": ''
}

def ddns():
    mypi = ""
    try:
        myip = requests.get('https://api-ipv4.ip.sb/ip').text[:-1]
    except:
        print('ip.sb error')
        return


    data['value'] = myip
    data_2['value'] = myip

    try:
        print(requests.post(url, data=data, headers=header).text)
        print(requests.post(url, data=data_2, headers=header).text)
    except:
        print('Failed: ', datetime.now())
    else:
        print('Done: ', datetime.now())

ddns()
