from patchright.sync_api import sync_playwright
import time 
import re
from datetime import datetime

def extract_facebook_data(text,url):
    # Define the regex pattern for time and reactions
    pattern = r'(\d+h|\d+m)\s*·\s*Shared with Public.*?All reactions:(\d+\.?\d*K?)(\d+)\s*comments\s*(\d+\.?\d*K?)\s*shares'
    
    # Search for the pattern in the text
    match = re.search(pattern, text, re.DOTALL)
    
    if match:
        # Extract the matched groups
        time = match.group(1)  # e.g., "3h" or "45m"
        reactions = match.group(2)
        comments = match.group(3)
        shares = match.group(4)
        
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
            'platform': 'facebook'
        }
        
        return data
    else:
        return None

def extract_page_name(url):
    """
    Extract the page name from a Facebook URL.
    Example: https://www.facebook.com/Lateefon.Ki.Dunya/posts/... -> Lateefon.Ki.Dunya
    """
    try:
        print("Original URL:", url)
        
        # Remove any query parameters and fragments
        url = url.split('?')[0].split('#')[0]
        print("URL after removing query params:", url)
        
        # Split the URL by '/' and get the part after 'facebook.com'
        parts = url.split('/')
        print("URL parts:", parts)
        
        # Find the index of 'facebook.com'
        # fb_index = parts.index('facebook.com')
        # print("Facebook.com index:", fb_index)
        
        # # Get the next part which should be the page name
        # page_name = parts[fb_index + 1]
        # print("Extracted page name:", page_name)
        
        return parts[3]
    except (ValueError, IndexError) as e:
        print("Error occurred:", str(e))
        return None

# Span and div class lists
span_classes = "x1lliihq x6ikm8r x10wlt62 x1n2onr6 xlyipyv xuxw1ft x1j85h84"
div_classes = ("x1i10hfl xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x972fbf "
               "xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r "
               "x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 "
               "x1hl2dhg xggy1nq x1a2a7pz x1heor9g xkrqix3 x1sur9pj x1s688f")

def extract_data():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=100)
        context = browser.new_context()

        # Optional: load existing login session
        page = context.new_page()

        # Go to the Facebook Reel
        # write code to get this part of url Lateefon.Ki.Dunya
        navigation_url = "https://www.facebook.com/Lateefon.Ki.Dunya/posts/pfbid09aoZuGvjsB6VwAABZa5AKj6sfJEeVPkaqEnmsgX5GjRfphjiMJM9uXwdEiCXRRDzl?rdid=fe3NyqO7ooqxRPsD#"
        page.goto(navigation_url, timeout=60000)
        # if navigation_url contains /reel then press escape key
        if "/reel" in navigation_url:
            page.keyboard.press("Escape")
            print("Escape key pressed, dialog should be closed.")
            time.sleep(10)
        
        # # Wait for the page to load manually if needed (e.g., to log in)
        # time.sleep(5)
        # # page.keyboard.press("Escape")
        # # print("Escape key pressed, dialog should be closed.")
        # # time.sleep(10)
        # print('Reactions data:')
        # reactions_data = page.query_selector("div[class*='xuk3077 x78zum5 x5yr21d x1hq5gj4 xt1id46 x1mh8g0r']")
        # print('reactions_data', reactions_data.text_content())
        # # write data in the file
        # with open('reactions_data.txt', 'w') as f:
        #     f.write(reactions_data.text_content())
        # time.sleep(5)
        # for reaction in reactions_data:
        #     print('in loop')
        #     print('reaction', reaction.text_content())
        # time.sleep(3)
        content_text = page.query_selector("div[class*='x6s0dn4 x78zum5 xdt5ytf x5yr21d xl56j7k x10l6tqk x17qophe x13vifvy xh8yej3']")
        extracted_data = extract_facebook_data(content_text.text_content(),navigation_url)
        print('extracted_data', extracted_data)
        with open('fb_data.txt', 'w') as f:
            f.write(content_text.text_content())
       
        browser.close()

if __name__ == "__main__":
    extract_data()
