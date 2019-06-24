import requests
from bs4 import BeautifulSoup
import json
import os
import datetime
import pymysql
import config as c

conn = pymysql.connect(host=c.host, user=c.user, password=c.password, db=c.database, charset='utf8')

curs = conn.cursor()

crawl_time = datetime.datetime(2018, 1, 1)
end_time = datetime.datetime(2019, 1, 1)
print(crawl_time,"크롤링 시작")

# print(crawl_time.year)
# print(crawl_time.month)
# print(crawl_time.day)



while(True):
  if (crawl_time == end_time):
    break
  while(True):
    req = requests.get('https://news.naver.com/main/history/mainnews/index.nhn?date='+str(crawl_time.date())+'&time='+str(crawl_time.time()))
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')

    my_title = soup.select(
      '#main_content > div.main_content_new > div > div > ul > li'
    )
    for title in my_title:
      try:
        sql = """INSERT INTO naver_news(headline, url, datetime)
            VALUES (%s, %s, %s)"""
        curs.execute(sql, (title.a.text,title.a['href'], str(crawl_time)))
        conn.commit()
        print(title.a.text)
        print(title.a['href'])
      except:
        pass
    if(str(crawl_time.time()) == "23:00:00"):
      break
    crawl_time += datetime.timedelta(hours=1)
    print(crawl_time)
  
  crawl_time += datetime.timedelta(days=1)
  crawl_time = datetime.datetime(crawl_time.year, crawl_time.month, crawl_time.day)
