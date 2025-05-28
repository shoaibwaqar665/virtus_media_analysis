import requests

PAGE_ID = "40796308305"
ACCESS_TOKEN = "EAAKaI7xnyj0BO8bwh9FZAmnN8LYV3L2KJpNsQMJbxvHSRYBIdGZCe8cshBFZALju08aoCgDjYGWCBVPdTV5RdxZASHKN1TODd8UmC5y7FGKb0BpBRfsHuWNirtut6gYeNzbPMh0ZBTqqfoPSz3sXamdquZCHe6vM4yHqJwUWCM8ZAOuR1lUMuhD3pZA0bJZCxYpg7v7xCsSZCWMFCXjA9UPE7hkyzDs8JR9wZDZD"

url = f"https://graph.facebook.com/v18.0/{PAGE_ID}/posts"
params = {
    "access_token": ACCESS_TOKEN,
    "fields": "id,message,created_time,permalink_url,"
              "comments.summary(true),likes.summary(true),shares"
}

res = requests.get(url, params=params)

if res.ok:
    data = res.json().get("data", [])
    for post in data:
        print("Post ID:", post.get("id"))
        print("Message:", post.get("message"))
        print("Created Time:", post.get("created_time"))
        print("Link:", post.get("permalink_url"))

        # Safely extract counts
        comments_count = post.get("comments", {}).get("summary", {}).get("total_count", 0)
        likes_count = post.get("likes", {}).get("summary", {}).get("total_count", 0)
        shares_count = post.get("shares", {}).get("count", 0)

        print("Likes:", likes_count)
        print("Comments:", comments_count)
        print("Shares:", shares_count)
        print("-" * 50)
else:
    print(f"Error: {res.status_code}")
    print(res.text)
