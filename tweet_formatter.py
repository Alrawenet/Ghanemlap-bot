def format_single_tweet(coin):
    name = coin["name"]
    symbol = coin["symbol"]
    slug = coin["slug"]
    return f"🚨 عملة جديدة تم إدراجها: {name} (${symbol})\n🔗 https://coinmarketcap.com/currencies/{slug}/"
