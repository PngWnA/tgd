import requests
from bs4 import BeautifulSoup

base_url = "https://tgd.kr"
novideo = "Video 태그를 지원하지 않는 브라우저입니다."

class Crawler:
    def __init__(self, streamer: str):
        if streamer is None:
            raise NotFoundException("Name of the streamer is not provided")
        
        target_url = "/".join([base_url, "s", streamer])
        redirected_url = requests.get(target_url).url
        if redirected_url[:-1] == base_url: # Trim "/"
            raise NotFoundException(f"Streamer '{streamer}' is not available in tgd.kr")

        self.streamer = streamer
        self.articles = Articles()

    def load_metadata(self, pages: int = 1):
        for idx in range(1, pages+1):
            target_url = "/".join([base_url, "s", self.streamer, "page", str(idx)])
            res = requests.get(target_url).text
            
            soup = BeautifulSoup(res, "html.parser")
            articles = soup.find_all("div", "article-list-row")
            
            for article in articles:
                meta = Article()

                upvote = article.find("div", "list-header").get_text(strip=True)
                if upvote in ["인기", "공지"]:
                    continue
                meta.upvote = int(upvote, 10)

                title_meta = article.find("a")
                meta.title = title_meta["title"]
                meta.href = title_meta["href"]
                meta.id = int(title_meta["href"].split("/")[-1])
                
                cc = article.find("small", "comment-count")
                if cc is not None:
                    meta.cc = int(cc.get_text()[1:-1], 10) # Trim "[", "]"
                else:
                    meta.cc = 0

                meta.writer = article.find("div", "list-writer").get_text(strip=True)
                meta.time = article.find("div", "list-time").get_text(strip=True)
                meta.contents = None
                
                self.articles.append(meta)
        return self
            

    def verbose(self, contents=True, comments=False):
        for meta in self.articles.get():
            # Contents
            target_url = base_url + meta.href
            res = requests.get(target_url).text
            soup = BeautifulSoup(res, "html.parser")
            
            contents = soup.find("div", id="article-content").get_text().replace(novideo, "")
            meta.contents = contents
            
            time = soup.find("span", "ago").get_text(strip=True)
            meta.time = time
            
            # Comments
            if comments:
                meta.comments = list()
                comment_url = "https://tgd.kr/board/comment_load"
                target_url = "/".join([comment_url, str(meta.id)])
                res = requests.get(target_url).json()
                for comment in res["data"]:
                    cmt = Comment()
                    cmt.id = comment["id"]
                    cmt.writer = comment["nickname"]
                    cmt.time = comment["updated_at"]
                    cmt.contents = BeautifulSoup(comment["content"], "html.parser").get_text(strip=True).replace(novideo, "")
                    meta.comments.append(cmt)

        return self
                
class Article:
    def __init__(self):
        # Models for tgd.kr articles
        self.id = None
        self.title = None
        self.upvote = None
        self.href = None
        self.cc = None # comment-count
        self.writer = None
        self.time = None
        self.contents = None
        self.comments = None
    
    def __repr__(self):
        out = "|".join([self.title, self.writer, self.time])
        if self.contents is not None:
            out = "|".join([out, self.contents[:30].strip().split("\n")[0]])
        return out

class Comment:
    def __init__(self):
        self.id = None
        self.writer = None
        self.time = None
        self.contents = None
    

    def __repr__(self):
        out = "|".join([self.writer, self.contents])
        return out

class Articles:
    def __init__(self):
        # Each article metadata should have its unique id 
        self.id = list()
        self.articles = list()
        self.head = 0
    
    def __str__(self):
        out = "\n".join(map(str, self.articles))
        return out

    def get(self):
        return self.articles

    # Ignored duplicate insert problem -> re-initiate the crawler to crawl again 
    def append(self, article: Article):
        self.id.append(article.id)
        self.articles.append(article)
        return self


class NotFoundException(Exception):
    pass