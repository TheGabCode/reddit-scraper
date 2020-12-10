import sys
import getopt
from postscraper import PostScraper

sub_name = ""
sort_by = "hot" # new, top, controversial, rising, hot
limit = 25
verbose = False

post_scraper = PostScraper()

opts, args = getopt.getopt(
    sys.argv[1:], 
    "",
    ["subreddit=","sort-by=","limit=","verbose=","filename="]
)

for opt, arg in opts:
    if opt == "--subreddit":
        sub_name = arg
    elif opt == "--sort-by":
        sort_by = arg
    elif opt == "--limit":
        limit = int(arg)
    elif opt == "--verbose":
        verbose = arg.lower().strip() == "true"
    elif opt == "--filename":
        if (len(arg.strip()) == 0):
            print("Filename can't be empty!")
        filename = arg    

post_scraper.scrapePosts(sub_name, limit, sort_by, verbose, filename)