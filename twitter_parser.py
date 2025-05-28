from patchright.sync_api import sync_playwright
import time
import json
from bs4 import BeautifulSoup
import re
from datetime import datetime
from dbOperations import store_data_in_db

def extract_tweet_data(url):
    username = url.split("/")[3]

    # Fetch HTML
    print("Fetching HTML")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        page.goto(url, timeout=60000)
        time.sleep(15)  # Let JS render
        html = page.content()
        browser.close()

    # Parse HTML
    soup = BeautifulSoup(html, 'html.parser')

    # 1. Extract time
    time_data = ""
    tag = soup.find('time')
    if tag:
        iso_dt = tag.get('datetime', '').strip()
        if iso_dt:
            dt_obj = datetime.strptime(iso_dt, "%Y-%m-%dT%H:%M:%S.000Z")
            time_data = dt_obj.strftime("%B %d, %Y %I:%M %p")

    # 2. Extract interactions
    most_engaged = {'replies': 0, 'reposts': 0, 'likes': 0, 'views': 0}
    for div in soup.find_all('div', attrs={'aria-label': True}):
        aria_text = div['aria-label']
        matches = re.findall(r'(\d+)\s+\b(replies|reposts|likes|views)\b', aria_text)
        interaction = {'replies': 0, 'reposts': 0, 'likes': 0, 'views': 0}
        for count, label in matches:
            interaction[label] = int(count)
        if sum(interaction.values()) > sum(most_engaged.values()):
            most_engaged = interaction

    # 3. Extract hashtags
    hashtags = []
    for a in soup.find_all('a', href=re.compile(r'^/hashtag/[^?]+')):
        match = re.search(r'^/hashtag/([^?]+)', a['href'])
        if match:
            hashtags.append(match.group(1))

    # Final JSON structure
    result = {
        "likes": most_engaged.get("likes", 0),
        "reshared_count": most_engaged.get("reposts", 0),
        "comments": most_engaged.get("replies", 0),
        "play_count": most_engaged.get("views", 0),
        "username": username,
        "hashtags": hashtags,
        "date_posted": time_data,
        "url": url,
        "platform": "Twitter",
        
    }

    # Write to file
    with open('twitter_data.json', 'w') as f:
        json.dump(result, f, indent=4, ensure_ascii=False)

    return result

# Example usage
if __name__ == "__main__":
    url = "https://x.com/PennyboisTrades/status/1917716764244181223"
    tweet_data = extract_tweet_data(url)
    print(json.dumps(tweet_data, indent=4))
    store_data_in_db(tweet_data)
