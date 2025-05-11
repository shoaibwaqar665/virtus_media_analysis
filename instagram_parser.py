from bs4 import BeautifulSoup
import re
import json
import requests

url = "https://www.instagram.com/p/DJfG6OizhvO/"

payload = {}
headers = {
  'Cookie': 'csrftoken=hM-q0p8Y6Q2ezYcFoF1qDu'
}

response = requests.get(url, headers=headers, data=payload)

def parse_instagram_html(html_content):
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
        
        return {
            'username': page_name,
            'likes': likes,
            'comments': comments,
            'date_posted': date_posted,
            'description': description
        }
    
    return None

# Example usage
if __name__ == "__main__":
    # Pass the content directly to the function
    html_content = response.text
    
    # Parse the HTML
    result = parse_instagram_html(html_content)
    
    if result:
        print("Page Name:", result['username'])
        print("Likes:", result['likes'])
        print("Comments:", result['comments'])
        print("Date Posted:", result['date_posted'])
        print("\nDescription:")
        print(result['description'])
    else:
        print("Failed to parse Instagram content") 

    # Store output in json file
    with open('instagram_data.json', 'w', encoding='utf-8') as file:
        json.dump(result, file, indent=4, ensure_ascii=False)
