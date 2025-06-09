import re
import json
import ast
import requests
from datetime import datetime
from dbOperations import store_data_in_db

# url = "https://www.tiktok.com/@capital.growth/video/7489494201114184965"

payload = {}
headers = {
  'Cookie': 'msToken=iHbNX3iGEkorwi7TvMcjzkJJ5F1AStn-gY0WifWMVBziTJRpJLW1xajKdY0dED0pMq78c8lkC336BJIC0_y2YXhjow4kUqzxt7PR; tt_chain_token=u2jQK8VvduKQ73ELTumlpQ==; tt_csrf_token=oBtskCgy-0JsY29u-rsnqka-fliOybKqrqdI; ttwid=1%7ChcuyB-OAhPz-Z3GAGf6zvbzOP7bwOImpOvLuLSCr8s4%7C1746968560%7C617f26b6d8d9a5f82492f76b847ce15bb7ff2c94eff3e8bbe42e0f4942a9aeeb',
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

# response = requests.get(url, headers=headers, data=payload)

def extract_json_from_html(html_content,url):
    result = {}

    # Extract "stats": { ... }
    stats_match = re.search(r'"stats"\s*:\s*({.*?})\s*(,|\n|\r|\})', html_content, re.DOTALL)
    if stats_match:
        try:
            stats_data = json.loads(stats_match.group(1))
            # Map TikTok stats to StockTwits format
            result['likes'] = stats_data.get('diggCount', 0)
            result['reshared_count'] = stats_data.get('shareCount', 0)
            result['comments'] = stats_data.get('commentCount', 0)
            result['play_count'] = stats_data.get('playCount', 0)
            # Convert collectCount to integer
            collect_count = stats_data.get('collectCount', '0')
            result['platform'] = "TikTok"
            result['url'] = url
            result['collect_count'] = int(collect_count) if collect_count.isdigit() else 0
        except json.JSONDecodeError:
            result['likes'] = 0
            result['reshared_count'] = 0
            result['comments'] = 0
            result['play_count'] = 0
            result['collect_count'] = 0

    # Extract "authorName": "..."
    author_match = re.search(r'"nickname"\s*:\s*"([^"]+)"', html_content)
    if author_match:
        result['username'] = author_match.group(1)

    # Extract "challenges": [ ... ]
    challenges_match = re.search(r'"challenges"\s*:\s*(\[[^\]]*?\])', html_content, re.DOTALL)
    if challenges_match:
        try:
            challenges_data = json.loads(challenges_match.group(1))
            result['hashtags'] = [c["title"] for c in challenges_data if "title" in c]
        except json.JSONDecodeError:
            result['hashtags'] = []

    # Extract "shareMeta": { ... }
    share_meta_match = re.search(r'"shareMeta"\s*:\s*({.*?})\s*(,|\n|\r|\})', html_content, re.DOTALL)
    if share_meta_match:
        try:
            share_meta = json.loads(share_meta_match.group(1))
            # Decode Unicode escape sequences in the "desc" using ast.literal_eval
            desc = share_meta.get("desc", "")
            result['description'] = ast.literal_eval(f'"{desc}"')  # safely evaluates escape sequences
        except json.JSONDecodeError:
            result['description'] = "Invalid JSON in shareMeta"

    # Add current timestamp in StockTwits format
    result['date_posted'] = datetime.now().strftime("%B %d, %Y %I:%M %p")

    return result

# Example usage

# html_content = response.text  # directly using the HTML content from the request

# cleaned_data = extract_json_from_html(html_content)
# print(json.dumps(cleaned_data, indent=4))

# # Store output in JSON file
# with open('tiktok_data.json', 'w', encoding='utf-8') as file:
#     json.dump(cleaned_data, file, indent=4, ensure_ascii=False)

# store_data_in_db(cleaned_data)

def extract_data():
    urls = [
        "https://www.tiktok.com/t/ZTjMKSuGg/",
        "https://vm.tiktok.com/ZMBchpuPm/",
        "https://www.tiktok.com/t/ZTjBHQea9/",
        "https://vm.tiktok.com/ZMB92NmmS/",
    ]
    all_results = []
    for url in urls:
        response = requests.get(url, headers=headers, data=payload)
        html_content = response.text
        cleaned_data = extract_json_from_html(html_content,url)
        print(cleaned_data)
        all_results.append(cleaned_data)
        # write the result to a file
        with open('tiktok_data.json', 'w', encoding='utf-8') as file:
            json.dump(all_results, file, indent=4, ensure_ascii=False)

    # for result in all_results:
    #     store_data_in_db(result)

if __name__ == "__main__":
    extract_data()

