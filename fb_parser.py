from patchright.sync_api import sync_playwright
import time 
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
        navigation_url = "https://www.facebook.com/SaeenKaPage/posts/pfbid0wZvQ1Unxqheiv8kywG133t3upk6GrXdsZNWVuiycwycHx6D6LKymMh26NCEen8BNl"
        page.goto(navigation_url, timeout=60000)
        # if navigation_url contains /reel then press escape key
        if "/reel" in navigation_url:
            page.keyboard.press("Escape")
            print("Escape key pressed, dialog should be closed.")
            time.sleep(10)
        
        # Wait for the page to load manually if needed (e.g., to log in)
        time.sleep(5)
        # page.keyboard.press("Escape")
        # print("Escape key pressed, dialog should be closed.")
        # time.sleep(10)
        print('Reactions data:')
        reactions_data = page.query_selector("div[class*='xuk3077 x78zum5 x5yr21d x1hq5gj4 xt1id46 x1mh8g0r']")
        print('reactions_data', reactions_data.text_content())
        # write data in the file
        with open('reactions_data.txt', 'w') as f:
            f.write(reactions_data.text_content())
        time.sleep(5)
        # for reaction in reactions_data:
        #     print('in loop')
        #     print('reaction', reaction.text_content())
            

        browser.close()

if __name__ == "__main__":
    extract_data()
