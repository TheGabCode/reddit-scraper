from managers.RequestManager import RequestManager
from bs4 import BeautifulSoup
import requests
import json
from common.Constants import URL_AFTER_ID, BASE_URL

class PostScraper:
    def __init__(self):
        self.request_manager = RequestManager()

    def __getPostsFromFirstSoup(self, first_soup, limit):
        try:
            script_data = first_soup.select('script#data')
            script_data_content = json.dumps(script_data[0].contents[0])
            script_data_content = script_data_content\
                .replace("window.___r = ", "")
            script_data_content = json.loads(script_data_content)
            script_data_content_len = len(script_data_content)
            script_data_content = script_data_content\
                [:script_data_content_len-1]

            script_data_dictionary = json.loads(script_data_content)
            script_data_list = list(script_data_dictionary["posts"]["models"]\
                .values())
            filtered_list = [
                post for post in script_data_list 
                    if post['belongsTo']['type'] == 'subreddit' and not 
                        post['isStickied'] and 
                        post['crosspostParentId'] == None
                        ]

            if (len(filtered_list) < limit):
                return filtered_list
            return filtered_list[:limit]
        except IndexError:
            return []

    def __getPostsAfterFirstSoup(self, soup, limit):
        post_list = list(json.loads(soup.text)["posts"].values())
        filtered_list = [
            post for post in post_list 
                if post["belongsTo"]["type"] == "subreddit" and not 
                    post["isStickied"] and 
                    post["crosspostParentId"] == None
                    ] 
        
        if (len(filtered_list) < limit):
            return filtered_list
        
        return filtered_list[:limit]

    def __getProcessedPosts(self, posts, return_keys=[], verbose=False):
        post_objects = []
        post_ids = []

        for value in posts:            
            post_object = {}
            if (len(return_keys) > 0):
                for return_key in return_keys:
                    post_object[return_key] = value[return_key]
            elif (verbose):
                post_object = value
            else:
                post_object["id"] = value["id"]
                post_object["title"] = value["title"]
                post_object["numComments"] = value["numComments"]
                post_object["created"] = value["created"]
                post_object["score"] = value["score"]
                post_object["author"] = value["author"]
                post_object["upvoteRatio"] = value["upvoteRatio"]
                post_object["permalink"] = value["permalink"]
                post_object["media"] = value["media"]

            post_ids.append(value["id"])
            post_objects.append(post_object)
            
        return post_objects, post_ids

    def scrapePosts(self, subreddit, limit, sort_by, verbose, filename):
        post_objects_list = []
        post_ids_list = []
        posts_count = 0

        subreddit_entered = subreddit != None and len(subreddit) > 0

        while (posts_count < limit):
            if (posts_count == 0):
                url = BASE_URL
                if (subreddit_entered):
                    url += "/r/{sub_name}"
                    url = url.format(sub_name=subreddit)
                url += "/{sort_by}"
                url = url.format(sort_by=sort_by)
                
                subreddit_post_soup = self.request_manager.getRedditSoup(url)        
                posts = self.__getPostsFromFirstSoup(
                    subreddit_post_soup, 
                    limit
                )
            else:
                remaining_limit = limit - posts_count
                if (subreddit_entered):
                    url = URL_AFTER_ID.format(
                        sub_name = subreddit, 
                        last_id=post_ids_list[-1], 
                        sort_by = sort_by
                        )
                else:
                    url = BASE_URL + "/{sort_by}/?after={last_id}"
                    url = url.format(
                        sort_by=sort_by, 
                        last_id=post_ids_list[-1]
                    )
                    
                subreddit_post_soup = self.request_manager.getRedditSoup(url)

                posts = self.__getPostsAfterFirstSoup(
                    subreddit_post_soup, 
                    remaining_limit
                    )\
                    if (subreddit_entered) else self.__getPostsFromFirstSoup(
                        subreddit_post_soup, 
                        remaining_limit
                    )

            post_objects, post_ids = self.__getProcessedPosts(
                posts, 
                return_keys=[], 
                verbose=verbose
            )
            post_objects_list.extend(post_objects)
            post_ids_list.extend(post_ids)
            posts_count = len(post_objects_list)

            if (posts_count == 0):
                break
            
            with open(filename, "w") as outfile:
                json.dump(post_objects_list, outfile, indent=4)