import streamlit as st
import pandas as pd
from pathlib import Path

#Dashboard title
st.title("Beauty-Tech News Sentiment Tracker")
st.write("Tracking news sentiment for FOREO, NuFACE, CurrentBody, and Therabody.")

#Load sentiment results
data_file = Path("data/sentiment_results.csv")

if not data_file.exists():
    st.error("No data found. Please run the sentiment analyzer first.")
    st.stop()

df = pd.read_csv(data_file)

if df.empty:
    st.warning("The dataset is empty.")
    st.stop()

#Convert publication dates into datetime format
df["published"] = pd.to_datetime(
    df["published"],
    errors="coerce",
    utc=True
)

#Dashboard summary
st.header("Overview")

col1, col2, col3 = st.columns(3)

col1.metric("Total Articles", len(df))
col2.metric("Brands Tracked", df["brand"].nunique())
col3.metric("Positive Articles", (df["sentiment"] == "positive").sum())

#Sentiment by brand
st.header("Sentiment by Brand")

sentiment_counts = pd.crosstab(
    df["brand"],
    df["sentiment"]
)

st.bar_chart(sentiment_counts)

#Articles published per week
st.header("Articles per Week")

weekly_articles = (
    df.dropna(subset=["published"])
    .set_index("published")
    .resample("W")
    .size()
)

st.line_chart(weekly_articles)

#Latest news articles
st.header("Latest Articles")

latest_articles = df.sort_values(
    "published",
    ascending=False
)

st.dataframe(
    latest_articles[
        ["brand", "headline", "sentiment", "confidence", "published", "link"]
    ],
    use_container_width=True,
    hide_index=True
)