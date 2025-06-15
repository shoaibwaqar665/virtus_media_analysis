from dbOperations import get_signal_from_db, get_urls_from_db
from fb_parser import facebook_main
from instagram_parser import instagram_main
from reddit_parser import reddit_main
from stocktwist_parser import stocktwits_main
from tiktok_parser import tiktok_main
from twitter_parser import twitter_main
from yahoo_parser import yahoo_finance_main
from discord_parser import discord_main




def main():
    signal = get_signal_from_db()
    if signal:
        print("signal", signal)
        result = get_urls_from_db()
        for platform, url in result.items():
            if platform == "X":
                twitter_main(url)
            elif platform == "Instagram":
                instagram_main(url)
            elif platform == "TikTok":
                tiktok_main(url)
            elif platform == "Facebook":
                facebook_main(url)
            elif platform == "Reddit":
                reddit_main(url)
            elif platform == "Stocktwits":
                stocktwits_main(url)
            elif platform == "Yahoo Finance":
                yahoo_finance_main(url)
            elif platform == "Discord":
                discord_main(url)

            
       
    
   

if __name__ == "__main__":
    main()