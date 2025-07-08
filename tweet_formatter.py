# tweet_formatter.py

def format_tweet(coin):
    name = coin.get("name")
    symbol = coin.get("symbol")
    slug = coin.get("slug")
    date = coin.get("date_added")[:10]
    url = f"https://coinmarketcap.com/currencies/{slug}/"

    tweet = (
        f"🚨 إدراج عملة جديدة!\n\n"
        f"🔹 الاسم: {name}\n"
        f"🔹 الرمز: {symbol}\n"
        f"📆 التاريخ: {date}\n"
        f"🔗 الرابط: {url}\n\n"
        f"#كريبتو #عملات_رقمية"
    )
    return tweet
