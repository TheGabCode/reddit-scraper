from bs4 import Tag, NavigableString, BeautifulSoup
import requests
import random
import json
import html
from managers.RequestManager import RequestManager
import sys
import getopt
from commentscraper import CommentScraper
import argparse

def main():
    # url = ""
    # sort_by = "confidence"
    # opts, _ = getopt.getopt(
    #     sys.argv[1:], 
    #     "",
    #     ["url=", "sort-by=", "filename="]
    # )

    # for opt, arg in opts:
    #     if opt == "--url":
    #         if (len(arg.strip()) == 0):
    #             print("Url can't be empty!")
    #         url = arg
    #         if (url.startswith("https://www")):
    #             url = url.replace("www", "old", 1)
    #     elif opt == "--sort-by":
    #         sort_by = arg if len(arg.strip()) > 0 else sort_by
    #         url = url + "?sort={sort_by}".format(sort_by = sort_by)
    #     elif opt == "--filename":
    #         if (len(arg.strip()) == 0):
    #             print("Filename can't be empty!")
    #         filename = arg    

    parser = argparse.ArgumentParser(
        description="Reddit comment scrape arguments"
    )
    parser.add_argument(
        "url", 
        help="Post url you want to scrape comments from"
    )
    parser.add_argument("--sort_by", help="Sort comments by")
    parser.add_argument(
        "filename", 
        help="Name of file you want to store scraped comments to"
    )

    arguments = parser.parse_args()

    url = arguments.url
    if (url.startswith("https://www")):
        url = url.replace("www", "old", 1)
    sort_by = arguments.sort_by if arguments.sort_by else "confidence"
    url = url + "?sort={sort_by}".format(sort_by = sort_by)
    filename = arguments.filename

    request_manager = RequestManager()
    comment_scraper = CommentScraper()

    soup = request_manager.getRedditSoup(url)
    results = comment_scraper.parseCommentsFromDocument(soup)

    with open(filename, "w") as outfile:
        json.dump(results, outfile, indent=4)

if __name__ == '__main__':
    main()