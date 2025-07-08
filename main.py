import os
import requests
import tweepy
import datetime
from dotenv import load_dotenv
from apscheduler.schedulers.blocking import BlockingScheduler

load_dotenv()

# إعداد مفاتيح تويتر و CMC
API_KEY = os.getenv("CMC_API_KEY")
TWITTER_CONSUMER_KEY = os.getenv("TWITTER_CONSUMER_KEY")
TWITTER_CONSUMER_SECRET = os.getenv("TWITTER_CONSUMER_SECRET")
TWITTER_ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
TWITTER_ACCESS_SECRET = os.getenv("TWITTER_ACCESS_SECRET")

auth = tweepy.OAuth1UserHandler(
    TWITTER_CONSUMER_KEY,
    TWITTER_CONSUMER_SECRET,
    TWITTER_ACCESS_TOKEN,
    TWITTER_ACCESS_SECRET
)
twitter_api = tweepy.API(auth)

# قاعدة بيانات العملات التي تم تغريدها
TWEETED_DB = "tweeted_coins.txt"
if not os.path.exists(TWEETED_DB):
    with open(TWEETED_DB, "w") as f:
        pass

def load_tweeted():
    with open(TWEETED_DB, "r") as f:
        return set([line.strip() for line in f.readlines()])

def save_tweeted(coin_id):
    with open(TWEETED_DB, "a") as f:
        f.write(f"{coin_id}\n")

def get_new_coins():
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
    params = {
        "start": "1",
        "limit": "100",
        "sort": "date_added",
        "sort_dir": "desc",
        "convert": "USD"
    }
    headers = {"X-CMC_PRO_API_KEY": API_KEY}
    response = requests.get(url, params=params, headers=headers)
    data = response.json()
    return data.get("data", [])

def extract_sector(coin):
    tags = coin.get("tags", [])
    if "gaming" in tags:
        return "🎮 الألعاب"
    elif "defi" in tags:
        return "💰 التمويل اللامركزي"
    elif "ai" in tags:
        return "🤖 الذكاء الاصطناعي"
    elif "nft" in tags:
        return "🖼️ NFT"
    else:
        return "🌐 غير محدد"

def tweet_coin(coin):
    name = coin["name"]
    symbol = coin["symbol"]
    slug = coin["slug"]
    link = f"https://coinmarketcap.com/currencies/{slug}/"
    market_cap = coin.get("quote", {}).get("USD", {}).get("market_cap", "غير معروف")
    date_added = coin["date_added"][:10]
    sector = extract_sector(coin)

    tweet = f"""🚀 إدراج جديد على CoinMarketCap!

🔹 الاسم: {name} (${symbol})
📅 تاريخ الإدراج: {date_added}
📊 ماركت كاب: {int(market_cap):,}$
🧠 القطاع: {sector}
🔗 {link}

تابعونا لمزيد من العملات الجديدة يوميًا!
#عملات_رقمية #كريبتو #GhanemLap
"""
    twitter_api.update_status(tweet)

def daily_coin_tweets():
    tweeted_ids = load_tweeted()
    new_coins = get_new_coins()
    for coin in new_coins:
        if coin["id"] not in tweeted_ids:
            tweet_coin(coin)
            save_tweeted(coin["id"])

def summary_tweet(days):
    coins = get_new_coins()
    today = datetime.datetime.utcnow()
    filtered = []
    for coin in coins:
        try:
            date_added = datetime.datetime.strptime(coin["date_added"][:10], "%Y-%m-%d")
            if (today - date_added).days < days:
                filtered.append(coin)
        except:
            continue

    if not filtered:
        return

    titles = {
        1: "📅 العملات المدرجة آخر 24 ساعة",
        7: "📅 العملات المدرجة هذا الأسبوع",
        31: f"📅 العملات المدرجة في شهر {today.strftime('%B')}"
    }
    tweet = f"""{titles[days]}
✅ تم رصد {len(filtered)} عملة جديدة

🎯 للاستعراض الكامل راجع التغريدات السابقة 👇
#كريبتو #عملات_رقمية #GhanemLap
"""
    twitter_api.update_status(tweet)

# إعداد الجدولة
scheduler = BlockingScheduler()

# تغريدة تلقائية لكل عملة جديدة
scheduler.add_job(daily_coin_tweets, 'interval', hours=1)

# تلخيص كل 24 ساعة
scheduler.add_job(lambda: summary_tweet(1), 'cron', hour=0, minute=5)

# تغريدة أسبوعية (كل أحد)
scheduler.add_job(lambda: summary_tweet(7), 'cron', day_of_week='sun', hour=9, minute=0)

# تغريدة شهرية (أول يوم في الشهر)
scheduler.add_job(lambda: summary_tweet(31), 'cron', day=1, hour=9, minute=10)

if __name__ == "__main__":
    print("📡 Bot started...")
    scheduler.start()
