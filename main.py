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
from wordcloud import WordCloud,STOPWORDS
import matplotlib.pyplot as plt

import webbrowser
import cx_Oracle
import os

def get_article(cate, date, page_cr):
    news_press = []
    news_titles = []
    news_links = []
    news_time = []
    page = 1
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
    # 명사 빈도 카운트
    noun_list = count.most_common(50)  # 상위 50개 추출

    # matplotlib 폰트설정
    from matplotlib import font_manager, rc
    import matplotlib
    from nltk import Text



    plt.rc('font', family='gulim.ttc')  # For Windows
    font_path = "C:\Windows\Fonts\HYGPRM.TTF"
    #
    # # 폰트 이름 얻어오기
    font_name = font_manager.FontProperties(fname=font_path).get_name()
    #
    # # font 설정
    matplotlib.rc('font', family=font_name)
    kolaw = Text(bindo, name="kolaw") # 그래프
    kolaw.plot(50)
    plt.show()
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

    fileName = "C:\python_workspace\wonsuppython\keyword.png"
    ndarray = img.imread(fileName)
    pp.imshow(ndarray)
    pp.show()


def ora_save():
    location = "C:\instantclient_21_3"
    os.environ["PATH"] = location + ";" + os.environ["PATH"]
    cx_Oracle.init_oracle_client(lib_dir="C:\instantclient_21_3")
    conn = cx_Oracle.connect("c##student", "student", "192.168.219.148")
    news = get_article(str(combobox.get()), str(ent3.get()), int(ent2.get()))[0]
    cursor = conn.cursor()
    query = "insert into NEWS values (:1, :2, :3, :4)"
    cursor.executemany(query, news)
    conn.commit()
    cursor.close()
    conn.close()


# gui
win = Tk()
win.title("네이버뉴스 속보 크롤링")
win.geometry("300x140")

def click():
    newWindow = Toplevel(win)
    newWindow.title("tkinter")  # 창 이름
    newWindow.geometry("500x530+200+200")  # 창 크기, 가로 x 세로 + 창 출력 위치 좌표
    newWindow.resizable(width=False, height=False)
    frame = Frame(newWindow)
    frame.pack()

    scrollbar = Scrollbar(frame)
    # fill 사용하면 스크롤바 길게 채워줌
    scrollbar.pack(side="right", fill="y")

    # set이 없으면 스크롤을 내려도 다시 올라옴
    listbox = Listbox(frame, selectmode="extended", width=70, height=30, yscrollcommand=scrollbar.set)
    listbox.pack(side="left")

    scrollbar.config(command=listbox.yview)

    titles = get_article(str(combobox.get()), str(ent3.get()), int(ent2.get()))[1]
    for item in titles[::-1]:
       listbox.insert(0, item)
    listbox.bind('<Double-Button>', click_listbox_callback)

    btn2 = Button(newWindow)
    btn2.config(text="텍스트마이닝", command=textmy)
    btn2.pack(side="right", anchor="s", pady=10, padx=10)

    btn3 = Button(newWindow)
    btn3.config(text="DB에 저장", command=ora_save)
    btn3.pack(side='bottom', anchor='e', pady=10, padx=10)

    newWindow.mainloop()
def click_listbox_callback(event):
    newslinks = get_article(str(combobox.get()), str(ent3.get()), int(ent2.get()))[2]
    index = event.widget.curselection()[0]
    webbrowser.open(newslinks[index])

# category
lab1 =Label(win)
lab1.config(text="CATE")
lab1.grid(row=0, column=0, padx=5, pady=5)
# category 입력창

values= "정치", "경제", "사회", "문화", "세계", "IT"
combobox = tkinter.ttk.Combobox(win, width=10, height=10, values=values)
combobox.current(0)
combobox.grid(row=0, column=1, padx=5, pady=5)

# page
lab2 =Label(win)
lab2.config(text="PAGE")
lab2.grid(row=1, column=0, padx=5, pady=5)

# page 입력창
ent2 = Entry(win, width=15)
def clear(event):
    if ent2.get() == "크롤링할 페이지 수":
        ent2.delete(0,len(ent2.get()))
ent2.bind("<Button-1>", clear) # 검색창 클릭시 클리어
ent2.insert(0, "크롤링할 페이지 수")
ent2.grid(row=1, column=1, padx=5, pady=5)

# date
lab3 =Label(win)
lab3.config(text="DATE")
lab3.grid(row=2, column=0, padx=5, pady=5)

# date 입력창
ent3 = Entry(win, width=15)
def clear(event):
    if ent3.get() == "YYYYMMDD":
        ent3.delete(0,len(ent3.get()))
ent3.bind("<Button-1>", clear)
ent3.insert(0, "YYYYMMDD")
ent3.grid(row=2, column=1, padx=5, pady=5)

# search button
btn1 = Button(win)
btn1.config(text = "검색", command=click)
btn1.grid(row=3, column=1, padx=5, pady=5)

# listbox

# listbox = Listbox(win, selectmode="extend", width = 70, height=33)
# listbox.config()
# listbox.grid(row=5, column=0, sticky='sw')

win.mainloop()
