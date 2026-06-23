class DigestEntity:
    def __init__(self, digest_id: str, user_id: str, articles: list[dict]):
        self.digest_id = digest_id
        self.user_id = user_id
        self.articles = articles
