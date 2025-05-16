import requests
import json
import os
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

channel_id = "749484877883375626"
base_url = "https://discord.com/api/v9"
channel_url = f"{base_url}/channels/{channel_id}"
messages_url = f"{channel_url}/messages?limit=50"

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

# First get channel info to get guild_id
channel_response = requests.get(channel_url, headers=headers)
channel_data = channel_response.json()
guild_id = channel_data.get('guild_id')
channel_name = channel_data.get('name')

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
print(f"\nCurrent Channel:")
print(f"Channel Name: {channel_name}")
print(f"Channel ID: {channel_id}")

print(f"\nAll Channels in Server:")
for channel in channels_data:
    print(f"Channel Name: {channel.get('name')} (ID: {channel.get('id')})")

# Get messages
messages_response = requests.get(messages_url, headers=headers)
messages_data = messages_response.json()

# Add server and channel info to the data
data_with_info = {
    'server_name': server_name,
    'server_id': guild_id,
    'channel_name': channel_name,
    'channel_id': channel_id,
    'all_channels': channels_data,
    'messages': messages_data
}

# Write the response to a file
with open('discord_data.json', 'w') as f:
    json.dump(data_with_info, f, ensure_ascii=False, indent=4)

def clean_discord_data(data):
    # Read the JSON file
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

cleaned_data = clean_discord_data(data_with_info['messages'])

# Write the cleaned data to a file
with open('discord_data.json', 'w', encoding='utf-8') as f:
    json.dump(cleaned_data, f, ensure_ascii=False, indent=4)

