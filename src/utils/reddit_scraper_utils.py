from bs4 import BeautifulSoup
import requests
import json

def getRedditSoup(url):
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "en-US, en; q=0.9",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.193 Safari/537.36"
    }
    response = requests.get(url, headers = headers)

    if (response.status_code != 200):
        return BeautifulSoup("", "html.parser")

    return BeautifulSoup(response.text, "html.parser")

def getPostsFromFirstSoup(first_soup, limit):
    try:
        script_data = first_soup.select('script#data')
        script_data_content = json.dumps(script_data[0].contents[0])
        script_data_content = script_data_content.replace("window.___r = ", "")
        script_data_content = json.loads(script_data_content)
        script_data_content_len = len(script_data_content)
        script_data_content = script_data_content[:script_data_content_len-1]

        script_data_dictionary = json.loads(script_data_content)
        script_data_list = list(script_data_dictionary["posts"]["models"].values())
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

def getPostsAfterFirstSoup(soup, limit):
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

def getProcessedPosts(posts, return_keys=[], verbose=False):
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