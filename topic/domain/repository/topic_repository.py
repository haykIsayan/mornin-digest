from abc import ABC, abstractmethod

from topic.domain.entity.topic_entity import TopicEntity

class TopicRepository(ABC):

    @abstractmethod
    def get_all_topics(self, user_id: str) -> list[TopicEntity]:
        pass

    @abstractmethod
    def create_topic(self, user_id: str, name: str) -> TopicEntity:
        pass
