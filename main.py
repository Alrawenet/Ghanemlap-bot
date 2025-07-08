import os
import tweepy
from flask import Flask

app = Flask(__name__)

# جلب المفاتيح من متغيرات البيئة
API_KEY = os.getenv("TWITTER_API_KEY")
API_SECRET = os.getenv("TWITTER_API_SECRET")
ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
ACCESS_SECRET = os.getenv("TWITTER_ACCESS_SECRET")

# التحقق من وجود كل المفاتيح
missing = [k for k, v in {
    "TWITTER_API_KEY": API_KEY,
    "TWITTER_API_SECRET": API_SECRET,
    "TWITTER_ACCESS_TOKEN": ACCESS_TOKEN,
    "TWITTER_ACCESS_SECRET": ACCESS_SECRET,
}.items() if not v]

if missing:
    raise Exception(f"❌ متغيرات بيئية ناقصة: {', '.join(missing)}")

# التهيئة والمصادقة مع تويتر
auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth)

@app.route("/")
def index():
    return "✅ البوت يعمل وتم الاتصال مع Twitter API بنجاح!"

# لتجربة التغريد مباشرة:
# api.update_status("🚀 تم نشر البوت بنجاح!")

if __name__ == "__main__":
   app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

