import re
from datetime import datetime
import re
from datetime import datetime

def extract_facebook_data_from_reel_response(text, url):
    """
    Extract specific data from Facebook response using regex patterns
    """
    try:
        # Updated pattern to specifically match "User","name":"Some Name"
        username_pattern = r'"User","name":"([^"]+)"'
        match = re.search(username_pattern, text)
        username = match.group(1) if match else None

        # Pattern for reactions/likes
        reactions_pattern = r'"likers":\{"count":(\d+)\}'
        # Pattern for comments
        comments_pattern = r'"total_comment_count":(\d+)'
        # Pattern for shares
        shares_pattern = r'"share_count_reduced":"(\d+)"'

        # Extract other data
        reactions_match = re.search(reactions_pattern, text)
        comments_match = re.search(comments_pattern, text)
        shares_match = re.search(shares_pattern, text)

        # Create data dictionary
        data = {
            'username': username,
            'likes': reactions_match.group(1) if reactions_match else None,
            'comments': comments_match.group(1) if comments_match else None,
            'shares': shares_match.group(1) if shares_match else None,
            'url': url,
            'platform': 'facebook',
            "scraped_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        return data

    except Exception as e:
        print(f"Error extracting data: {str(e)}")
        print(f"Error type: {type(e)}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        return None

print(extract_facebook_data_from_reel_response(open('fb_response_data_reel.txt', 'r', encoding='utf-8').read(), 'https://www.facebook.com/'))