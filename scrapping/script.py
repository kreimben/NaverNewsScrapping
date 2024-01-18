'''
This script is nothing different with jupyter notebook version.
I wrote this script just for debugging.
'''

import traceback
from datetime import datetime, timedelta
from time import sleep

import pandas as pd
import requests
from bs4 import BeautifulSoup

end_date = datetime.now()
start_date = end_date - timedelta(days=2)  # 최근 3일간의 데이터를 위한 설정

end_date = end_date.strftime("%Y%m%d")
start_date = start_date.strftime("%Y%m%d")

query = '데이터분석'
url = f"https://search.naver.com/search.naver?where=news&query={query}&sm=tab_opt&sort=0&photo=0&field=0&reporter_article=&pd=3&ds={start_date}&de={end_date}&docid=&nso=so:r,p:from{start_date}to{end_date},a:all&mynews=0&refresh_start=0&related=0"
max_page = 5  # 크롤링을 원하는 최대 페이지 수 지정

# 각 기사들의 데이터를 종류별로 나눠담을 리스트를 생성합니다. (추후 DataFrame으로 모을 예정)
titles = []
dates = []
articles = []
article_urls = []
press_companies = []
categories = []
summaries_map = {}
summaries = []
category_kind = {
    '정치': 100, '경제': 101, '사회': 102, '생활/문화': 103, "세계": 104, "IT/과학": 105, '연예': 106, '스포츠': 107
}

# 지정한 기간 내 원하는 페이지 수만큼의 기사를 크롤링합니다.
current_call = 1
last_call = (max_page - 1) * 10 + 1  # max_page이 5일 경우 41에 해당 (1페이지는 url에 포함되어 있으므로 1을 빼줌)

# For error rate calulation
errors = []

# For exclude duplicated articles
visit = []

while current_call <= last_call:

    print('\n{}번째 기사글부터 크롤링을 시작합니다.'.format(current_call))

    url = "https://search.naver.com/search.naver?where=news&query=" + query \
          + "&nso=so%3Ar%2Cp%3Afrom" + start_date \
          + "to" + end_date \
          + "%2Ca%3A&start=" + str(current_call)

    web = requests.get(url).content
    source = BeautifulSoup(web, 'html.parser')

    urls_list = []
    for urls in source.find_all('a', {'class': "info"}):
        if urls["href"].startswith("https://n.news.naver.com"):
            summaries_map[urls["href"]] = source.find('a', {'class': 'api_txt_lines dsc_txt_wrap'}).get_text()
            urls_list.append(urls["href"])

    for url in urls_list:
        # 중복 기사 제거
        if url in visit:
            continue
        else:
            visit.append(url)

        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
            web_news = requests.get(url, headers=headers).content
            source_news = BeautifulSoup(web_news, 'html.parser')

            if title := source_news.find('h2', {'class': 'media_end_head_headline'}):
                title = title.get_text()
            else:
                title = source_news.find('h2', {'class': 'end_tit'}).get_text()
            print('Processing article : {}'.format(title))

            date = source_news.find('span', {'class': 'media_end_head_info_datestamp_time'}).get_text()

            article = source_news.find('article', {'id': 'dic_area'}).get_text()
            article = article.replace("\n", "")
            article = article.replace("// flash 오류를 우회하기 위한 함수 추가function _flash_removeCallback() {}", "")
            article = article.replace("동영상 뉴스       ", "")
            article = article.replace("동영상 뉴스", "")
            article = article.strip()

            press_company = source_news.find('em', {'class': 'media_end_linked_more_point'}).get_text()

            titles.append(title)
            dates.append(date)
            articles.append(article)
            press_companies.append(press_company)
            article_urls.append(url)
            summaries.append(summaries_map.get(url, ''))

            for k, v in category_kind.items():
                find = f'sid={v}'
                target = url
                if find in target:
                    categories.append(k)
                    break
            else:
                categories.append('N/A')
        except Exception as e:
            print(f'*** 다음 링크의 뉴스를 크롤링하는 중 에러가 발생했습니다 : {url}')
            print(f'에러 내용 : {e}')
            print(traceback.format_exc())
            errors.append(url)

    # 대량의 데이터를 대상으로 크롤링을 할 때에는 요청 사이에 쉬어주는 타이밍을 넣는 것이 좋습니다.
    sleep(1)
    current_call += 10

# Dataset Length Check
print(f'Titles: {len(titles)}')
print(f'Dates: {len(dates)}')
print(f'Articles: {len(articles)}')
print(f'Article URLs: {len(article_urls)}')
print(f'Press Companies: {len(press_companies)}')
if not (len(titles) == len(dates) == len(articles) == len(article_urls) == len(press_companies)):
    raise ValueError('Dataset Length is not equal')

print(f'{len(errors)} errors occured')

# 각 데이터 종류별 list에 담아둔 전체 데이터를 DataFrame에 모으고 엑셀 파일로 저장합니다.
# 파일명을 result_연도월일_시분.csv 로 지정합니다.
article_df = pd.DataFrame({
    'title': titles,
    'date': dates,
    'document': articles,
    'link': article_urls,
    'press': press_companies,
    'category': categories,
    'summary': summaries
})

article_df.to_csv(f'result_from_{start_date}_end_{end_date}.csv', index=False, encoding='utf-8')

article_df.sort_values(by='date', ascending=True)
