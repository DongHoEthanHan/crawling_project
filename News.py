# News.py

# 크롤링된 결과 저장용 클래스 정의 스크립트
class News:
    # 멤버변수 (field) : private 적용
    __title = ''  # 뉴스제목
    __company = '' # 언론사
    __link = '' # 링크
    __time = '' # 뉴스날짜

    #생성자
    def __init__(self, news_dict):
        self.__title = news_dict['title']
        self.__company = news_dict['company']
        self.__link = news_dict['link']
        self.__time = news_dict['time']

    # 소멸자
    def __del__(self):
        print(self, '인스턴스 소멸 됨됨')

    # 멤버함수
    def set_newstitle(self, ntitle):
        self.__title = ntitle
    def set_company(self, company):
        self.__company = company
    def set_link(self, link):
        self.__link = link
    def set_ntime(self, time):
        self.__time = time


# 해당 객체 정보를 저장할 데이터베이스 테이블 생성
# 테이블명 news
# 컬럼명은 필드명과 같게 구성
# title : pk
