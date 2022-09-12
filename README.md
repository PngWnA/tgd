# 렐
다음과 같이 의존성 설치 진행
```python
pip install -r requirement.txt
```

# 버
트게더 게시판 및 게시글 불러오기 예시: rellacast
```python
from tgd.crawler import Crawler

rella = Crawler("rellacast")
rella.load_metadata().verbose(comments=True)

for article in rella.articles:
    print(article)
    print(article.comments)
```
`Crawler(id)`로 초기화 한 후 다음과 같은 기능 사용 가능
* load_metadata: 게시물 리스트 반환
* verbose: 게시물 리스트에 있는 게시글 내용 및 댓글 불러오기

article에는 다음과 같은 정보를 포함하고 있음
* id(게시글 id), href(링크)
* title(글 제목), contents(글 내용), writer(작성자)
* upvote(추천 수), cc(댓글 갯수), time(게시 시간)

article.comments에는 다음과 같은 정보를 포함하고 있음
* id(댓글 id)
* writer(작성자), contents(글 내용)
* time(갱신 시간)

# 거

추가 예정 기능
* 특정 시간 이후 작성된 게시글만 가져오기
* 방송 공지글 분석
