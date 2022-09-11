from tgd.crawler import Crawler

rella = Crawler("rellacast")
rella.load_metadata().verbose(comments=True)

for article in rella.articles.get():
    print(article)
    print(article.comments)

kane = Crawler("kanetv8")
kane.load_metadata().verbose(comments=True)

for article in kane.articles.get():
    print(article)
    print(article.comments)