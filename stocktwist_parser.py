import json
import re
from bs4 import BeautifulSoup
from datetime import datetime
import requests
from dbOperations import store_data_in_db

url = "https://stocktwits.com/pbelo/message/612322988"

payload = {}
headers = {
  'Cookie': '_cfuvid=Qe3vptBiju_qYSeu0KnUJKNpYqw8rMFE_7ndeg0PSSU-1746971879426-0.0.1.1-604800000; auto_log_in=1; enw=1',
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

response = requests.request("GET", url, headers=headers, data=payload)

# write the response to a file
with open('stocktwits.html', 'w') as f:
    f.write(response.text)

def extract_required_data(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    script_tags = soup.find_all("script")

    for script in script_tags:
        if script.string and '"pageProps"' in script.string:
            json_match = re.search(r'({.*"pageProps".*})', script.string, re.DOTALL)
            if json_match:
                try:
                    data = json.loads(json_match.group(1))
                    page_props = data.get("props", {}).get("pageProps", {})
                    messages = (
                        page_props.get("initialData", {})
                                  .get("threading", {})
                                  .get("messages", {})
                    )

                    first_msg = next(iter(messages.values()), None)
                    if not first_msg:
                        return {}

                    extracted = {
                        "reshared_count": first_msg.get("reshares", {}).get("reshared_count"),
                        "likes": first_msg.get("likes", {}).get("total"),
                        "description": first_msg.get("body"),
                        "comments": first_msg.get("conversation", {}).get("replies"),
                        "date_posted": datetime.strptime(first_msg.get("created_at"), "%Y-%m-%dT%H:%M:%SZ").strftime("%B %d, %Y %I:%M %p"),
                        "username": first_msg.get("user", {}).get("username"),
                        "platform": "StockTwits"
                    }
                    

                    return extracted

                except json.JSONDecodeError:
                    continue

    return {}

# Example usage
if __name__ == "__main__":
    with open("stocktwits.html", "r", encoding="utf-8") as f:
        html = f.read()

    result = extract_required_data(html)
    print(json.dumps(result, indent=4, ensure_ascii=False))
    # write the result to a file
    with open("stocktwist_data.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=4, ensure_ascii=False)
    store_data_in_db(result)

