from wordcloud import WordCloud
import matplotlib.pyplot as plt
from konlpy.tag import Okt
from collections import Counter
#from konlpy.tag import Twitter #Okt로 바뀜

file = open('C:\\Users\\Administrator\\Desktop\\study_example\\test.txt', 'r')
a = file.read()
nlp
dat = Okt()
nouns = nlp.nouns(data)
count_word = Counter(nouns) #counter을 통해 단어마다 수를 사전형태로 변환
#tag2 = count.most_common(40) # 상위 40가지를 추출

font_path = 'C:\\Windows\\Fonts\\NanumGothic.ttf' #폰트 설정
wc = WordCloud(
    font_path = font_path, #사용할 글꼴 경로
    width = 800, #캔버스 너비
    height = 800 #캔버스 높이
    )

cloud = wc.generate_from_frequencies(dict(count_word))
fig = plt.figure(figsize=(12,12))
plt.imshow(cloud)
plt.axis("off")
plt.show()