import os
import tweepy

# قراءة المفاتيح من متغيرات البيئة
API_KEY = os.getenv("TWITTER_API_KEY")
API_SECRET = os.getenv("TWITTER_API_SECRET")
ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
ACCESS_SECRET = os.getenv("TWITTER_ACCESS_SECRET")

# إعداد الاتصال
auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth)

# تجربة النشر
try:
    tweet = "📢 تم تشغيل بوت GhanemLap بنجاح! هذه أول تغريدة تلقائية 🚀 تابعونا لتحليل مشاريع العملات الجديدة أولاً بأول."
    api.update_status(tweet)
    print("✅ تم نشر التغريدة بنجاح.")
except tweepy.TweepyException as e:
    print(f"❌ خطأ أثناء النشر:", e)
