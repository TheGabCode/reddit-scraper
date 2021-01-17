# reddit-scraper

## **Synopsis**
Scripts for scraping posts and comments from Reddit using `requests` Python builtin package for retrieving content and `Beautifulsoup4` for parsing data from the retrieved content.

## 1. Motivation
I hang around Reddit a lot, and I realized that Reddit is a rich source of text data which can be used for a lot of interesting data related stuff such as sentiment analysis, topic extraction, and others which I haven't really read into yet.

## 2. Demo for Post Scraping
python post_scrape.py --subreddit='MechanicalKeyboards' 'mk.json'

Arguments:<br />
--subreddit (optional) subreddit you want to scrape, defaults to reddit main feed if not specified<br />
--sort_by (optional) sort parameter in reddit, defaults to 'confidence'
--limit (optional) limit of posts to scrape<br />
--verbose (optional) returns the exact json response Reddit returns for every post (default False)<br />
filename (required)


## 3. Demo for Comment Scraping
python comment_scrape.py 'https://www.reddit.com/r/MechanicalKeyboards/comments/kz0ayl/first_time_soldering_was_a_success/' 'soldering.json'

Arguments:<br />
--sort_by (optional) sort by top, new, confidence, controversial, old, qa<br />
url (required) url of posts you want to scrape comments from<br />
filename (required)
