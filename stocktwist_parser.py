import json
import re
from bs4 import BeautifulSoup
from datetime import datetime
import requests

url = "https://stocktwits.com/pbelo/message/612322988"

headers = {
    'Cookie': '_cfuvid=Qe3vptBiju_qYSeu0KnUJKNpYqw8rMFE_7ndeg0PSSU-1746971879426-0.0.1.1-604800000; auto_log_in=1; enw=1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

response = requests.get(url, headers=headers)

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
                        "likes_total": first_msg.get("likes", {}).get("total"),
                        "body": first_msg.get("body"),
                        "replies": first_msg.get("conversation", {}).get("replies"),
                        "created_at": datetime.strptime(first_msg.get("created_at"), "%Y-%m-%dT%H:%M:%SZ").strftime("%B %d, %Y %I:%M %p"),
                        "username": first_msg.get("user", {}).get("username")
                    }

                    return extracted

                except json.JSONDecodeError:
                    continue

    return {}

# Example usage
if __name__ == "__main__":
    html = response.text
    result = extract_required_data(html)
    print(json.dumps(result, indent=2, ensure_ascii=False))
