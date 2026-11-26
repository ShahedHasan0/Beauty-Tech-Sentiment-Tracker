import pandas as pd
from transformers import pipeline
from pathlib import Path

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

    #Read the collected headlines
    df = pd.read_csv(input_file)

    print(f"Analyzing {len(df)} headlines...")

    #Analyze sentiment
    df = analyze_sentiment(df)

    #Save results
    output_file = Path("data/sentiment_results.csv")
    df.to_csv(output_file, index=False, encoding="utf-8-sig")

    print("\nSentiment analysis complete!")
    print(f"Results saved to: {output_file}")

    print("\nSentiment summary:")
    print(df["sentiment"].value_counts())


if __name__ == "__main__":
    main()