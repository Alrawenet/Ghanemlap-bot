import os
import tweepy
from coinmarketcap import get_new_listings  # تأكد من أن هذه الدالة موجودة عندك
from tweet_formatter import format_single_tweet  # تنسيق التغريدة

# تحميل المتغيرات من البيئة
TWITTER_API_KEY = os.getenv("TWITTER_API_KEY")
TWITTER_API_SECRET = os.getenv("TWITTER_API_SECRET")
TWITTER_ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
TWITTER_ACCESS_SECRET = os.getenv("TWITTER_ACCESS_SECRET")

# تحقق من وجود المفاتيح
if not all([TWITTER_API_KEY, TWITTER_API_SECRET, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET]):
    raise Exception("❌ Twitter API credentials are missing from environment variables.")

# إعداد الاتصال بـ Twitter
auth = tweepy.OAuth1UserHandler(
    TWITTER_API_KEY,
    TWITTER_API_SECRET,
    TWITTER_ACCESS_TOKEN,
    TWITTER_ACCESS_SECRET
)
api = tweepy.API(auth)

# الحصول على العملات الجديدة
coins = get_new_listings()

# نشر تغريدة لكل عملة جديدة
for coin in coins:
    tweet = format_single_tweet(coin)
    api.update_status(tweet)
