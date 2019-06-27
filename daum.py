import requests
from bs4 import BeautifulSoup
import json
import os
import datetime
import pymysql
import config as c

conn = pymysql.connect(host=c.host, user=c.user, password=c.password, db=c.database, charset='utf8')

curs = conn.cursor()

crawl_time = datetime.datetime(2017, 5, 4)
end_time = datetime.datetime(2018, 1, 1)
print(crawl_time,"크롤링 시작")

while(True):
  print(crawl_time.strftime("%Y%m%d"))
  if (crawl_time.strftime("%Y%m%d") == end_time.strftime("%Y%m%d")):
    break
  page = 1
  while(True):
    print("페이지: "+str(page))
    req = requests.get('https://media.daum.net/newsbox/?page='+str(page)+'&tab_cate=NE&regDate='+crawl_time.strftime("%Y%m%d"))
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')

    is_end_page = soup.select(
      '#mArticle > p'
    )

    if (len(is_end_page)==1):
      print("This is last the page.")
      break
    else:
      articles = soup.select(
        '#mArticle > div.box_etc.etc_arrange > ul > li'
      )
      for article in articles:
        try:
          sql = """INSERT INTO daum_news(headline, url, source, datetime)
              VALUES (%s, %s, %s, %s)"""
          curs.execute(sql, (article.strong.a.text, article.strong.a['href'], article.span.text, str(crawl_time)))
          conn.commit()
          print(article.strong.a.text)
          print(article.strong.a['href'])
          print(article.span.text)
        except:
          pass
      page += 1
  
  crawl_time += datetime.timedelta(days=1)