import os
import tweepy
import requests
from tweet_formatter import format_single_tweet

def get_new_listings():
    cmc_key = os.getenv("CMC_API_KEY")
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
    params = {"start": "1", "limit": "5", "sort": "date_added"}
    headers = {"X-CMC_PRO_API_KEY": cmc_key}
    response = requests.get(url, headers=headers, params=params)
    data = response.json()["data"]
    return data

TWITTER_API_KEY = os.getenv("TWITTER_API_KEY")
TWITTER_API_SECRET = os.getenv("TWITTER_API_SECRET")
TWITTER_ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
TWITTER_ACCESS_SECRET = os.getenv("TWITTER_ACCESS_SECRET")

if not all([TWITTER_API_KEY, TWITTER_API_SECRET, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET]):
    raise Exception("❌ Twitter API credentials are missing from environment variables.")

auth = tweepy.OAuth1UserHandler(
    TWITTER_API_KEY,
    TWITTER_API_SECRET,
    TWITTER_ACCESS_TOKEN,
    TWITTER_ACCESS_SECRET
)
api = tweepy.API(auth)

coins = get_new_listings()
for coin in coins:
    tweet = format_single_tweet(coin)
    api.update_status(tweet)
