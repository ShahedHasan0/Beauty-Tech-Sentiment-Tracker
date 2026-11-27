import pandas as pd
import sys
from unittest.mock import MagicMock

#Mock the Hugging Face pipeline before importing our analyzer
mock_transformers = MagicMock()
sys.modules["transformers"] = mock_transformers

from src.sentiment_analyzer import analyze_sentiment


#Test that sentiment analysis adds the correct columns
def test_sentiment_columns(monkeypatch):

    #Create fake article data
    df = pd.DataFrame({
        "headline": ["FOREO launches a new device"]
    })

    #Create a fake model prediction
    def fake_prediction(headline):
        return [{"label": "positive", "score": 0.91234}]

    #Replace the real model with our fake prediction
    monkeypatch.setattr(
        "src.sentiment_analyzer.sentiment_analyzer",
        fake_prediction
    )

    #Analyze the fake headline
    result = analyze_sentiment(df)

    #Check that the results are correct
    assert "sentiment" in result.columns
    assert "confidence" in result.columns
    assert result["sentiment"].iloc[0] == "positive"
    assert result["confidence"].iloc[0] == 0.912
