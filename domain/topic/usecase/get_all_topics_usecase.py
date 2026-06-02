from domain.topic.entity.topic_entity import TopicEntity
from domain.topic.repository.topic_repository import TopicRepository


class GetAllTopicsUseCase:

    def __init__(self, topic_repository: TopicRepository):
        self.topic_repository = topic_repository

    def execute(self, userId: str) -> list[TopicEntity]:
        return self.topic_repository.get_all_topics(userId)