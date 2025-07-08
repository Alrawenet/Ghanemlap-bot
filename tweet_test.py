import os
import tweepy
from dotenv import load_dotenv

# تحميل متغيرات البيئة (في حالة التشغيل المحلي)
load_dotenv()

# جلب المفاتيح من متغيرات البيئة
API_KEY = os.getenv("TWITTER_API_KEY")
API_SECRET = os.getenv("TWITTER_API_SECRET")
ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
ACCESS_SECRET = os.getenv("TWITTER_ACCESS_SECRET")

# إعداد الاتصال بـ Twitter
auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth)

# تجربة تغريدة
try:
    api.update_status("🚀 تم التفعيل بنجاح من GhanemLap")
    print("✅ تم نشر التغريدة بنجاح")
except Exception as e:
    print(f"❌ خطأ أثناء التغريد: {e}")
