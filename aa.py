from tkinter import *
import tkinter.ttk
import urllib.request
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import sys
from konlpy.tag import Okt
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import webbrowser
import oradb


def get_article(cate, date, page_cr):
    news_press = []
    news_titles = []
    news_links = []
    news_time = []
    page = 1
    # news_cat = {'1': '정치', '2': '경제', '3': '사회', '4': '문화', '5': '세계', '6': 'IT'}
    # section = news_cat[cate]
    url_section = {'정치': '100', '경제': '101', '사회': '102', '문화': '103', '세계': '104', 'IT': '105'}
    while page < page_cr + 1:
        url = 'https://news.naver.com/main/list.naver?mode=LSD&mid=sec&sid1={}&date={}&page={}'.format(url_section[cate], date, page)
        headers = {
                "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36"}
        req = requests.get(url, headers=headers)
        soup = BeautifulSoup(req.text, 'html.parser')
        for i in soup.select('div.list_body > ul > li'):
            dts = i.select('dt')
            news_titles.append(dts[-1].a.text.strip())
            news_links.append(dts[-1].a['href'])
        for i in soup.select('div.list_body > ul > li > dl > dd > span.writing'):
           news_press.append(i.text.strip())
        for i in soup.select("div.list_body > ul > li > dl > dd > span.date"):
            news_time.append(i.text.strip())
        page += 1
    news_all = list(zip(news_titles, news_links, news_press, news_time))
    return news_all, news_titles, news_links

def textmy():
    titles = get_article(str(combobox.get()), str(ent3.get()), int(ent2.get()))[1]
    strlist = ''
    for a in range(0, len(titles)):  # 뉴스 헤드라인 str로 변경
        strlist += str(titles[a])

    okt = Okt()
    noun = okt.nouns(strlist)
    bindo = []  # 형태소 분석
    for s in noun:
        if len(s) > 1:  # 1글자 이상 단어만
            bindo.append(s)
    count = Counter(bindo)  # 형태소 분석한것을 카운트
    print(count)

    # 명사 빈도 카운트
    noun_list_list = []
    noun_list = count.most_common(50)  # 상위 50개 추출
    for v in noun_list:
        noun_list_list.append(v)
    # ret = dict((x, y) for x, y in tuple1) # 딕셔너리에 담고
    # print(ret)
    # df = pd.DataFrame(list(ret.items()), columns=['words', 'freq'])
    # df.to_csv('news_freq.csv', mode='w', sep=',')

    # matplotlib 폰트설정
    plt.rc('font', family='gulim.ttc')  # For Windows
    visualize(noun_list)

def visualize(noun_list):
    import matplotlib.image as img
    import matplotlib.pyplot as pp

    wc = WordCloud(font_path='C:/Windows/Fonts/gulim.ttc',
                   background_color="white",
                   width=1000,
                   height=1000,
                   max_words=100,
                   max_font_size=300)

    wc.generate_from_frequencies(dict(noun_list))
    wc.to_file('keyword.png')

    fileName = "C:\python_workspace\crowling_naver\keyword.png"
    ndarray = img.imread(fileName)
    pp.imshow(ndarray)
    pp.show()

# gui
win = Tk()
win.title("속보 텍스트 마이닝")
win.geometry("550x700")
# win.option_add("*Font", "궁서 15")

# category
lab1 =Label(win)
lab1.config(text="CATE")
lab1.place(x= 20, y=30)
# category 입력창

values= "정치", "경제", "사회", "문화", "세계", "IT"
combobox = tkinter.ttk.Combobox(win, width=10, height=10, values=values)
combobox.current(0)
combobox.place(x= 60, y=30)

# page
lab2 =Label(win)
lab2.config(text="PAGE")
lab2.place(x = 20, y= 60)

# page 입력창
ent2 = Entry(win, width=15)
def clear(event):
    if ent2.get() == "크롤링할 페이지 수":
        ent2.delete(0,len(ent2.get()))
ent2.bind("<Button-1>", clear) # 검색창 클릭시 클리어
ent2.insert(0, "크롤링할 페이지 수")
ent2.place(x = 60, y= 60)

# date
lab3 =Label(win)
lab3.config(text="DATE")
lab3.place(x = 20, y= 90)

# date 입력창
ent3 = Entry(win, width=15)
def clear(event):
    if ent3.get() == "YYYYMMDD":
        ent3.delete(0,len(ent3.get()))
ent3.bind("<Button-1>", clear)
ent3.insert(0, "YYYYMMDD")
ent3.place(x = 60, y= 90)


def click():
    titles = get_article(str(combobox.get()), str(ent3.get()), int(ent2.get()))[1]
    for item in titles[::-1]:
        listbox.insert(0, item)

def click_listbox_callback(event):
    newslinks = get_article(str(combobox.get()), str(ent3.get()), int(ent2.get()))[2]
    index = event.widget.curselection()[0]
    webbrowser.open(newslinks[index])

# search button
btn1 = Button(win)
btn1.config(text = "크롤링", command= click)
btn1.place(x=180, y=85)


btn2 = Button(win)
btn2.config(text = "텍스트마이닝", command=textmy)
btn2.place(x=400, y=90)

btn2 = Button(win)
btn2.config(text = "DB에 저장")
btn2.place(x=300, y=90)

# listbox
listbox = Listbox(win, selectmode="extend", width = 70, height=33)
listbox.place(x=20, y=120)

listbox.bind('<Double-Button>', click_listbox_callback)

win.mainloop()


