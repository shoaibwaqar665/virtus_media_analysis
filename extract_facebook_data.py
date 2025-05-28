import re

def extract_facebook_data(text):
    # Define the regex pattern
    pattern = r'All reactions:(\d+\.?\d*K?)(\d+)\s*comments\s*(\d+\.?\d*K?)\s*shares'
    
    # Search for the pattern in the text
    match = re.search(pattern, text, re.DOTALL)
    
    if match:
        # Extract the matched groups
        reactions = match.group(1)
        comments = match.group(2)
        shares = match.group(3)
        
        # Create a dictionary with the extracted data
        data = {
            # 'page_title': 'Saeen To Saeen, Saeen Ka PAGE Bhi Saeen. =p*',
            # 'post_text': 'ہندوستان کی جانب سے مسلسل ڈرون حملے،عاطف اسلم اور ساحر علی بگا راولپنڈی طلب۔۔',
            'reactions': reactions,
            'comments': comments,
            'shares': shares
        }
        
        return data
    else:
        return None

def main():
    # Sample text (you can replace this with your actual text)
    with open('fb_data.txt', 'r') as f:
        sample_text = f.read()
    
    # Extract the data
    result = extract_facebook_data(sample_text)
    
    if result:
        print("Extracted Data:")
        # print(f"Page Title: {result['page_title']}")
        # print(f"Post Text: {result['post_text']}")
        print(f"Reactions: {result['reactions']}")
        print(f"Comments: {result['comments']}")
        print(f"Shares: {result['shares']}")
    else:
        print("No match found in the text")

if __name__ == "__main__":
    main() 