import feedparser
from urllib.parse import quote

#Beauty brands to track
brands=["NuFACE", "FOREO", "CurrentBody", "Therabody"]

#Fetching news articles for each brand
for brand in brands:
    print(f"\n---News about {brand}---")

    #Create english google news RSS URL
    search_query=quote(f'"{brand}" beauty device')
    url =(
        f"https://news.google.com/rss/search?q={search_query}&hl=en-US&gl=US&ceid=US:en"
    )

    #Read RSS feed
    feed = feedparser.parse(url)

    #Display 5 headlines
    if not feed.entries:
        print("No news articles found.")
    for article in feed.entries[:5]:
        print(f"- {article.title}")