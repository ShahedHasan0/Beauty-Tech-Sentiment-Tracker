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

#Test that articles are sorted from newest to oldest
def test_articles_sorted_by_date(monkeypatch):

    #Create articles with different publication dates
    fake_articles = [
        {
            "brand": "FOREO",
            "headline": "Older article",
            "link": "https://example.com/old",
            "published": "2026-11-01"
        },
        {
            "brand": "FOREO",
            "headline": "Newest article",
            "link": "https://example.com/new",
            "published": "2026-11-25"
        },
        {
            "brand": "FOREO",
            "headline": "Middle article",
            "link": "https://example.com/middle",
            "published": "2026-11-15"
        }
    ]

    #Use fake articles instead of Google News
    monkeypatch.setattr(
        "src.news_collector.fetch_news",
        lambda brand: fake_articles
    )

    #Collect and clean the articles
    df = collect_news(["FOREO"])

    #Check the order of the headlines
    assert df["headline"].tolist() == [
        "Newest article",
        "Middle article",
        "Older article"
    ]