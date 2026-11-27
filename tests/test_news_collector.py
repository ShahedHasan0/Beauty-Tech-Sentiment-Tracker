from src.news_collector import collect_news


#Test that collecting an empty list of brands returns an empty DataFrame
def test_empty_brands():
    df = collect_news([])

    assert df.empty
    assert list(df.columns) == ["brand", "headline", "link", "published"]

#Test that duplicate articles are removed
def test_duplicate_articles(monkeypatch):

    #Create fake news articles
    fake_articles = [
        {
            "brand": "FOREO",
            "headline": "FOREO launches a new device",
            "link": "https://example.com/article1",
            "published": "2026-11-20"
        },
        {
            "brand": "FOREO",
            "headline": "FOREO launches a new device",
            "link": "https://example.com/article1",
            "published": "2026-11-20"
        }
    ]

    #Replace the real news fetching function with fake data
    monkeypatch.setattr(
        "src.news_collector.fetch_news",
        lambda brand: fake_articles
    )

    #Collect and clean the fake articles
    df = collect_news(["FOREO"])

    #Only one article should remain
    assert len(df) == 1