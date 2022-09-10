import argparse
from tgd.crawl import get_articles

parser = argparse.ArgumentParser(description="Analyze rellacast")
parser.add_argument("-t", "--tgd", help="Get specific statistics from tgd.kr", metavar="STAT")
args = parser.parse_args()

if stat := args.tgd:
    if stat == "notice":
        articles = get_articles()
        print(articles)

