from tgd.crawler import Crawler

rella = Crawler("rellacast")
rella.load_metadata().verbose(comments=True)

for article in rella.articles:
    print(article)
    print(article.comments)