# 네이버 뉴스 크롤링과 텍스트 마이닝

![image](https://user-images.githubusercontent.com/102849917/166107505-2405a08d-44fd-452e-82a1-8c32f1adb89d.png)

- CATE 목록에서 뉴스의 카테고리 목록 선택 가능

- PAGE 네이버 뉴스 페이징에 따른 원하는 페이지의 량을 선택 가능

- DATE 입력한 날짜의 뉴스 선택 가능

- 뉴스 제목들을 크롤링 하여 text 창에 띄어줌


![image](https://user-images.githubusercontent.com/102849917/166107517-67a0509d-7e85-4fd7-95b0-4c432d30e716.png)

- 뉴스 제목들이 크롤링 된 text창에서 DB에 저장 버튼을 누르면 oracle에 데이터 저장


![image](https://user-images.githubusercontent.com/102849917/166107529-875714dc-0709-4149-86cf-ae4c779dc417.png)

- 뉴스 제목들이 크롤링 된
text창에서 텍스트 마이닝 버튼을 누르면 실행되는 화면

- Konlpy  모듈을 활용하여 문장을 형태소로 추출 후 1글자 이상의  중복된 단어를 카운트

- matplotlib 모듈을 활용하여 시각화 
