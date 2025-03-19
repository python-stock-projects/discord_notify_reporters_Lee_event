'''
追縱經濟日報 財金記者 李孟珊的新聞。
新聞網址：https://udn.com/news/reporter/MDg3MTY=
'''


import requests
from datetime import datetime
from bs4 import BeautifulSoup
import json
import os  



# 聯合新聞網
news_url = "https://udn.com/news/reporter/MDg3MTY="

# 紀錄已發送的新聞
sent_news_file = 'sent_news.json'
if os.path.exists(sent_news_file):
    with open(sent_news_file, 'r', encoding='utf-8') as f:
        sent_news = set(json.load(f))
else:
    sent_news = set()

# 紀錄上次檢查日期的文件
last_checked_date_file = 'last_checked_date.txt'
if os.path.exists(last_checked_date_file):
    with open(last_checked_date_file, 'r', encoding='utf-8') as f:
        last_checked_date = f.read().strip()
else:
    last_checked_date = datetime.now().strftime('%Y%m%d')

def save_sent_news():
    with open(sent_news_file, 'w', encoding='utf-8') as f:
        json.dump(list(sent_news), f, ensure_ascii=False, indent=4)

def save_last_checked_date(date):
    with open(last_checked_date_file, 'w', encoding='utf-8') as f:
        f.write(date)

def get_news():

    response = requests.get(news_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # 找到所有新聞的容器
    news_list = soup.find_all('div', class_='story-list__news')
    #print(news_list)
    today_news = []

    for news in news_list:
        # 提取標題
        # title_tag = news.find('h2').find('a')
        # title = title_tag.get_text()
        title_tag = news.find('h2')
        if title_tag:
            title_link = title_tag.find('a')
            if title_link:
                title = title_link.get_text()
                # print(f'title = ', title)

                # 提取部分文章開頭
                summary_tag = news.find('p')
                if summary_tag:
                    summary = summary_tag.get_text()
                    # print(f'summary = ', summary)

                    # 提取網址
                    url = title_link['href']
                    # print(f'url = ', url)   

                    # 提取日期並檢查是否為今天
                    date_tag = news.find('time')
                    # print(f'date_tag = ', date_tag)
                    if date_tag:
                        date_str = date_tag.get_text()  # 提取日期字串
                        news_date = datetime.strptime(date_str, '%Y-%m-%d %H:%M').date()
                        today_date = datetime.today().date()

                        if news_date == today_date:
                            news_id = title
                            if news_id not in sent_news:
                                sent_news.add(news_id)
                                today_news.append({'title': title, 'summary': summary, 'url': url})
            
    save_sent_news()
    return today_news



def check_news():
    global last_checked_date
    today = datetime.now().strftime('%Y%m%d')
    
    # 如果跨日，清空 sent_announcements
    if today != last_checked_date:
        sent_news.clear()
        last_checked_date = today
        save_sent_news()
        save_last_checked_date(today)

    new_news = get_news()

    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
   
    if new_news:
        # 處理新公告，例如發送通知
        print(f"有新的news - {current_time}")
  
    else:
        print(f"沒有新的news - {current_time}")

    return new_news


if __name__ == "__main__":
    check_news()

    


    

