import requests
from bs4 import BeautifulSoup

tgd_base = "https://tgd.kr"
novideo = "\nVideo 태그를 지원하지 않는 브라우저입니다.\n"

def get_articles(streamer="rellacast", max_pages=1, only_entries=True):
    result = []
    for idx in range(1, max_pages+1):
        target_url = "/".join([tgd_base, "s", streamer, "page", str(idx)])
        res = requests.get(target_url).text
        soup = BeautifulSoup(res, "html.parser")
        articles = soup.find_all("div", "article-list-row")
        for article in articles:
            meta = {}

            upvote = article.find("div", "list-header").get_text(strip=True)
            if upvote in ["인기", "공지"]:
                continue
            meta["upvote"] = int(upvote, 10)

            title_meta = article.find("a")
            meta["title"] = title_meta["title"]
            meta["href"] = title_meta["href"]
            meta["id"] = int(title_meta["href"].split("/")[-1])
            
            cc = article.find("small", "comment-count")
            if cc is not None:
                meta["comment-count"] = int(cc.get_text().replace("[", "").replace("]", ""), 10)
            else:
                meta["comment-count"] = 0

            meta["writer"] = article.find("div", "list-writer").get_text(strip=True)
            
            meta["time"] = article.find("div", "list-time").get_text(strip=True)

            meta["contents"] = None
            if not only_entries:
                target_url = tgd_base + meta["href"]
                res = requests.get(target_url).text
                soup = BeautifulSoup(res, "html.parser")
                
                contents = soup.find("div", id="article-content").get_text().replace(novideo, "")
                meta["contents"] = contents
                
                time = soup.find("span", "ago").get_text(strip=True)
                meta["time"] = time
                print(soup)
                input()
                comments = []
                replies = soup.find_all("div", "reply")
                print(replies)
                for reply in replies:
                    writer = reply.find("div", "reply-writer").get_text(strip=True)
                    comment = reply.find("div", "reply-content").get_text(strip=True)
                    print(writer, comment)
                
                    input()

            result.append(meta)
    return result
        
        
