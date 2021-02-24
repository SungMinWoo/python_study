import requests
import time
from selenium import webdriver
from bs4 import BeautifulSoup
from konlpy.tag import Okt
from selenium import webdriver
import pandas as pd
page_list = []
title_list = []
time_list = []

def save_scv(text, time): #csv파일 생성
    title_df_2 = pd.DataFrame(title_list.append(text), columns=['뉴스제목'])
    title_df_2['날짜'] = time.replace('.','') #날짜에 .표시 제거
    title_df_2['주가변동'] = 0

    title_df_2 = pd.concat([title_df_2])
    title_df_2.to_csv('대우조선해양_뉴스타이틀.csv', index=False, encoding='utf-8')

for page in range(50):
     page_list.append("https://search.naver.com/search.naver?&where=news&query=%EB%8C%80%EC%9A%B0%EC%A1%B0%EC%84%A0%ED%95%B4%EC%96%91&sm=tab_pge&sort=0&photo=0&field=0&reporter_article=&pd=3&ds=2019.04.01&de=2019.04.30&docid=&nso=so:r,p:from20190401to20190430,a:all&mynews=0&cluster_rank=19&start={}&refresh_start=0".format(
               str(page * 10 + 1))) #네이버 뉴스 기사 페이지 넘기기
while True:
     for page in page_list:
          res = requests.get(page, headers={'User-Agent': 'Mozilla/5.0'})
          res.raise_for_status()

          html = BeautifulSoup(res.text, 'html.parser')
          new_title = html.find_all("a", attrs={"class": "news_tit"}) #뉴스 제목 크롤링
          time = html.find_all("span", attrs={"class": "info"}) #날짜 출력
          end_croling = html.find("a", attrs={"class": "btn_next"}) #크롤링 종료를 위한 버튼 찾기

          for n, t in zip(new_title, time):  # 변수 두개 for으로 쓰기
              print("날짜 = {} 기사제목 = {}".format(t.text, n.text))
              save_scv(n.text, t.text)

          print("*"*30)
          if end_croling.get("aria-disabled") == "true":  # 다음 페이지로 넘어가는 이벤트가 없으면 정지
               break #for문을 끝내기 위한 if문

     if end_croling.get("aria-disabled") == "true":  #true면 마지막페이지 false면 활성화
          break #while문을 끝내기 위한 if문