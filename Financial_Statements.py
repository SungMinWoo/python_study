import requests
import pandas as pd
import numpy as np
from  bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from matplotlib import pyplot as plt
from matplotlib import font_manager, rc

def receive_code(comp):
    code_data = pd.read_html("http://kind.krx.co.kr/corpgeneral/corpList.do?method=download", header=0)[0]  # 파일 다운로드
    code_data = code_data[['종목코드', '회사명']]
    number = code_data.loc[code_data["회사명"] == comp, ["종목코드"]]  # 종목코드 구하기
    int_code_data = np.int64(number.values).item()
    # 숫자만 추출 타입 numpy.ndarray), int64를 int형으로 변환 (np.int16(변환할int64).item()
    six_number = '{0:06d}'.format(int_code_data)
    return six_number

def input_company(comp_code, comp_info):
    font_name = font_manager.FontProperties(fname="c:/Windows/Fonts/malgun.ttf").get_name()
    rc('font', family=font_name) #한글 폰트 깨짐 방지

    url = "https://finance.naver.com/item/main.nhn?code={}".format(comp_code)

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
    return list_year, int_sales, comp_code, comp_info

info = {1:"매출액",2:"영업이익",3:"당기순이익",4:"영업이익률",5:"순이익률",6:"ROE",7:"부채비율"}
number = input("알고싶은 정보의 숫자를 입력하시오")
comp1, comp2 = input(f"비교하고 싶은 회사 두개를 입력하시오\n {info}\n").split()

comp_code = receive_code(comp1)
comp_code1 = receive_code(comp2)

list_year, int_sales, comps, comp_info = input_company(comp_code, number)
list_year1, int_sales1, comps1, comp_info1 = input_company(comp_code1, number)

print(int_sales)
print(int_sales1)

sales_df = pd.DataFrame({comp1:int_sales,comp2:int_sales1},index=list_year)

sales_df.plot(kind='bar',color=['y','g'],figsize=(6,4))
plt.title('{}변화'.format(info.get(int(number))),fontsize=13)
plt.ylabel('{}'.format(info.get(int(number))))
#plt.savefig('매출액.png',dpi=300)
plt.show()