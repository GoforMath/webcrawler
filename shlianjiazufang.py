import requests
from bs4 import BeautifulSoup

base_url='https://sh.lianjia.com/zufang/pg%d/'
# lianjia provide list of properties up to 100 pages (30 properties per page), as a test I will only get first 5 pages

cookie='lianjia_ssid=f5093c93-7641-4861-899f-3fa706144e7e; lianjia_uuid=1ccf8b27-7cd5-42d4-8059-396c76deae16; srcid=eyJ0Ijoie1wiZGF0YVwiOlwiM2JkZjgyOGYxNTc3OWU0NDhkZmYzYzBhZDdkYTMxZjU2NzgxY2U2NzUzOGU5ODdkZTE0Yjc1MDg5NzMyZTBhNzBiODI0Mjc4MmFlMGI0NWE1YTk5MTRmYjc1MjJiOGRkOWUzMDhjOGQ2MDdlY2Y3YjY1NTg4YzFlOWQyMTQ5YjYwNDc3YzExN2Q5YWRjMDEyNzM3MDU3NTRmZDQ0MGQxYmJjMTAzZDVlNWExNWNiZTc4OWVjMTNhNjQ2ZDg2OTZkYmQ4N2FjZmY3NWQwODBmYTgwYTY2MDNlNzBkNzcwY2Q1ZmQ3NTMzMTg4ZmMzYzc2ZDAzYmI5YzMyZTk1YzhkNTg1ODU3MTcwMjAyMWFkYjA5ZGU3ODZhODczN2JkMWNkNTM0NDVmNmUzMzE3NmYzMDc3Y2U1Y2M3ODFlZTg4NjFcIixcImtleV9pZFwiOlwiMVwiLFwic2lnblwiOlwiMTQ4N2RmMDhcIn0iLCJyIjoiaHR0cHM6Ly9zaC5saWFuamlhLmNvbS96dWZhbmcvIiwib3MiOiJ3ZWIiLCJ2IjoiMC4xIn0='
user_agent='Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:68.0) Gecko/20100101 Firefox/68.0'

headers={
    'cookie':cookie,
    'user-agent':user_agent
}

s = requests.Session()
s.headers.update(headers)

f = open("shlianjiazufang.csv",'w')
tmp = ['标题','URL','位置','面积','朝向','房型','楼层','可否看房','租金']
f.write(','.join(tmp)+'\n')
buffer=''

for i in range(1,6): # only retrieve first 5 pages
    r = s.get(base_url % i)
    html_doc = r.text
    soup = BeautifulSoup(html_doc,features="html.parser")
    # content_list is the 17th div element appeared in the html document
    items=soup.find_all('div',"content__list--item")
    
    for i in items:
        # each i is a Tag
        main = i.div
        name = main.a.text.strip()
        partial_url = main.a["href"]
        # get description
        des=main.find("p","content__list--item--des").text # 其他同学有用select的 main.select(".content__list--item--des")，不知道开销和find比如何
        #tmp = des.find_all("a")
        #location = '-'.join([x.string for x in tmp]) not a good way to extract info
        des_list=des.split('/')
        location = des_list[0].strip()
        area = des_list[1].strip()
        direction = des_list[2].strip()
        roomtype = des_list[3].strip()
        floor = des_list[4].strip().replace(' ','')# remove leading, trailing space as well as space inside
        
        brand = main.find('p','content__list--item--brand oneline').text.strip() # not used
        publish_date = main.find('p',"content__list--item--time oneline").text # not used
        service = main.find("p","content__list--item--bottom oneline").text.strip().replace('\n','/')
        price = main.find("span","content__list--item-price").text.replace(' ','')

        tmp = [name,partial_url,location,area,direction,roomtype,floor,service,price]
        entry = ','.join(tmp)
        buffer = buffer+entry+'\n'
        #f.write(entry+'\n') change to batch writing
    f.write(buffer)

f.close()




