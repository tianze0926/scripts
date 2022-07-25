import argparse
import requests
import base64
from datetime import datetime
import time

def download(credential: str) -> int:
    """
    Return the byte length of the file.
    """
    url = 'https://dav.jianguoyun.com/dav/KeePass/KeePass.kdbx'
    r = requests.get(url, headers={
        'Authorization': f'Basic {credential}'
    })
    if r.status_code != 200:
        raise Exception(f'failed: {r.status_code}')
    
    with open('/file/KeePass.kdbx', 'wb') as f:
        f.write(r.content)
    
    return int(r.headers['Content-Length'])

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--auth_file', type=str, required=True)
    args = parser.parse_args()

    with open(args.auth_file) as f:
        credential = f.readline().strip()

    credential = base64.encodebytes(credential.encode()) \
                        .decode().strip()
    
    while True:
        print(datetime.now())
        try:
            length = download(credential)
        except Exception as e:
            print(e)
        else:
            print(length)
        
        time.sleep(600)
