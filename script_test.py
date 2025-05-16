import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

channel_id = "749484877883375626"
base_url = "https://discord.com/api/v9"
channel_url = f"{base_url}/channels/{channel_id}"
messages_url = f"{channel_url}/messages?limit=100"
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

# Get guild (server) info
guild_url = f"{base_url}/guilds/{guild_id}"
guild_response = requests.get(guild_url, headers=headers)
guild_data = guild_response.json()
server_name = guild_data.get('name')

print(f"Server Name: {server_name}")

# Get messages
messages_response = requests.get(messages_url, headers=headers)
messages_data = messages_response.json()

# Add server name to the data
data_with_server = {
    'server_name': server_name,
    'messages': messages_data
}

# Write the response to a file
with open('discord_data.json', 'w') as f:
    json.dump(data_with_server, f, ensure_ascii=False, indent=4)
