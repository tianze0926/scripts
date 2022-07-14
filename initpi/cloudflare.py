import socket
import requests
from datetime import datetime
import json
import time

from typing import TypedDict, List

class Record(TypedDict):
    id: str
    name: str

def ddns(token: str, zone_id: str, records: List[Record]):
    print('Cloudflare DDNS', datetime.now())

    myip = socket.gethostbyname(socket.gethostname())
    
    headers = {
        'Authorization': f'Bearer {token}'
    }
    for i, record in enumerate(records):
        print(f'record {i}: ')
        try:
            r = requests.put(
                f'https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records/{record["id"]}',
                headers=headers,
                json={
                    'type': 'A',
                    'name': record['name'],
                    'content': myip,
                    'ttl': 1,
                    'proxied': False,
                }
            )
            print(r.status_code)
            if r.status_code != 200:
                print(r.json())
        except Exception as e:
            print(e)

if __name__ == '__main__':
    with open('sensitive_cloudflare.json') as f:
        info = json.load(f)

    print('Input: ', info)

    while True:
        ddns(**info)
        time.sleep(30)