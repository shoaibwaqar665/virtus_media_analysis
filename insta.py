from json import JSONDecodeError
import os
from instagrapi import Client
import json
from instagrapi.mixins.challenge import ChallengeChoice

# Define the session file path
SESSION_FILE = "session.json"

# Initialize the Client
cl = Client()
cl.set_device({"manufacturer": "samsung", "model": "SM-G973F", "android_id": "1234567890"})

# Load session if it exists
if os.path.exists(SESSION_FILE):
    cl.load_settings(SESSION_FILE)
    print("Session loaded successfully!")
else:
    # Login and save session
    cl.login("___fanny_magnet", "8667665waqar")
    cl.dump_settings(SESSION_FILE)
    print("Session saved successfully!")

# Step 1: Get user ID
username = "leanfit_gym"  # Replace with the account username
user_id = cl.user_id_from_username(username)
# print("followers",user_id.follower_count)
# Custom function to convert numeric media_id to shortcode
def media_id_to_shortcode(media_id):
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_"
    shortcode = ""
    media_id = int(media_id)
    while media_id:
        media_id, remainder = divmod(media_id, 64)
        shortcode = alphabet[remainder] + shortcode
    return shortcode

# Step 2: Fetch all media from the user
all_media = cl.user_medias(user_id, amount=10)  # Adjust the amount as needed

# Step 3: Filter, process, and save Posts/Reels to JSON
print(f"Data from {username}:")

media_list = []

try:
    for media in all_media:
        media_type = "Reel" if media.media_type == 2 else "Post"
        shortcode = media.code if hasattr(media, "code") else media_id_to_shortcode(str(media.id))
        post_url = f"https://www.instagram.com/p/{shortcode}/"

        media_data = {
            "type": media_type,
            "id": str(media.id),
            "caption": media.caption_text,
            "views": media.view_count,
            "likes": media.like_count,
            "comments": media.comment_count,
            "video_url": str(media.video_url) if media.video_url else None,
            "meta": media.clips_metadata,
            "post_url": post_url
        }

        # Print to console
        print(f"{media_type} ID: {media.id}")
        print(f"{media_type} Caption: {media.caption_text}")
        print(f"{media_type} Views: {media.view_count}")
        print(f"{media_type} Likes: {media.like_count}")
        print(f"{media_type} Comments: {media.comment_count}")
        print(f"{media_type} Video URL: {media.video_url}")
        print(f"{media_type} Meta: {media.clips_metadata}")
        print(f"{media_type} Post URL: {post_url}")
        print("-" * 50)

        media_list.append(media_data)

    # Save to JSON file
    with open(f"{username}_media.json", "w", encoding="utf-8") as f:
        json.dump(media_list, f, indent=4, ensure_ascii=False, default=str)

except JSONDecodeError:
    print("Error decoding JSON data.")
