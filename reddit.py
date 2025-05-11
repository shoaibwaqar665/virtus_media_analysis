import requests
import json

url = "https://www.reddit.com/r/Killtony.json"

payload = {}
headers = {
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
}

response = requests.request("GET", url, headers=headers, data=payload)

# Extract only the required fields from each post
filtered_posts = []
for post in response.json()['data']['children']:
    post_data = post['data']
    filtered_post = {
        'num_comments': post_data['num_comments'],
        'permalink': 'https://www.reddit.com' + post_data['permalink'],
        'title': post_data['title'],
        'selftext': post_data['selftext'],
        'ups': post_data['ups']
    }
    filtered_posts.append(filtered_post)

# Write filtered data to file
with open('Killtony.json', 'w') as f:
    f.write(json.dumps(filtered_posts, indent=4, ensure_ascii=False))
