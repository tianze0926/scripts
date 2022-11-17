import requests
from tqdm import tqdm

URL = 'url of <video />'
FILENAME = 'video.mp4'

headers = {
    'authority': 'yunluzhi-az-1258344699.file.myqcloud.com',
    'scheme': 'https',
    'accept': '*/*',
    'accept-encoding': 'identity;q=1, *;q=0',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'no-cache',
    'pragma': 'no-cache',
    'range': 'bytes=0-',
    'referer': 'https://meeting.tencent.com/',
    'sec-ch-ua': '"Chromium";v="109", "Not_A Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'video',
    'sec-fetch-mode': 'no-cors',
    'sec-fetch-site': 'cross-site',
    'sec-gpc': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
}

r = requests.get(URL, stream=True, headers=headers)
print(r.headers['Content-Length'])
print(r.status_code)

with open(FILENAME, 'wb') as f:
    pbar = tqdm(unit='B', total=int(r.headers['Content-Length']))
    for chunk in r.iter_content(chunk_size=1024):
        if chunk:
            pbar.update(len(chunk))
            f.write(chunk)


