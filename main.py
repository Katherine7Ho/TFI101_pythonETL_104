import pandas as pd
import requests
from bs4 import BeautifulSoup
import json
import time

# def main():
userAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
headers = {
'UserAgent': userAgent
}

parameterDict = {
    'ro': '0',
    'keyword': 'python',
    'expansionType': 'area%2Cspec%2Ccom%2Cjob%2Cwf%2Cwktm',     # '%2C' = ',' # area,spec,com,job,wf,wktm
    'order': '1',
    'asc': '0',
    'page': '1',
    'mode': 's',
    'langFlag': '0'
}


parameterList = [key+'='+val for key, val in parameterDict.items()]    # ['ro=0', 'keyword=python', 'expansionType=area%2Cspec%2Ccom%2Cjob%2Cwf%2Cwktm', 'order=1', 'asc=0', 'page=1', 'mode=s', 'langFlag=0']['ro=0', 'keyword=python', 'expansionType=area%2Cspec%2Ccom%2Cjob%2Cwf%2Cwktm', 'order=1', 'asc=0', 'page=1', 'mode=s', 'langFlag=0']

url = "https://www.104.com.tw/jobs/search" + '?' + '&'.join(parameterList)

ss = requests.session()

res = ss.get(url, headers=headers)
soup = BeautifulSoup(res.text, 'html.parser')
# print(soup)

# article
articleList = soup.select('article')    # 搜尋關鍵字後，頁面上的工作。 約20~30個

articleTitleUrlList = list()
for i in articleList:
    try:
        articleTitle = i.select('a[class="js-job-link"]')[0].text    # 工作職稱
        articleUrl = "https:" + i.select('a[class="js-job-link"]')[0]['href']    # 工作網址
        articleTitleUrlList.append((articleTitle, articleUrl))    # 工作 與其對應 網址
        # print(articleTitle)
        # print(articleUrl)
    except:
        pass
        # print(i.select('a[class="js-job-link"]'))
    # print('===============')

print(articleTitleUrlList)


# company, job_title, job_content, job_category
jobInfo = []
for articleTitle, articleUrl in articleTitleUrlList:
    print(articleTitle)
    print(articleUrl)

    jobUrl = articleUrl.split('?')[0]
    jobUrlAhead = jobUrl.split('://')[0]
    jobUrlBehindList = jobUrl.split('://')[1].split('/')
    jobUrlBehindList.insert(-1, 'ajax')
    jobUrlBehindList.insert(-1, 'content')
    jobJsUrl = jobUrlAhead + '://' + '/'.join(jobUrlBehindList)    # 完整網址
    print('\t' + jobUrl)
    print('\t' + jobJsUrl)

    headers['Referer'] = jobUrl
    articleRes = ss.get(jobJsUrl, headers=headers)    # get回來json在做整理
    jsonArticleRes = json.loads(articleRes.text)
    company = jsonArticleRes['data']['header']['custName']
    jobTitle = jsonArticleRes['data']['header']['jobName']
    jobContent = jsonArticleRes['data']['jobDetail']['jobDescription']
    jobCategoryList = [i['description'] for i in jsonArticleRes['data']['jobDetail']['jobCategory']]
    jobInfo.append([jobTitle, company, ','.join(jobCategoryList), jobContent])
    print('\t\t' + company)
    print('\t\t' + jobTitle)
    print('\t\t' + jobContent)
    print('\t\t' + ','.join(jobCategoryList))
    # print('================')
#     # time.sleep(3)
#
# print(jobInfo)

columns = ['工作職稱', '公司', '職務類別', '工作內容']
df = pd.DataFrame(data=jobInfo, columns=columns)

df.to_csv(r'./search_python.csv')


