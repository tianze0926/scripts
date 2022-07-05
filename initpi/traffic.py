import requests

url = 'https://net.tsinghua.edu.cn/rad_user_info.php'

r = requests.post(url)

print(f'{int(r.text.split(",")[6]) / 1e9}G')

