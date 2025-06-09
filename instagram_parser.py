from bs4 import BeautifulSoup
import re
import json
import requests
from dbOperations import store_data_in_db


def parse_instagram_html(html_content,url):
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Extract meta description which contains likes, comments, and date
    meta_description = soup.find('meta', {'name': 'description'})
    if meta_description:
        description_text = meta_description.get('content', '')
        
        # Extract likes and comments using regex
        likes_match = re.search(r'(\d+) likes', description_text)
        comments_match = re.search(r'(\d+) comments', description_text)
        
        likes = likes_match.group(1) if likes_match else '0'
        comments = comments_match.group(1) if comments_match else '0'
        
        # Extract page name - updated pattern to handle dynamic usernames
        page_name_match = re.search(r'- (\w+) on', description_text)
        page_name = page_name_match.group(1) if page_name_match else 'Unknown'
        
        # Extract date
        date_match = re.search(r'on (\w+ \d+, \d{4})', description_text)
        date_posted = date_match.group(1) if date_match else 'Unknown'
        
        # Extract description (everything after the date)
        description = description_text.split('on ' + date_posted + ': ')[-1].strip('"')
        
        # Extract hashtags using regex
        hashtags = re.findall(r'#(\w+)', description)
        
        return {
            'username': page_name,
            'likes': likes,
            'comments': comments,
            'date_posted': date_posted,
            'description': description,
            'hashtags': hashtags,
            'platform': "Instagram",
            'url': url
        }
    
    return None

# Example usage
if __name__ == "__main__":
    
    urls =["https://www.instagram.com/reel/DI_5YKJP_Ot/?igsh=N21teHpjazFpMHVs"]

    payload = {}
    headers = {
    'Cookie': 'csrftoken=hM-q0p8Y6Q2ezYcFoF1qDu'
    }
    
    all_results = []

    for url in urls:
        response = requests.get(url, headers=headers, data=payload)
        # Pass the content directly to the function
        html_content = response.text
        
        # Parse the HTML
        result = parse_instagram_html(html_content,url)
        if result:
            all_results.append(result)

            # Store output in json file
        with open('instagram_data.json', 'w', encoding='utf-8') as file:
            json.dump(all_results, file, indent=4, ensure_ascii=False)

    for result in all_results:
        store_data_in_db(result)

    
