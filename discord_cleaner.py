import json
from datetime import datetime

def clean_discord_data(file_path):
    # Read the JSON file
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    cleaned_messages = []
    
    for message in data:
        # Calculate total reactions (handle case where reactions field doesn't exist)
        total_reactions = sum(reaction['count'] for reaction in message.get('reactions', []))
        
        # Format timestamp
        timestamp = datetime.fromisoformat(message['timestamp'].replace('Z', '+00:00'))
        formatted_timestamp = timestamp.strftime('%Y-%m-%d %H:%M:%S')
        
        # Get username (prefer global_name if available, otherwise use username)
        username = message['author'].get('global_name') or message['author']['username']
        
        # Clean the content (remove mentions and extra whitespace)
        content = message['content']
        for mention in message.get('mentions', []):
            mention_text = f"<@{mention['id']}>"
            content = content.replace(mention_text, f"@{mention['username']}")
        
        # Create cleaned message dictionary
        cleaned_message = {
            'username': username,
            'content': content.strip(),
            'timestamp': formatted_timestamp,
            'total_reactions': total_reactions
        }
        
        cleaned_messages.append(cleaned_message)
    
    return cleaned_messages

def main():
    # Process the data
    cleaned_data = clean_discord_data('discord_data.json')
    
    # Print the results
    for message in cleaned_data:
        print("\n" + "="*80)
        print(f"Username: {message['username']}")
        print(f"Timestamp: {message['timestamp']}")
        print(f"Total Reactions: {message['total_reactions']}")
        print("\nContent:")
        print(message['content'])
        print("="*80)
    
    # Write the cleaned data to a file
    with open('discord_cleaned_data.json', 'w', encoding='utf-8') as f:
        json.dump(cleaned_data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    main() 