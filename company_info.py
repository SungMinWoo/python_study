import requests
import pandas as pd
import numpy as np
import csv

from  bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from matplotlib import pyplot as plt
from matplotlib import font_manager, rc


def input_company(comp, comp_info):
    font_name = font_manager.FontProperties(fname="c:/Windows/Fonts/malgun.ttf").get_name()
    rc('font', family=font_name) #한글 폰트 깨짐 방지

    url = "https://finance.naver.com/item/main.nhn?code={}".format(comp)

    headers = {
        "User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36"
    }
    options = webdriver.ChromeOptions() #백그라운드로 실행
    options.add_argument('headless')

    res = requests.get(url, headers=headers)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "lxml")

    driver = webdriver.Chrome(options=options)
    driver.get(url) #홈페이지 접속

    year = driver.find_element_by_xpath("//*[@id='content']/div[4]/div[1]/table/thead/tr[2]")#년도 가져오기

    sales = []
    for i in range(1, 11): #매출액 부분만 추출
        sales.append(driver.find_element_by_xpath("//*[@id='content']/div[4]/div[1]/table/tbody/tr[{}]/td[{}]".format(comp_info,i)).text.replace(",","")) #,제거해야 int형으로 변환가능

    new_sales=[]
    for item in sales:
        sales_test = item.replace(' ', '0')
        new_sales.append(sales_test) #빈공간에 0을 넣어 값 표현

    if len(new_sales) < 9:
       sales.append("0")  # 리스트 맨 뒤에 값 맞추기

    #int_sales = [int(a) for a in new_sales] #list str -> list int
    int_sales = list(map(int,new_sales))#list str -> list int
    list_year = year.text.split() #공란을 기준으로 리스트로 만들기
    driver.quit()
    return list_year, int_sales, comp, comp_info

info = {1:"매출액",2:"영업이익",3:"당기순이익",4:"영업이익률",5:"순이익률",6:"ROE",7:"부채비율"}
comps, comp_infos = input(f"회사명과 알고싶은 정보의 숫자를 입력하시오\n {info}\n").split()
list_year, int_sales, comp, comp_info = input_company(comps, comp_infos)
print(int_sales)