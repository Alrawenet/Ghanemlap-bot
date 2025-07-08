import os
import logging
import tweepy
import requests
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask
from tweet_formatter import format_tweet

# إعداد السجلات
logging.basicConfig(level=logging.INFO)

# مفاتيح API من المتغيرات البيئية
CMC_API_KEY = os.getenv("CMC_API_KEY")
TWITTER_API_KEY = os.getenv("TWITTER_API_KEY")
TWITTER_API_SECRET = os.getenv("TWITTER_API_SECRET")
TWITTER_ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
TWITTER_ACCESS_SECRET = os.getenv("TWITTER_ACCESS_SECRET")

# مصادقة تويتر
auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_SECRET)
auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET)
api = tweepy.API(auth)

# التخزين المؤقت لتجنب التكرار
tweeted_ids = set()

def get_new_listings():
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
    headers = {"X-CMC_PRO_API_KEY": CMC_API_KEY}
    params = {
        "start": 1,
        "limit": 30,
        "sort": "date_added",
        "sort_dir": "desc"
    }
    try:
        response = requests.get(url, headers=headers, params=params)
        data = response.json()
        return data["data"]
    except Exception as e:
        logging.error(f"Error fetching data: {e}")
        return []

def tweet_new_coins():
    logging.info("🔁 Checking for new coins...")
    coins = get_new_listings()
    now = datetime.utcnow()
    yesterday = now - timedelta(days=1)

    for coin in coins:
        try:
            coin_id = coin["id"]
            date_added = datetime.strptime(coin["date_added"], "%Y-%m-%dT%H:%M:%S.%fZ")

            if coin_id not in tweeted_ids and date_added > yesterday:
                tweet = format_tweet(coin)
                api.update_status(tweet)
                tweeted_ids.add(coin_id)
                logging.info(f"✅ Tweeted: {coin['name']}")
        except Exception as e:
            logging.error(f"❌ Error processing coin: {e}")

# جدولة التغريد كل ساعة
def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(tweet_new_coins, "interval", hours=1)
    scheduler.start()
    logging.info("🕒 Scheduler started.")

# إعداد Flask (لـ Railway)
app = Flask(__name__)

@app.route("/")
def index():
    return "Bot is running!"

# نقطة البداية
if __name__ == "__main__":
    env = os.getenv("RAILWAY_ENVIRONMENT")

    if env == "production":
        tweet_new_coins()
        start_scheduler()
        app.run(debug=False, host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
    else:
        # GitHub Actions: تنفيذ فوري فقط
        tweet_new_coins()
