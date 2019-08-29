import requests
import time
import bs4

start = 0
pageSize = 90
url = 'https://fe-api.zhaopin.com/c/i/sou?start=%d&pageSize=90&cityId=538&workExperience=-1&education=-1&companyType=-1&employmentType=-1&jobWelfareTag=-1&kw=python&kt=3'

cookie = 'acw_tc=2760822715670614832681982e0e2a3914f6458682f6e78f6c553ba01d1bc2'
user_agent = 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:68.0) Gecko/20100101 Firefox/68.0'

s = requests.Session()
s.headers.update({'cookie': cookie, 'user-agent': user_agent})

entry_list = []
url_list = []

r = s.get(url % start)
results = r.json()['data']['results']
for entry in results:
    jobName = entry['jobName']
    # city = entry['city']['display']
    compName = entry['company']['name']
    compType = entry['company']['type']['name']
    compSize = entry['company']['size']['name']
    salary = entry['salary']
    eduLevel = entry['eduLevel']['name']
    workingExp = entry['workingExp']['name']
    emplType = entry['emplType']
    url = entry['positionURL']

    entry_list.append(','.join(
        [jobName, compName, compType, compSize, salary, eduLevel, workingExp, emplType, url]))
    url_list.append(url)

with open('pyzhaopinJD.csv', 'w') as f:
    titles = ['职位名称','公司名称','公司类型','公司规模','薪酬','学历','工作经验','是否全职','职位页面','岗位职责']
    f.write(','.join(titles)+'\n')
    for i in range(len(url_list)):
        r = s.get(url_list[i])
        strainer = bs4.SoupStrainer('div', 'describtion__detail-content')
        soup = bs4.BeautifulSoup(r.text, "lxml", parse_only=strainer)
        jd = soup.get_text(strip=True) # get job description
        f.write(entry_list[i]+','+jd+'\n')
        print('collecting %d(th) JD ...' %i)
        time.sleep(2) # wait for 2s before next http request