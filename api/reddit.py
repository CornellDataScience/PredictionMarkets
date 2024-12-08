import praw
from dotenv import load_dotenv
from datetime import datetime
import os
import pandas as pd

load_dotenv()

# Initialize Reddit API
reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent=os.getenv("REDDIT_USER_AGENT"),
)

print(f"Reddit Read-Only: {reddit.read_only}")

# Define subreddit and query
politics_sub = reddit.subreddit("politics")
query = "Kamala Harris Trump election"

# Define date range
start_date = datetime(2024, 11, 1)
end_date = datetime(2024, 11, 10)
start_timestamp = start_date.timestamp()
end_timestamp = end_date.timestamp()


# Search and filter posts (Print)
for submission in politics_sub.search(query, sort="top", time_filter="month", limit=10):
    if start_timestamp <= submission.created_utc <= end_timestamp:
        print(f"Title: {submission.title}")
        print(f"Created at: {datetime.fromtimestamp(submission.created_utc)}")
        print(f"Score: {submission.score}")
        print(f"URL: {submission.url}\n")


# Search and filter posts (Save to csv)

posts_data = []

for submission in politics_sub.search(query, sort="top", time_filter="month", limit=10):
    if start_timestamp <= submission.created_utc <= end_timestamp:
        posts_data.append({
            'title': submission.title,
            'created_at': datetime.fromtimestamp(submission.created_utc),
            'score': submission.score,
            'url': submission.url
        })

df = pd.DataFrame(posts_data)
df.to_csv('data/reddit_posts_test.csv', index=False)
print(f"Saved {len(posts_data)} posts to reddit_posts.csv")

# Check approximate rate limit remaining
print(f"Rate Limit Remaining: {reddit._core._rate_limit_remaining}")
