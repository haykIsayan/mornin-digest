class DigestEntity:
    def __init__(self, digestId: str, userId: str, articles: list[dict]):
        self.digestId = digestId
        self.userId = userId
        self.articles = articles
