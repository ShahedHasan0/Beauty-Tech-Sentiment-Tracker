from src.news_collector import collect_news


#Test that collecting an empty list of brands returns an empty DataFrame
def test_empty_brands():
    df = collect_news([])

    assert df.empty
    assert list(df.columns) == ["brand", "headline", "link", "published"]
