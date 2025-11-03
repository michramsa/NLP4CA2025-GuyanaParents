import praw
import pandas as pd
import time
from datetime import datetime, timedelta

### This should be in any files within this folder!! ###
import sys
from pathlib import Path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
from imports import *
########################################################

from config import REDDIT_CONFIG

def explore_guyana_subreddit():
    subreddit = reddit.subreddit("Guyana")
    
    print(f"Subreddit: r/{subreddit.display_name}")
    print(f"Subscribers: {subreddit.subscribers}")
    print("\nRecent posts mentioning family/parenting:")
    
    # Search for family-related content
    for post in subreddit.search("family OR parent OR child OR upbringing OR parents OR kids", limit=5):
        print(f"\n {post.title}")
        print(f"   Score: {post.score} | Comments: {post.num_comments}")
        print(f"   Created: {datetime.fromtimestamp(post.created_utc)}")


def collect_comments_from_post(post):
    """
    Collect all comments from a specific post
    """
    comments_data = []
    
    # Expand all comment replies
    post.comments.replace_more(limit=None)
    
    # Iterate through all comments (including nested replies)
    for comment in post.comments.list():
        if hasattr(comment, 'body') and comment.body not in ['[deleted]', '[removed]']:
            comment_data = {
                'comment_id': comment.id,
                'post_id': post.id,
                'body': comment.body,
                'score': comment.score,
                'created_utc': datetime.fromtimestamp(comment.created_utc),
                'author': '[ANONYMIZED]',  # Following ethical guidelines
                'parent_id': comment.parent_id,
                'is_root': comment.parent_id == f"t3_{post.id}",  # True if direct reply to post
                'comment_depth': 0  # You can calculate depth if needed
            }
            comments_data.append(comment_data)
    
    return comments_data

def collect_family_related_posts_and_comments(subreddit_name, start_date, end_date, keywords=None):
    if keywords is None:
        keywords = [
            'parent', 'parenting', 'mother', 'father', 'mom', 'dad', 'mommy', 'daddy', 'family', 'child', 'children',
            'upbringing', 'kids', 'kid', 'were raised', 'grew up', 'raised'
        ]
    
    subreddit = reddit.subreddit(subreddit_name)
    posts_data = []
    comments_data = []
    
    start_timestamp = start_date.timestamp()
    end_timestamp = end_date.timestamp()
    
    # Search for posts with keywords
    for keyword in keywords:
        print(f"Searching for posts containing: {keyword}")
        
        for post in subreddit.search(keyword, sort='new', time_filter='all', limit=100):
            # Check if post is within timeframe
            if start_timestamp <= post.created_utc <= end_timestamp:
                # Avoid duplicates
                if post.id not in [p['post_id'] for p in posts_data]:
                    post_data = {
                        'post_id': post.id,
                        'title': post.title,
                        'selftext': post.selftext,
                        'score': post.score,
                        'num_comments': post.num_comments,
                        'created_utc': datetime.fromtimestamp(post.created_utc),
                        'search_keyword': keyword,
                        'author': '[ANONYMIZED]',
                        'subreddit': subreddit_name
                    }
                    posts_data.append(post_data)
                    
                    # Collect comments for this post
                    post_comments = collect_comments_from_post(post)
                    comments_data.extend(post_comments)
                    
                    time.sleep(2)
    
    return posts_data, comments_data

if __name__=="__main__":
    reddit = praw.Reddit(**REDDIT_CONFIG)

    # explore_guyana_subreddit()

    end_date = datetime.now()
    start_date = end_date - timedelta(days=1096)

    family_posts, family_comments = collect_family_related_posts_and_comments(
        "Guyana",
        start_date,
        end_date
    )

    # Save to CSV for analysis
    posts_df = pd.DataFrame(family_posts)
    comments_df = pd.DataFrame(family_comments)

    posts_df.to_csv('data/family_guyana_posts.csv', index=False)
    comments_df.to_csv('data/family_guyana_comments.csv', index=False)

    print(f"Collected {len(family_posts)} posts and {len(family_comments)} comments")