from apify_client import ApifyClient
import json
# Initialize the ApifyClient with your Apify API token
# Replace '<YOUR_API_TOKEN>' with your token.
client = ApifyClient("apify_api_sQN7ysWc9mp2jqcug7VMuxzeF98vTp0eMzaA")

# Prepare the Actor input
run_input = {
    "startUrls": [{ "url": "https://www.facebook.com/SaeenKaPage/" }],
    "resultsLimit": 20,
}

# Run the Actor and wait for it to finish
run = client.actor("apify/facebook-posts-scraper").call(run_input=run_input)

# Fetch results
results = [item for item in client.dataset(run["defaultDatasetId"]).iterate_items()]

# Save results to a JSON file
with open("facebook_posts.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print("✅ Data saved to facebook_posts.json")
# 📚 Want to learn more 📖? Go to → https://docs.apify.com/api/client/python/docs/quick-start