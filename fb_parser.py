# from patchright.sync_api import sync_playwright
# import time 
# # Span and div class lists
# span_classes = "x1lliihq x6ikm8r x10wlt62 x1n2onr6 xlyipyv xuxw1ft x1j85h84"
# div_classes = ("x1i10hfl xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x972fbf "
#                "xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r "
#                "x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 "
#                "x1hl2dhg xggy1nq x1a2a7pz x1heor9g xkrqix3 x1sur9pj x1s688f")

# def extract_data():
#     with sync_playwright() as p:
#         browser = p.chromium.launch(headless=False, slow_mo=100)
#         context = browser.new_context()

#         # Optional: load existing login session
#         page = context.new_page()

#         # Go to the Facebook Reel
#         page.goto("https://www.facebook.com/reel/683361637963437", timeout=60000)

#         # Wait for the page to load manually if needed (e.g., to log in)
#         time.sleep(5)
#         page.keyboard.press("Escape")
#         print("Escape key pressed, dialog should be closed.")
#         # Get span content
#         html = page.content()
#         # print(html)
#         with open("fb_reel.html", "w") as f:
#             f.write(html)
#         time.sleep(10)
#         browser.close()

# if __name__ == "__main__":
#     extract_data()

# from PIL import Image
# import pytesseract

# image = Image.open('image.png')
# text = pytesseract.image_to_string(image)
# print(text)

import easyocr

reader = easyocr.Reader(['en'])
results = reader.readtext('image.png')

for bbox, text, prob in results:
    print(f"{text} (Confidence: {prob:.2f})")
