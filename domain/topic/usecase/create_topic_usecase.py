from domain.topic.repository.topic_repository import TopicRepository

class CreateTopicUseCase:
    def __init__(self, topic_repository: TopicRepository):
        self.topic_repository = topic_repository

    def execute(self, userId: str, name: str) -> dict:
        return self.topic_repository.create_topic(userId, name)