import time
from datetime import datetime
import requests
import socket
import json

import tunet

# read sensitives
f = open('sensitive.json')
sensitives = json.load(f)

USERNAME = sensitives['username']
PASSWORD = sensitives['password']
TOKEN = sensitives['dnspod_token']

f.close()

###########
# ddns
###########

url = 'https://dnsapi.cn/Record.Ddns'

header = {
    'user-agent': 'ddns/1.0.0(tz039e@outlook.com)'
}

datas = [
    {
        "login_token": TOKEN,
        "record_line_id": "0",
        "value": '',
        **d
    } for d in [
        {
            'domain': 'leoz.ml',
            'record_id': '811321586',
            'sub_domain': '*'
        },
        {
            'domain': 'leoz.ml',
            'record_id': '811321226',
            'sub_domain': '@'
        },
        {
            'domain': 'tianze.xyz',
            'record_id': '962662642',
            'sub_domain': '*'
        },
        {
            'domain': 'tianze.xyz',
            'record_id': '958081611',
            'sub_domain': '@'
        },
    ]
]

def ddns():
    mypi = ""
    try:
        myip = requests.get('https://api-ipv4.ip.sb/ip').text[:-1]
    except:
        print('ip.sb error')
        return

    for d in datas:
        d['value'] = myip

    try:
        for d in datas:
            print(requests.post(url, data=d, headers=header).text)
    except:
        print('Failed: ', datetime.now())
    else:
        print('Done: ', datetime.now())

##################
# test internet
##################

# force IPv4
import requests.packages.urllib3.util.connection as urllib3_cn
def allowed_gai_family():
    family = socket.AF_INET    # force IPv4
    return family
urllib3_cn.allowed_gai_family = allowed_gai_family

timeout = 5
test_url = 'https://www.baidu.com'

ddns()

while True:
    try:
        request = requests.get(test_url, timeout=timeout)
        # if connected
        time.sleep(30)
    except (requests.Timeout, requests.exceptions.SSLError):
        # if ipv4 is not connected
        print(datetime.now())
        print(tunet.auth4.logout())
        print(tunet.auth4.login(USERNAME, PASSWORD, net=True))
        ddns()
