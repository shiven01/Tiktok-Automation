import praw
import os

reddit = praw.Reddit(
        client_id = os.environ.get('REDDIT_CLIENT_ID'),
        client_secret = os.environ.get('REDDIT_CLIENT_SECRET'),
        password = os.environ.get('REDDIT_USER_PASSWORD'),
        user_agent = os.environ.get('REDDIT_USER_AGENT'),
        username = os.environ.get('REDDIT_USER_USERNAME')
        )

reddit.read_only = True

subreddit = reddit.subreddit("ClaudeAI")

print(subreddit.display_name)

submission = reddit.submission(url="https://www.reddit.com/r/ClaudeAI/comments/1e43bli/claude_is_so_good/")

# Print the title of the post
print(f"Title: {submission.title}")

# Print the text content of the post
print(f"Content: {submission.selftext}")

# Print the score (upvotes - downvotes) of the post
print(f"Score: {submission.score}")

# Print the author's name
print(f"Author: {submission.author.name}")

submission.comments.replace_more(limit=0)  # This line will load all top-level comments
for top_level_comment in submission.comments:
    print(f"Comment by {top_level_comment.author}: {top_level_comment.body}")
