# -*- coding:utf-8 -*-
'''
crossin的爬虫学习小组第二次作业(apikey由crossin提供)
1. 获取电影肖申克的救赎的海报，并以jpg形式保存在本地
2. 获取豆瓣Top250部电影的信息，并组织成为一个csv文件
'''
import requests
from PIL import Image
from io import BytesIO

movieid = '1292052'# movie ID for The Shawshank Redemption
apikey = 'apikey=0df993c66c0c636e29ecbb5344252a4a'
apimovie = 'https://api.douban.com/v2/movie/' # apimovie+movieid+'?'+apikey
apimovie250 = 'https://api.douban.com/v2/movie/top250?' # apimovie250+start_str+'&'+apiKey

#get poster of The Shawshank Redemption
rsp = requests.get(apimovie+movieid+'?'+apikey)
img_url = rsp.json()['image']
img_rsp = requests.get(img_url)
i = Image.open(BytesIO(img_rsp.content)) # get image instance
with open(movieid+'.jpg','wb') as f:
    i.save(f, format='JPEG')
    
# get top 250 movies on douban.com
MOVIETOTAL = 250
start=0
with open('movie_list.csv','w',encoding="utf-8") as f:
    while start < MOVIETOTAL:
        start_str='start='+str(start)
        rsp = requests.get(apimovie250+start_str+'&'+apikey)
        items = rsp.json()
        start += items['count']
        movie_list = items['subjects']
        for d in movie_list:
            entry_list = []
            for key, val in d.items():
                if key == 'rating':
                    entry_list.append(str(val['average']))
                elif key == 'casts' or key=='directors':
                    casts_list = []
                    for celebrity in val:
                        casts_list.append(celebrity['name'])
                    entry_list.append('/'.join(casts_list))
                elif key== 'images':
                    entry_list.append(val['small']) # default is to save the link to small pic
                elif isinstance(val,list):
                    item_list = []
                    for i in val:
                        item_list.append(str(i))
                    entry_list.append('/'.join(item_list))
                elif key== "original_title":
                    #在处理排名49的两杆大烟枪时因为原始电影original_title（"Lock, Stock and Two Smoking Barrels"）里有逗号
                    #导致excel在检查时会将title拆成两部分 比正常数据多出一列 格式有误
                    #https://stackoverflow.com/questions/4617935/is-there-a-way-to-include-commas-in-csv-columns-without-breaking-the-formatting
                    #根据这个链接建议，需要在数据外再包一层""
                    #也可以加if 判断里面是否有逗号，再决定是否包 不过我觉得这样划不来 不如全包上
                    entry_list.append('"'+val+'"')
                else:
                    entry_list.append(str(val))
            entry=','.join(entry_list)
            f.write(entry+'\n')
print('collection done')
