import os
import requests
import tweepy
from flask import Flask

app = Flask(__name__)

# جلب المفاتيح من متغيرات البيئة
API_KEY = os.getenv("TWITTER_API_KEY")
API_SECRET = os.getenv("TWITTER_API_SECRET")
ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
ACCESS_SECRET = os.getenv("TWITTER_ACCESS_SECRET")
CMC_API_KEY = os.getenv("CMC_API_KEY")  # مفتاح CoinMarketCap

# التحقق من وجود كل المفاتيح
missing = [k for k, v in {
    "TWITTER_API_KEY": API_KEY,
    "TWITTER_API_SECRET": API_SECRET,
    "TWITTER_ACCESS_TOKEN": ACCESS_TOKEN,
    "TWITTER_ACCESS_SECRET": ACCESS_SECRET,
    "CMC_API_KEY": CMC_API_KEY
}.items() if not v]

if missing:
    raise Exception(f"❌ متغيرات بيئة ناقصة: {', '.join(missing)}")

# تهيئة الاتصال بـ Twitter
auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth)

@app.route("/")
def index():
    return "✅ تم الاتصال بـ Twitter API و CMC API بنجاح!"

# جلب العملات الجديدة من CoinMarketCap
def get_latest_coins():
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
    headers = {
        "Accepts": "application/json",
        "X-CMC_PRO_API_KEY": CMC_API_KEY
    }
    params = {
        "limit": 5,
        "sort": "date_added"
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print("❌ خطأ في جلب البيانات من CoinMarketCap:", response.text)
        return None

# تنفيذ التغريدة عند التشغيل
data = get_latest_coins()
if data:
    tweet_text = "🆕 العملات المدرجة حديثًا على CoinMarketCap:\n\n"
    for coin in data["data"]:
        tweet_text += f"- {coin['name']} ({coin['symbol']})\n"

    try:
        api.update_status(tweet_text)
        print("✅ تم نشر التغريدة بنجاح!")
    except Exception as e:
        print("❌ خطأ أثناء النشر على تويتر:", e)

# تشغيل السيرفر (ضروري لـ Heroku أو أي خدمة مشابهة)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
