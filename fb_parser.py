from patchright.sync_api import sync_playwright
import time 
import re
from datetime import datetime
import json

def extract_facebook_data(text,url):
    # Define the regex pattern for time and reactions
    pattern = r'All reactions:(\d+\.?\d*K?)(\d+)\s*comments\s*(\d+\.?\d*K?)\s*shares'
    
    # Search for the pattern in the text
    match = re.search(pattern, text, re.DOTALL)
   
    if match:
        # Extract the matched groups
        reactions = match.group(1)
        comments = match.group(2)
        shares = match.group(3)
        
        # Create a dictionary with the extracted data
        # convert the time in todays date and format should be April 4, 2025
        today = datetime.now().strftime("%B %d, %Y")
        page_name = extract_page_name(url)
        data = {
            'time': today,
            'reactions': reactions,
            'comments': comments,
            'shares': shares,
            'page_name': page_name,
            'platform': 'facebook',
            'url': url
        }
        
        return data
    else:
        return None


def extract_facebook_data_from_reel_response(text,url):
    """
    Extract specific data from Facebook response using regex patterns
    """
    try:
       
        
        # Try different username patterns
        username_patterns = [
            r'User\\",\\"name\\":\\"([^"]+)\\"',  # Original pattern
            r'User\\",\\"name\\":\\"([^"]+)"',    # Without trailing backslash
            r'name\\":\\"([^"]+)\\"',             # Simpler pattern
            r'name\\":\\"([^"]+)"'                # Simplest pattern
        ]
        
        username = None
        for pattern in username_patterns:
            match = re.search(pattern, text)
            if match:
                username = match.group(1)
               
                break
        
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
            # 'username': username,
            'reactions': reactions_match.group(1) if reactions_match else None,
            'comments': comments_match.group(1) if comments_match else None,
            'shares': shares_match.group(1) if shares_match else None,
            'url': url,
            'platform': 'facebook'
        }

        # Print debug information
       

        return data
    except Exception as e:
        print(f"Error extracting data: {str(e)}")
        print(f"Error type: {type(e)}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        return None

def extract_page_name(url):
  
    try:
       
        # Remove any query parameters and fragments
        url = url.split('?')[0].split('#')[0]
    
        # Split the URL by '/' and get the part after 'facebook.com'
        parts = url.split('/')
       
      
        return parts[3]
    except (ValueError, IndexError) as e:
        print("Error occurred:", str(e))
        return None

def handle_response(response, responses, reel_id,url):
    """Handle network responses and log requests"""
    try:
        # Check for the reel URL with dynamic ID
        if f"reel/{reel_id}" in response.url:
            # Get response data based on content type
            content_type = response.headers.get('content-type', '')
            
            if 'application/json' in content_type:
                response_data = response.json()
            else:
                # For non-JSON responses, get the text
                response_data = response.text()
            
            # Check if the response contains our target ID
            if reel_id in str(response_data):
                # Extract specific data from the response
                extracted_data = extract_facebook_data_from_reel_response(str(response_data),url)
                if extracted_data:
                    responses.append(extracted_data)
               
    except Exception as e:
        print(f"Error handling response from {response.url}: {str(e)}")

def extract_data():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=100)
        context = browser.new_context()

        # Enable request interception
        page = context.new_page()
        
        # List to store responses
        responses = []
        
        # Extract reel ID from the URL
        navigation_url = "https://www.facebook.com/reel/1147282673869577"
        reel_id = navigation_url.split("reel/")[-1].split("?")[0].split("#")[0]
       
        
        # Listen for network requests with the specific reel ID
        page.on("response", lambda response: handle_response(response, responses, reel_id, navigation_url))
        
        # Go to the Facebook Reel
        page.goto(navigation_url, timeout=60000)
        
        # if navigation_url contains /reel then press escape key
        if "/reel" in navigation_url:
            page.keyboard.press("Escape")
            print("Escape key pressed, dialog should be closed.")
            time.sleep(5)
            
            # Write only extracted data to file
            if responses:
                filename = f'fb_data.json'
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(responses[0], f, indent=4, ensure_ascii=False)  # Save only the first extracted data
               
            
            browser.close()
            return
        
        content_text = page.query_selector("div[class*='x6s0dn4 x78zum5 xdt5ytf x5yr21d xl56j7k x10l6tqk x17qophe x13vifvy xh8yej3']")
        extracted_data = extract_facebook_data(content_text.text_content(),navigation_url)
        
        with open('fb_data.json', 'w', encoding='utf-8') as f:
            json.dump(extracted_data, f, indent=4, ensure_ascii=False)
       
        browser.close()
        return

if __name__ == "__main__":
    extract_data()
