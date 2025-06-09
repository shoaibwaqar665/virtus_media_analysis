import requests
import json
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
from dbOperations import store_data_in_db

# Load environment variables
load_dotenv()

base_url = "https://discord.com/api/v9"

# Get token from environment variable
discord_token = os.getenv('DISCORD_TOKEN')
if not discord_token:
    raise ValueError("DISCORD_TOKEN environment variable is not set")

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:138.0) Gecko/20100101 Firefox/138.0',
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Authorization': discord_token,
}

def get_active_members_at_message(message_id, all_messages, time_window_minutes=5):
    """
    Get members who were active around the time of a specific message
    time_window_minutes: Number of minutes before and after the message to consider for activity
    """
    # Find the target message
    target_message = None
    for message in all_messages:
        if message['message_id'] == message_id:
            target_message = message
            break
    
    if not target_message:
        return []
    
    # Convert message timestamp to datetime
    message_time = datetime.strptime(target_message['timestamp'], '%Y-%m-%d %H:%M:%S')
    
    # Calculate time window
    start_time = message_time - timedelta(minutes=time_window_minutes)
    end_time = message_time + timedelta(minutes=time_window_minutes)
    
    # Get all unique members who sent messages in the time window
    active_members = set()
    for message in all_messages:
        msg_time = datetime.strptime(message['timestamp'], '%Y-%m-%d %H:%M:%S')
        if start_time <= msg_time <= end_time:
            active_members.add(message['username'])
    
    return list(active_members)

def count_messages_after(message_id, all_messages):
    """
    Count the number of messages sent after a specific message ID
    """
    found_message = False
    count = 0
    
    for message in all_messages:
        if message['message_id'] == message_id:
            found_message = True
            continue
        if found_message:
            count += 1
    
    return count if found_message else -1

def get_channel_messages(channel_id, channel_name):
    channel_url = f"{base_url}/channels/{channel_id}"
    messages_url = f"{channel_url}/messages?limit=50"
    
    # Get messages
    messages_response = requests.get(messages_url, headers=headers)
    messages_data = messages_response.json()
    
    # Clean messages
    cleaned_messages = []
    for message in messages_data:
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
            'message_id': message['id'],
            'username': username,
            'content': content.strip(),
            'timestamp': formatted_timestamp,
            'total_reactions': total_reactions,
            'channel_name': channel_name,
            'channel_id': channel_id,
            'url': url
        }
        
        cleaned_messages.append(cleaned_message)
    
    return cleaned_messages

def main():
    # Get server info using the first channel ID
    channel_id = "749484877883375626"  # Initial channel ID to get server info
    channel_url = f"{base_url}/channels/{channel_id}"
    
    # Get channel info to get guild_id
    channel_response = requests.get(channel_url, headers=headers)
    channel_data = channel_response.json()
    guild_id = channel_data.get('guild_id')
    
    # Get guild (server) info
    guild_url = f"{base_url}/guilds/{guild_id}"
    guild_response = requests.get(guild_url, headers=headers)
    guild_data = guild_response.json()
    server_name = guild_data.get('name')
    
    # Get all channels in the server
    channels_url = f"{base_url}/guilds/{guild_id}/channels"
    channels_response = requests.get(channels_url, headers=headers)
    channels_data = channels_response.json()
    
    print(f"\nServer Information:")
    print(f"Server Name: {server_name}")
    print(f"Server ID: {guild_id}")
    
    # Process messages for each channel
    all_messages = []
    # for channel in channels_data:
    channel_id = "749484877883375626"
    channel_name = "💯│testimonials"
    print(f"\nProcessing Channel: {channel_name} (ID: {channel_id})")
    
    try:
        channel_messages = get_channel_messages(channel_id, channel_name)
        all_messages.extend(channel_messages)
    except Exception as e:
        print(f"Error processing channel {channel_name}: {str(e)}")
    
    # Create final data structure
    final_data = {
        'server_name': server_name,
        'server_id': guild_id,
        'messages': all_messages,
        'platform': 'discord',
        'url': url
        
    }
    # Write the cleaned data to a file
    with open('discord_data.json', 'w', encoding='utf-8') as f:
        json.dump(final_data, f, ensure_ascii=False, indent=4)
    
    store_data_in_db(final_data)
    print(f"\nData has been saved to discord_data.json")
    
    # Example of how to use the count_messages_after function
    message_id = "1083173797089255505"
    print("\nTo count messages after a specific message, use:")
    print("count_messages_after('message_id_here', all_messages)")
    print(count_messages_after(message_id, all_messages))
    
    # Get active members at the time of the message
    active_members = get_active_members_at_message(message_id, all_messages)
    print("\nActive members at the time of the message:")
    for member in active_members:
        print(f"- {member}")

if __name__ == "__main__":
    main()

