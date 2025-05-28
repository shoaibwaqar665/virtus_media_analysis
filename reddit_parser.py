import requests
import json
from dbOperations import store_data_in_db

# Example: fetch Reddit data from a subreddit
#  remove last '/' from the url using string manipulation
url = "https://www.reddit.com/r/pennystocks/comments/1judcea/ive_developed_a_new_watchlist_of_stocks_to_keep/"
url = url[:-1]
url = url + ".json"
print(url)
headers = {'User-Agent': 'Mozilla/5.0'}

# Custom headers to avoid 429 Too Many Requests or 403 Forbidden
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) RedditScraper/1.0"
}

response = requests.get(url, headers=headers)

# Parse the response and extract the data
filtered_posts = []

if response.status_code == 200:
    listings = response.json()  # This is a list
    for listing in listings:
        for post in listing.get("data", {}).get("children", []):
            post_data = post.get("data", {})
            filtered_post = {
                "title": post_data.get("title", ""),
                "description": post_data.get("selftext", ""),
                "likes": post_data.get("ups", 0),
                "comments": post_data.get("num_comments", 0),
                "platform": "Reddit"
            }
            filtered_posts.append(filtered_post)
else:
    print("Failed to fetch data. Status code:", response.status_code)
# Print extracted posts
print(filtered_posts[0])

# Write the filtered posts to a JSON file
with open('reddit_data.json', 'w') as f:
    json.dump(filtered_posts[0], f, indent=4, ensure_ascii=False)

store_data_in_db(filtered_posts[0])