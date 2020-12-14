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
    sort_by = arguments.sort_by if arguments.sort_by else "confidence"
    filename = arguments.filename

    comment_scraper = CommentScraper()
    results = comment_scraper.scrape_comments(url, sort_by)

    with open(filename, "w") as outfile:
        json.dump(results, outfile, indent=4)


if __name__ == '__main__':
    main()
