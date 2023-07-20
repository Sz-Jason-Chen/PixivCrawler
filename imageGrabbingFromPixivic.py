"""
This is a separate independent crawler written by @Mist2404.
It gets relevant images by searching for the keywords provided.
"""

import requests
import json
import time

# adr = input('请输入图片存储的文件夹路径')
adr = "E:\program\PixivCrawler"
# kw = input('请输入搜索关键词')
kw = "刻晴"
#pages = input('请输入爬取页数')
headers = {
     'referer': 'https://pixivic.com/',
     'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
     'authorization': 'eyJhbGciOiJIUzUxMiJ9.eyJwZXJtaXNzaW9uTGV2ZWwiOjEsInJlZnJlc2hDb3VudCI6MiwiaXNDaGVja1Bob25lIjowLCJ1c2VySWQiOjUwODY2NywiaWF0IjoxNjgwMDkwNjA3LCJleHAiOjE2ODA2MDkwMDd9.65rv_9yQZCGcwtNmjrY96Ro-9rylVFTwa7Xe8Jklhn9F-s9I3DfAmYguauMBH1aLHIHQgjLf8B-SihL33PzsiA',
     'cookie': 'id=22d61a357cce00a3||t=1635859619|et=730|cs=002213fd48bf443a5925ede07e'
 }
url = 'https://api.bbmang.me/illustrations?illustType=illust&searchType=original&maxSanityLevel=3&page=1&keyword={}&pageSize=30'.format(kw)
r = requests.get(url,headers= headers)
content = r.text
json_data = json.loads(content)
data = json_data['data']
for item in data:
    image = item['imageUrls']
    Id = item['id']
    imageUrls = image[0]['original']
    real_img = imageUrls.replace('i.pximg.net','o.acgpic.net')
    # if(real_img.status_code != 200):
    #     break
    fo = real_img[-3:]
    print(real_img)
    response = requests.get(real_img, headers=headers)
    with open(adr + '\demo_涩图' + '\{}.{}'.format(Id,fo),'wb') as f:
        f.write(response.content)

