import requests
import pandas as pd
import numpy as np
from  bs4 import BeautifulSoup


def receive_code(comp):
    code_data = pd.read_html("http://kind.krx.co.kr/corpgeneral/corpList.do?method=download", header=0)[0]  # 파일 다운로드
    code_data = code_data[["회사명", "종목코드"]]
    code_data = code_data.rename(columns={'회사명': 'company', '종목코드': 'code'})
    number = code_data.loc[code_data["company"] == comp, ["code"]]  # 종목코드 구하기
    int_code_data = np.int64(number.values).item()
    # 숫자만 추출 타입 numpy.ndarray to in64
    six_number = '{0:06d}'.format(int_code_data) #종목코드 6자리로 맞추기
    return six_number

test = input("회사 이름을 입력하시오 : ")
number = receive_code(test)
print(number)




