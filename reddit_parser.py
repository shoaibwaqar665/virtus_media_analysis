import requests
import json
from dbOperations import store_data_in_db
from datetime import datetime
def extract_data():
    
    # Custom headers to avoid 429 Too Many Requests or 403 Forbidden
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    headers = {'User-Agent': 'Mozilla/5.0'}

# Custom headers to avoid 429 Too Many Requests or 403 Forbidden
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) RedditScraper/1.0"
    }

    urls = [
        "https://www.reddit.com/r/pennystocks/comments/1jewiqr/a_unique_beverage_company_caught_my_eye_and/",
        "https://www.reddit.com/r/pennystocks/comments/1jgg8bo/why_im_high_on_beverages_right_now_and_why_you/",
        "https://www.reddit.com/r/pennystocks/comments/1jpo611/hear_me_out_theres_some_recent_catalysts_on_my/",
        "https://www.reddit.com/r/pennystocks/comments/1jqhr68/after_a_fundamental_breakdown_yesterday_heres_how/",
        "https://www.reddit.com/r/pennystocks/comments/1jtkvwa/weekly_watchlist_shot_heating_up_while_prop/",
        "https://www.reddit.com/r/pennystocks/comments/1jvxtur/markets_pop_on_surprise_pause_heres_what_im/",

    ]
    all_results = []
    for url in urls:
        url = url[:-1]
        url = url + ".json"
        print(url)
        response = requests.get(url, headers=headers)
        # Parse the response and extract the data


        if response.status_code == 200:
            listings = response.json()  # This is a list
            print(listings)
            for listing in listings:
                for post in listing.get("data", {}).get("children", []):
                    post_data = post.get("data", {})
                    filtered_post = {
                        "title": post_data.get("title", ""),
                        "description": post_data.get("selftext", ""),
                        "likes": post_data.get("ups", 0),
                        "comments": post_data.get("num_comments", 0),
                        "platform": "Reddit",
                        "username": post_data.get("author", ""),
                        "url": url,
                        "scraped_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
                    if filtered_post["description"] != "":
                        all_results.append(filtered_post)
                    
        else:
            print("Failed to fetch data. Status code:", response.status_code)

        # write the result to a file
        with open('reddit_data.json', 'w', encoding='utf-8') as file:
            json.dump(all_results, file, indent=4, ensure_ascii=False)

    for result in all_results:
        store_data_in_db(result)

if __name__ == "__main__":
    extract_data()