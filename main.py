import os
import tweepy

# قراءة المفاتيح من متغيرات البيئة
API_KEY = os.getenv("TWITTER_API_KEY")
API_SECRET = os.getenv("TWITTER_API_SECRET")
ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
ACCESS_SECRET = os.getenv("TWITTER_ACCESS_SECRET")

# إعداد الاتصال باستخدام OAuth1
auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth)

# تجربة نشر تغريدة
try:
    tweet = "✅ تم الاتصال بنجاح! تجربة تغريدة من GhanemLap-Bot 🌐"
    api.update_status(tweet)
    print("✅ تم نشر التغريدة.")
except tweepy.TweepyException as e:
    print("❌ خطأ أثناء النشر:", e)
