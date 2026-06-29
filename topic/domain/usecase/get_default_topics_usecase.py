from topic.domain.entity.topic_entity import TopicEntity
from topic.domain.repository.default_topic_repository import DefaultTopicRepository


class GetDefaultTopicsUseCase:

    def __init__(self, default_topic_repository: DefaultTopicRepository):
        self.default_topic_repository = default_topic_repository

    def execute(self) -> list[TopicEntity]:
        return self.default_topic_repository.get_default_topics()
