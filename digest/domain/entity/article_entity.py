class ArticleEntity:
    def __init__(self, article_id: str, topic: str, title: str, summary: str, source: str, url: str, published_date: str):
        self.article_id = article_id
        self.topic = topic
        self.title = title
        self.summary = summary
        self.source = source
        self.url = url
        self.published_date = published_date
