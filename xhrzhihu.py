import requests
import logging

#import json

page_number = 1  # default initial value is 2
limit = 6  # default number of items returned in each request
after_id = 0 # default initial value is 5, update by after_id += limit

# 看起来知乎是首先加载5个推荐问答/文章，如果用户继续下拉，再从after_id开始，继续加载，共加载limit个，page_number也自增
# 因此可以用循环多次发送请求，获取前x个推荐

url = 'https://www.zhihu.com/api/v3/feed/topstory/recommend?page_number=%s&after_id=%s'

cookie = 'q_c1=0462fdf7af1748989f4eb03c4682043d|1565338204000|1506911204000; q_c1=0462fdf7af1748989f4eb03c4682043d|1506911204000|1506911204000; _zap=d72bd555-3cdf-4f68-8ccb-964d581f8628; d_c0="AACCRPDPdgyPTgY7GGgMnQo6QeY_9x8wdOY=|1506911786"; __utma=51854390.77038509.1506911786.1561119486.1561889866.10; __utmv=51854390.100--|2=registration_date=20130322=1^3=entry_date=20130322=1; _xsrf=5ZVuz2qGsOh8otRlswM22VkDtqewG9u6; z_c0="2|1:0|10:1552749264|4:z_c0|92:Mi4xRlNnSkFBQUFBQUFBQUlKRThNOTJEQ1lBQUFCZ0FsVk4wR0I2WFFDUE5yVGFLbmpJZnVWQ0RyRnI0NHpSSXE0a0tB|27463a310cddaa038481b8071e6797c4ef411aa03866b611cea7fb9975a5e376"; __gads=ID=e5f39879eba3251b:T=1554648790:S=ALNI_MZjCNlDeWYswk-VR0AzzBNcI6uPzg; __utmz=51854390.1561889866.10.8.utmcsr=zhihu.com|utmccn=(referral)|utmcmd=referral|utmcct=/hot; _ga=GA1.2.77038509.1506911786; tst=r; tgw_l7_route=73af20938a97f63d9b695ad561c4c10c'
user_agent = 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:68.0) Gecko/20100101 Firefox/68.0'

headers = {
    'cookie': cookie,
    'user-agent': user_agent
}

s = requests.Session() # help reuse tcp connection
s.headers.update(headers) # bind the headers

PAGECOUNT = 5
with open('xhrzhihu.csv', 'w', encoding='utf-8') as f:
    while page_number <= PAGECOUNT:
        r = s.get(url % (page_number, after_id))
        page_number += 1
        after_id += limit
        data_list = r.json()['data']
        for data in data_list:
            entry_list = []
            entry_list.append(data['action_text'])
            target = data['target']
            #logging.error(str(target.keys())+target['url'])
            type = target['type']
            entry_list.append(type)
            if type =='answer':
                entry_list.append(target['question']['title'])  
            else: # assume there is only 2 types: answer / article
                entry_list.append(target['title'])
            entry_list.append(target['author']['name'])
            entry_list.append(str(target['voteup_count']))
            # 有些target的type是 article，就没有thanks_count
            entry_list.append(str(target['comment_count']))
            entry_list.append(target['url'])
            entry_list.append(target['excerpt'])
            f.write(','.join(entry_list)+'\n')