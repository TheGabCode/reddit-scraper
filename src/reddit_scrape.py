from datetime import datetime
from reddit_scraper_utils import getRedditSoup, getPostsFromFirstSoup, getPostsAfterFirstSoup, getProcessedPosts
import json
import sys, getopt
from Constants import BASE_URL, URL_AFTER_ID

sub_name = ""
sort_by = "new" # new, top, controversial, rising, hot
limit = 25
return_keys = []
verbose = False
save_to_file = True

opts, args = getopt.getopt(
    sys.argv[1:], 
    "",
    ["subreddit=","sort-by=","limit=","verbose=","save-to-file="]
)

for opt, arg in opts:
    if opt == "--subreddit":
        sub_name = arg
    elif opt == "--sort-by":
        sort_by = arg
    elif opt == "--limit":
        limit = int(arg)
    elif opt == "--verbose":
        verbose = True if arg.lower().strip() == "true" else False
    elif opt == "--save-to-file":
        save_to_file = True if arg.lower().strip() == "true" else False

filename = "{sub_name}_{sort_by}_{limit}_verbose={verbose}_{date}".format(
    sub_name=sub_name,
    sort_by=sort_by,
    limit=limit,
    verbose=verbose,
    date = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
)

post_objects_list = []
post_ids_list = []
posts_count = 0

subreddit_entered = sub_name != None and len(sub_name) > 0

while (posts_count < limit):
    if (posts_count == 0):
        url = BASE_URL
        if (subreddit_entered):
            url += "/r/{sub_name}"
            url = url.format(sub_name=sub_name)
        url += "/{sort_by}"
        url = url.format(sort_by=sort_by)
        subreddit_post_soup = getRedditSoup(url)        
        posts = getPostsFromFirstSoup(subreddit_post_soup, limit)
    else:
        remaining_limit = limit - posts_count
        if (subreddit_entered):
            url = URL_AFTER_ID.format(
                sub_name = sub_name, 
                last_id=post_ids_list[-1], 
                sort_by = sort_by
                )
        else:
            url = BASE_URL + "/{sort_by}/?after={last_id}"
            url = url.format(sort_by=sort_by, last_id=post_ids_list[-1])
            
        subreddit_post_soup = getRedditSoup(url)

        posts = getPostsAfterFirstSoup(subreddit_post_soup, remaining_limit)\
            if (subreddit_entered) else getPostsFromFirstSoup(subreddit_post_soup, remaining_limit)

    post_objects, post_ids = getProcessedPosts(
        posts, 
        return_keys=return_keys, 
        verbose=verbose
    )
    post_objects_list.extend(post_objects)
    post_ids_list.extend(post_ids)
    posts_count = len(post_objects_list)

    if (posts_count == 0):
        break
    
if (save_to_file):
    with open(filename, "w") as outfile:
        json.dump(post_objects_list, outfile, indent=4)