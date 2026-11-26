from transformers import pipeline

#Load the sentiment analysis model
model_name = "cardiffnlp/twitter-xlm-roberta-base-sentiment"

sentiment_analyzer = pipeline(
    "text-classification",
    model=model_name,
    tokenizer=model_name
)

#Example headlines to test
headlines = [
    "The new beauty device receives excellent customer reviews",
    "The company announces a new skincare device",
    "Customers complain about defective beauty products"
]

#Analyze each headline
for headline in headlines:
    result = sentiment_analyzer(headline)[0]

    print(f"\nHeadline: {headline}")
    print(f"Sentiment: {result['label']}")
    print(f"Confidence: {result['score']:.2f}")
