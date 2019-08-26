import requests
apikey = 'apikey=0df993c66c0c636e29ecbb5344252a4a'
apimovie250 = 'https://api.douban.com/v2/movie/top250?' # apimovie250+start_str+'&'+apiKey

MOVIETOTAL = 250
start=0
with open('movie_list_simple.csv','w',encoding="utf-8") as f:
    while start < MOVIETOTAL:
        start_str='start='+str(start)
        rsp = requests.get(apimovie250+start_str+'&'+apikey)
        items = rsp.json()
        start += items['count']
        movie_list = items['subjects']
        for d in movie_list:
            entry_list = []
            # get movie id
            entry_list.append(str(d['id']))
            # get movie title
            entry_list.append(d['title'])
            # get average rating
            entry_list.append(str(d['rating']['average']))
            # get casts (using list comprehension)
            celebrity_list = [celebrity['name'] for celebrity in d['casts']]
            entry_list.append('/'.join(celebrity_list))
            # get image of small size
            entry_list.append(d['images']['small'])
            # for other features, we can do it the same way               
            entry=','.join(entry_list)
            f.write(entry+'\n')
print('collection done')

# 比起第一个版本，这个方式可以省掉一个if...elif...else判断，因为直接拿key取值，也省掉了循环字典的所有键值对，
# 注意到 https://stackoverflow.com/questions/10458437/what-is-the-difference-between-dict-items-and-dict-iteritems
# 如果出于内存考虑不想用.items()方法，还可以用.iteritems()方法，返回iterator，但避免不了用if判断key值
