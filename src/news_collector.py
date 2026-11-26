import feedparser
import pandas as pd
from urllib.parse import quote
from pathlib import Path

#Beauty brands to track
brands=["NuFACE", "FOREO", "CurrentBody", "Therabody"]

#Empty list to store article info
articles=[]

#Fetching news articles for each brand
for brand in brands:
    print(f"Fetching news for {brand}---")

    #Create english google news RSS URL
    search_query=quote(f'"{brand}" beauty device')
    url =(
        f"https://news.google.com/rss/search?q={search_query}&hl=en-US&gl=US&ceid=US:en"
    )

    #Read RSS feed
    feed = feedparser.parse(url)

    for article in feed.entries:
        articles.append(
            {
                "brand": brand,
                "headline": article.title,
                "link": article.link,
                "published": article.get("published", ""),
            }
        )

#Convert collected articles into pandas dataframe
df=pd.DataFrame(
    articles,
    columns=["brand", "headline", "link", "published"]
)

#Remove duplicate articles within each brand
df=df.drop_duplicates(subset=["brand", "link"])

#Convert published date to datetime format
df["published"]=pd.to_datetime(df["published"], errors="coerce", utc=True)

#Sort articles from newest to oldest
df=df.sort_values(by="published", ascending=False)

#Create data folder if it doesn't exist
data_folder=Path("data")
data_folder.mkdir(exist_ok=True)

#Save results to CSV file
output_file= data_folder / "headlines.csv"
df.to_csv(output_file, index=False, encoding="utf-8-sig")

print("\nCollection Complete")
print(f"Total articles collected: {len(df)}")
print(f"Results saved to: {output_file}")

#Displaying first 5 rows
print("\nPreview:")
print(df[["brand", "headline"]].head())