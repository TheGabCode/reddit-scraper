from bs4 import Tag, NavigableString, BeautifulSoup
import requests
import random
import json
import html
from managers.RequestManager import RequestManager
import sys
import getopt
from commentscraper import CommentScraper

def main():
    request_manager = RequestManager()
    comment_scraper = CommentScraper()
    
    url = ""
    sort_by = "confidence"
    opts, _ = getopt.getopt(
        sys.argv[1:], 
        "",
        ["url=", "sort-by=", "filename="]
    )

    for opt, arg in opts:
        if opt == "--url":
            if (len(arg.strip()) == 0):
                print("Url can't be empty!")
            url = arg
            if (url.startswith("https://www")):
                url = url.replace("www", "old", 1)
        elif opt == "--sort-by":
            sort_by = arg if len(arg.strip()) > 0 else sort_by
            url = url + "?sort={sort_by}".format(sort_by = sort_by)
        elif opt == "--filename":
            if (len(arg.strip()) == 0):
                print("Filename can't be empty!")
            filename = arg    

    soup = request_manager.getRedditSoup(url)
    results = comment_scraper.parseCommentsFromDocument(soup)

    with open(filename, "w") as outfile:
        json.dump(results, outfile, indent=4)

if __name__ == '__main__':
    main()