import os
import tweepy

# إعداد التوثيق باستخدام متغيرات البيئة
auth = tweepy.OAuth1UserHandler(
    os.getenv("TWITTER_API_KEY"),
    os.getenv("TWITTER_API_SECRET"),
    os.getenv("TWITTER_ACCESS_TOKEN"),
    os.getenv("TWITTER_ACCESS_SECRET")
)

api = tweepy.API(auth)

# نشر تغريدة اختبارية
api.update_status("✅ تغريدة اختبارية من GhanemLap-Bot - تم الاتصال بنجاح 🔁")
