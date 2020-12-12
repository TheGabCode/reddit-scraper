from bs4 import Tag, NavigableString, BeautifulSoup
import json
from managers.RequestManager import RequestManager
from commentscraper import CommentScraper
import argparse


def main():
    parser = argparse.ArgumentParser(
        description="Reddit comment scraper arguments")
    parser.add_argument("url",
                        help="Post url you want to scrape comments from")
    parser.add_argument("--sort_by", help="Sort comments by")
    parser.add_argument(
        "filename",
        help="Name of file you want to store scraped comments to")

    arguments = parser.parse_args()

    url = arguments.url
    if (url.startswith("https://www")):
        url = url.replace("www", "old", 1)
    sort_by = arguments.sort_by if arguments.sort_by else "confidence"
    url = url + "?sort={sort_by}".format(sort_by=sort_by)
    filename = arguments.filename

    request_manager = RequestManager()
    comment_scraper = CommentScraper()

    soup = request_manager.getRedditSoup(url)
    results = comment_scraper.parseCommentsFromDocument(soup)

    with open(filename, "w") as outfile:
        json.dump(results, outfile, indent=4)


if __name__ == '__main__':
    main()
