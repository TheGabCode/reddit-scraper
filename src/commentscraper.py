from bs4 import Tag, NavigableString, BeautifulSoup
import requests
import random
import json
import html
from managers.RequestManager import RequestManager

class CommentScraper:
    def __init__(self):
        self.request_manager = RequestManager()

    def parseCommentsFromDocument(self, document, get_children = False):
        comment_objects_list = []
        
        comments_container = document.find_all("div", class_=["nestedlisting"])[0]
        container_comments = comments_container.find_all("div", class_="comment")
        
        if (get_children and len(container_comments) == 1):
            return comment_objects_list
        
        first_comment = comments_container\
            .find_all("div", class_="comment")[1 if get_children else 0]
        
        comment_objects_list.append(self.extractCommentData(first_comment))
        
        for sibling in first_comment.next_siblings:
            is_tag = isinstance(sibling, Tag)
            is_comment = "comment" in sibling["class"]
            is_morechildren = "morechildren" in sibling["class"]
    
            if (is_tag and is_comment):
                comment_objects_list.append(self.extractCommentData(sibling))
            elif (is_tag and is_morechildren):
                subreddit = document\
                .find("link", {"rel":"canonical"})["href"]\
                .split("/")[4]
                
                comment_objects_list.extend(self.getMoreComments(sibling, subreddit))
        
        return comment_objects_list

    def extractCommentData(self, comment_tag, recursive=True):
        top_level_comment_object = {}
        
        score_tag = comment_tag.find("span", class_="score unvoted")
        score = score_tag["title"] if score_tag != None else "???"
        author_tag = comment_tag.find("a", class_="author")
        author = author_tag.text.strip() if author_tag != None else "[deleted]"
        
        date_posted = comment_tag.find("time", class_="live-timestamp")
        date_posted_timestamp = date_posted["datetime"]
        date_posted_readable = date_posted["title"]
        
        date_edited = comment_tag.find("time", class_="edited-timestamp")
        date_edited_timestamp = date_edited["datetime"]\
            if date_edited != None else None
        
        num_children = int(comment_tag.find("a", class_="numchildren")\
            .text.strip().replace("(", "").replace(")", "").split(" ")[0])
        
        permalink_old = comment_tag.find("a", class_="bylink")["href"]
        permalink = permalink_old.replace("old", "www", 1)
        
        comment_container = comment_tag\
            .find("div", class_="usertext-body may-blank-within md-container")\
            .find("div", class_="md")
        
        comment_formatted = comment_container.prettify()
        comment_raw = " ".join([p.text for p in comment_container.find_all("p")])\
            .strip().rstrip()
        
        top_level_comment_object["score"] = score
        top_level_comment_object["author"] = author
        top_level_comment_object["date_posted_timestamp"] = date_posted_timestamp
        top_level_comment_object["date_posted_readable"] = date_posted_readable
        top_level_comment_object["date_edited_timestamp"] = date_edited_timestamp
        top_level_comment_object["num_children"] = num_children
        top_level_comment_object["permalink_old"] = permalink_old
        top_level_comment_object["permalink"] = permalink
        top_level_comment_object["comment_formatted"] = comment_formatted
        top_level_comment_object["comment_raw"] = comment_raw
        
        if (num_children == 0 or not recursive):
            return top_level_comment_object
        else:    
            nested_soup = self.request_manager.getRedditSoup(permalink_old)
            parsed_replies = parseCommentsFromDocument(nested_soup, True)
            
            if (len(parsed_replies) == 0):
                return top_level_comment_object
            
            top_level_comment_object["replies"] = parsed_replies
                                                
            return top_level_comment_object     

    def getMoreComments(self, morecomment_tag, subreddit):
        morecomments_args = morecomment_tag.a["onclick"]\
        .replace("return morechildren", "")\
        .replace("(", "")\
        .replace(")", "")\
        .replace("'","")\
        .split(",")
        
        data_id = morecomment_tag["data-fullname"]
        link_id = morecomments_args[1].strip()
        sort = morecomments_args[2].strip()
        renderstyle = "html"
        limit_children = False
        r = subreddit
        children = ",".join(morecomments_args[3:len(morecomments_args) - 1]).strip()
        
        payload = {
            "id": data_id,
            "link_id": link_id,
            "sort": sort,
            "renderstyle": renderstyle,
            "limit_children": limit_children,
            "r": r,
            "children": children
            }
        
        more_soup = self.request_manager\
            .postRedditSoup("https://old.reddit.com/api/morechildren", payload)
        
        json_comments = json.loads(more_soup.prettify())
        json_comments_list = json_comments["jquery"][10][3][0]

        more_comments = []
        for comment in json_comments_list:
            comment_content = comment["data"]["content"]
            comment_tag_string = html.unescape(comment_content)
            comment_tag_soup = BeautifulSoup(comment_tag_string, "html.parser")
            if (comment["kind"] == "more"):
                more_comments.extend(self.getMoreComments(
                    comment_tag_soup.find("div", class_="morechildren"), subreddit)
                )
            else:            
                more_comments.append(self.extractCommentData(comment_tag_soup))
        
        return more_comments