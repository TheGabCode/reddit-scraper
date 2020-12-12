import argparse
from postscraper import PostScraper


def main():
    parser = argparse.ArgumentParser(
        description="Reddit post scraper arguments")
    parser.add_argument("--subreddit", help="Subreddit you want to scrape")
    parser.add_argument("--sort_by", help="Sort posts by")
    parser.add_argument("--limit", help="Number of posts to scrape")
    parser.add_argument(
        "--verbose",
        action="store_true",
        help=("If you want to save the exact same object representation scrap",
              "ed from reddit"))
    parser.add_argument("filename",
                        help="Name of file you want to store scraped data to")

    arguments = parser.parse_args()

    subreddit = arguments.subreddit if arguments.subreddit else ""
    sort_by = arguments.sort_by if arguments.sort_by else "hot"
    limit = arguments.limit if arguments.limit else 25
    verbose = arguments.verbose
    filename = arguments.filename

    post_scraper = PostScraper()
    post_scraper.scrapePosts(subreddit, limit, sort_by, verbose, filename)


if __name__ == '__main__':
    main()
