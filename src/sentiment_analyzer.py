import pandas as pd
from transformers import pipeline
from pathlib import Path
from datetime import datetime, timezone

#Load the sentiment model
model_name = "cardiffnlp/twitter-xlm-roberta-base-sentiment"

sentiment_analyzer = pipeline(
    "text-classification",
    model=model_name,
    tokenizer=model_name
)


#Analyze headlines
def analyze_sentiment(df):
    sentiments = []
    confidences = []

    for headline in df["headline"]:
        result = sentiment_analyzer(headline)[0]

        sentiments.append(result["label"])
        confidences.append(round(result["score"], 3))

    df["sentiment"] = sentiments
    df["confidence"] = confidences

    return df


#Run sentiment analysis
def main():
    input_file = Path("data/headlines.csv")
    output_file = Path("data/sentiment_results.csv")

    #Read the latest collected headlines
    df = pd.read_csv(input_file)

    #Read previous results if the file exists
    if output_file.exists():
        old_df = pd.read_csv(output_file)
    else:
        old_df = pd.DataFrame()

    #Find articles that have not been analyzed before
    if not old_df.empty:
        old_articles = set(
            zip(old_df["brand"], old_df["link"])
        )

        df = df[
            ~pd.Series(
                list(zip(df["brand"], df["link"])),
                index=df.index
            ).isin(old_articles)
        ]

    print(f"New articles to analyze: {len(df)}")

    #Analyze only new articles
    if not df.empty:
        df = analyze_sentiment(df)

        #Record when articles were collected
        df["collected_at"] = datetime.now(timezone.utc).isoformat()

        #Combine old and new results
        df = pd.concat([old_df, df], ignore_index=True)
    else:
        df = old_df

    #Save the complete historical dataset
    df.to_csv(output_file, index=False, encoding="utf-8-sig")

    print("\nSentiment analysis complete!")
    print(f"Total saved articles: {len(df)}")
    print(f"Results saved to: {output_file}")

    if not df.empty:
        print("\nSentiment summary:")
        print(df["sentiment"].value_counts())


if __name__ == "__main__":
    main()