import requests
import praw
from enum import Enum

from utils import Post

class PostFilter(Enum):
    HOT = 1
    NEW = 2
    TOP = 3

class RedditGetter:
    def __init__(self, client_id, client_secret, user_agent) -> None:
        self.reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=user_agent,
        )

    def get_post_ids(self, subreddit=str, limit=1, filter = PostFilter.HOT):
        post_ids = []
        subreddit = self.reddit.subreddit(display_name=subreddit)
        if filter == PostFilter.HOT:
            posts = subreddit.hot(limit=limit)
        elif filter == PostFilter.NEW:
            posts = subreddit.new(limit=limit)
        elif filter == PostFilter.TOP:
            posts = subreddit.top(time_filter="all", limit=limit)
        for post in posts:
            post_ids.append(post.id)

        return post_ids



    def get_post_data(self, subreddit, post_id) -> Post:
        url = f"https://www.reddit.com/r/{subreddit}/comments/{post_id}.json"
        headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:121.0) Gecko/20100101 Firefox/121.0"}
        
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            post = Post(data)
            return post
        else:
            print(f"Error: {response.status_code}")
            return None
    
    def get_posts(self, subreddit,  limit=1, category=PostFilter.HOT) -> list[Post]:
        ls = []
        posts = self.get_post_ids(subreddit, limit, category)
        for post in posts:
            print("more")
            ls.append(self.get_post_data(subreddit, post))

        return ls
    def get_video_posts(self, subreddit,  limit=1, category=PostFilter.HOT) -> list[Post]:
        ls = []
        posts = self.get_post_ids(subreddit, 20, category)
        for post in posts:
            data = self.get_post_data(subreddit, post)
            if data.has_video:
                ls.append(data)
            if len(ls) == limit:
                return ls
        return ls


