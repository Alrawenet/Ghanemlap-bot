import os
import requests
import tweepy
from flask import Flask

app = Flask(__name__)

# تحميل المفاتيح من المتغيرات البيئية
CMC_API_KEY = os.environ.get("CMC_API_KEY")
TWITTER_API_KEY = os.environ.get("TWITTER_API_KEY")
TWITTER_API_SECRET = os.environ.get("TWITTER_API_SECRET")
TWITTER_ACCESS_TOKEN = os.environ.get("TWITTER_ACCESS_TOKEN")
TWITTER_ACCESS_SECRET = os.environ.get("TWITTER_ACCESS_SECRET")

# إعداد عميل تويتر
auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_SECRET)
auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET)
twitter_api = tweepy.API(auth)

# حفظ آخر عملة تم نشرها لتجنب التكرار
latest_coin = {"symbol": ""}

def fetch_new_coins():
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
    headers = {"X-CMC_PRO_API_KEY": CMC_API_KEY}
    params = {
        "start": "1",
        "limit": "10",
        "sort": "date_added"
    }

    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()["data"]
        return data
    else:
        print("فشل في جلب البيانات من CMC:", response.status_code)
        return []

def post_tweet(text):
    try:
        twitter_api.update_status(text)
        print("تم النشر بنجاح على تويتر.")
    except Exception as e:
        print("خطأ في النشر:", e)

@app.route("/")
def index():
    coins = fetch_new_coins()
    for coin in coins:
        symbol = coin["symbol"]
        if symbol != latest_coin["symbol"]:
            latest_coin["symbol"] = symbol
            name = coin["name"]
            slug = coin["slug"]
            cmc_rank = coin.get("cmc_rank", "N/A")
            url = f"https://coinmarketcap.com/currencies/{slug}/"
            tweet = f"🚨 عملة جديدة تم إدراجها: {name} (${symbol})\n🔹 الترتيب: {cmc_rank}\n🔗 {url}\n#كريبتو #Crypto #عملات_رقمية"
            post_tweet(tweet)
            break
    return "تم التنفيذ ✅"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
