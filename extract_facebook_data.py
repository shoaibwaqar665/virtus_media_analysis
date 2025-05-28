import re
from datetime import datetime

def extract_facebook_data(text):
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
        data = {
            'time': today,
            'reactions': reactions,
            'comments': comments,
            'shares': shares
        }
        
        return data
    else:
        return None

def main():
    # Read text from file
    with open('fb_data.txt', 'r') as f:
        sample_text = f.read()
    
    # Extract the data
    result = extract_facebook_data(sample_text)
    
    if result:
        print("Extracted Data:")
        print(f"Time: {result['time']}")
        print(f"Reactions: {result['reactions']}")
        print(f"Comments: {result['comments']}")
        print(f"Shares: {result['shares']}")
    else:
        print("No match found in the text")

if __name__ == "__main__":
    main() 