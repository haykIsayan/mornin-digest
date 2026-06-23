from topic.domain.entity.topic_entity import TopicEntity
from topic.domain.repository.topic_repository import TopicRepository


class GetAllTopicsUseCase:

    def __init__(self, topic_repository: TopicRepository):
        self.topic_repository = topic_repository

    def execute(self, user_id: str) -> list[TopicEntity]:
        return self.topic_repository.get_all_topics(user_id)
