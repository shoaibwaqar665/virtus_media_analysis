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
        time.sleep(5)  # Let JS render
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
        "shares": most_engaged.get("reposts", 0),
        "comments": most_engaged.get("replies", 0),
        "play_count": most_engaged.get("views", 0),
        "username": username,
        "hashtags": hashtags,
        "date_posted": time_data,
        "url": url,
        "platform": "X",
        "scraped_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    return result

# Example usage
if __name__ == "__main__":
    all_results = []
    urls = [
        "https://x.com/PennyboisTrades/status/1902002822889046497",
        "https://x.com/PennyboisTrades/status/1902768934673113535",
        "https://twitter.com/PennyboisTrades/status/1904618833198903426",
        "https://x.com/PennyboisTrades/status/1906759729105285571",
        "https://x.com/PennyboisTrades/status/1909300117187813393",
        "https://x.com/MrStockLockPro1/status/1911846302947951071",
        "https://x.com/PennyboisTrades/status/1915489929724862504",
        "https://x.com/MrStockLockPro1/status/1918420993141362894",
        "https://x.com/PennyboisTrades/status/1919767580815868165?t=EqOYQg_as6igj0kE5F-psQ&s=19",
        "https://x.com/PennyboisTrades/status/1922337413546049885",
        "https://x.com/PennyboisTrades/status/1902040300274503850",
    ]
    for url in urls:
        tweet_data = extract_tweet_data(url)
        if tweet_data:
            all_results.append(tweet_data)
    if all_results:
        filename = f'twitter_data.json'
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(all_results, f, indent=4, ensure_ascii=False)

        for result in all_results:
            store_data_in_db(result)
